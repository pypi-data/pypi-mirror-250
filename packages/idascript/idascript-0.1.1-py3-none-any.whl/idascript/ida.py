import enum
import subprocess
import logging
from idascript import IDA_BINARY
from pathlib import Path
from multiprocessing import Pool, Queue
import queue
import os
from typing import List, Optional, Iterable, Union, Generator, Tuple

TIMEOUT_RETURNCODE: int = -1


class IDAException(Exception):
    """
    Base class for exceptions in the module.
    """

    pass


class IDANotStared(IDAException):
    """
    This exception is raised when attempting
    to call a function of the `IDA` class before
    having called `start`.
    """

    pass


class IDAModeNotSet(IDAException):
    """
    This exception is raised when the IDA Mode has not been set before calling `start`.
    """

    pass


class MultiIDAAlreadyRunning(IDAException):
    """
    Exception raised if the `map` function of MultiIDA
    is called while another map operation is still pending.
    Design choices disallow launching two MultiIDA.map
    function in the same time.
    """

    pass


class IDAMode(enum.Enum):
    """
    Different modes possible for the IDA class
    """

    # Default value
    NOTSET = enum.auto()

    # Used when IDA will be launched for an IDAPython script
    IDAPYTHON = enum.auto()

    # Used when IDA will be launched directly
    DIRECT = enum.auto()


class IDA:
    """
    Class representing an IDA execution on a given file
    with a given script. This class is a wrapper to
    subprocess IDA.
    """

    def __init__(self,
                 binary_file: Union[Path, str],
                 script_file: Optional[Union[str, Path]] = None,
                 script_params: Optional[List[str]] = None,
                 timeout: Optional[float] = None):
        """
        :param binary_file: path of the binary file to analyse
        :param script_file: path to the Python script to execute on the binary (if required)
        :param script_params: additional parameters to send either to the script or IDA directly
        """

        if not Path(binary_file).exists():
            raise FileNotFoundError("Binary file: %s" % binary_file)

        self.bin_file: Path = Path(binary_file).resolve()  #: File to the binary
        self._process = None

        self.script_file: Optional[Path] = None  #: script file to execute
        self.params: List[str] = []  #: list of paramaters given to IDA

        self.timeout: Optional[float] = timeout  #: Timeout for IDA execution

        if script_file is not None:  # Mode IDAPython
            self._set_idapython(script_file, script_params)
        else:  # Direct mode
            self._set_direct(script_params)

    def _set_idapython(self, script_file: Union[Path, str], script_params: List[str] = None) -> None:
        """
        Set IDAPython script parameter.

        :param script_file: path to the script to execute on the binary file
        :param script_params: additional parameters sent to the script (available via idc.ARGV in idapython)
        """

        if not Path(script_file).exists():
            raise FileNotFoundError("Script file: %s" % script_file)

        if script_params is None:
            script_params = []

        if script_params:
            if not isinstance(script_params, list):
                raise TypeError("script_params parameter should be a list")

        self.script_file = Path(script_file).resolve()
        self.params = [x.replace('"', '\\"') for x in script_params] if script_params else []
        self.mode = IDAMode.IDAPYTHON

    def _set_direct(self, script_options: List[str]) -> None:
        """
        Set parameters script in direct mode

        :param script_options: List of script options
        :return: None
        """

        for option in script_options:
            if ':' not in option:
                raise TypeError('Options must have a ":"')
            self.params.append(f'-O{option}')

        self.mode = IDAMode.DIRECT

    def start(self) -> None:
        """
        Start the IDA process on the binary.
        """

        cmd_line = [IDA_BINARY.as_posix(), '-A']

        if self.mode == IDAMode.IDAPYTHON:
            params = " "+" ".join(self.params) if self.params else ""
            cmd_line.append('-S%s%s' % (self.script_file.as_posix(), params))
        elif self.mode == IDAMode.DIRECT:
            cmd_line.extend(self.params)
        else:
            raise

        cmd_line.append(self.bin_file.as_posix())
        logging.debug(f"run: {' '.join(cmd_line)}")

        env = os.environ
        env["TVHEADLESS"] = "1"
        env["TERM"] = "xterm"

        self._process = subprocess.Popen(
            cmd_line,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            # See `https://www.hex-rays.com/blog/igor-tip-of-the-week-08-batch-mode-under-the-hood/`_
            env=env
        )

    @property
    def returncode(self) -> Optional[int]:
        """
        Get the returncode of the process. Raise IDANotStart
        if called before launching the process.
        """

        if self._process:
            return self._process.returncode
        else:
            raise IDANotStared()

    @property
    def terminated(self) -> bool:
        """
        Boolean function returning True if the process is terminated
        """

        if self._process:
            if self._process.poll() is not None:
                return True
            else:
                return False
        else:
            raise IDANotStared()

    @property
    def pid(self) -> int:
        """
        Returns the PID of the IDA process

        :return: int (PID of the process)
        """

        if self._process:
            return self._process.pid
        else:
            raise IDANotStared()

    def wait(self) -> int:
        """
        Wait for the process to finish. This function hangs until
        the process terminate. A timeout can be given which raises
        TimeoutExpired if the timeout is exceeded (subprocess mechanism).
        """

        if self._process:
            try:
                return self._process.wait(self.timeout)
            except subprocess.TimeoutExpired:
                self._process.terminate()
                return TIMEOUT_RETURNCODE
        else:
            raise IDANotStared()

    def terminate(self) -> None:
        """
        Call terminate on the IDA process (kill -15)
        """

        if self._process:
            self._process.terminate()
        else:
            raise IDANotStared()

    def kill(self) -> None:
        """
        Call kill on the IDA subprocess (kill -9)
        """

        if self._process:
            self._process.kill()
        else:
            raise IDANotStared()


class MultiIDA:
    """
    Class to trigger multiple IDA processes concurrently
    on a bunch of files.
    """

    _data_queue = Queue()
    _script_file: Optional[Path] = None
    _params: List[str] = []
    _running: bool = False
    _timeout: float = None

    @staticmethod
    def _worker_handle(bin_file) -> Tuple[int, str]:
        """
        Worker function run concurrently

        :param bin_file: binary file to analyse
        :return: return code, name of binary file
        """

        ida = IDA(bin_file, MultiIDA._script_file, MultiIDA._params, MultiIDA._timeout)

        ida.start()
        res = ida.wait()
        MultiIDA._data_queue.put((res, bin_file))
        
        return res, bin_file.name

    @staticmethod
    def map(generator: Iterable[Path],
            script: Union[str, Path] = None,
            params: List[str] = None,
            workers: int = None,
            timeout: Optional[float] = None) -> Generator[Tuple[int, Path], None, None]:
        """
        Iterator the generator sent and apply the script file on each
        file concurrently on a bunch of IDA workers. The function consume
        the generator as fast as it can occupy all the workers and yield a
        tuple (return code, path file) everytime an IDA process as terminated.

        :param generator: Iterable of file paths strings (or Path)
        :param script: path to the script to execute
        :param params: list of parameters to send to the script
        :param workers: number of workers to trigger in parallel
        :param timeout: timeout for IDA runs (-1 means infinity)
        :return: generator of files processed (return code, file path)
        """

        if MultiIDA._running:
            raise MultiIDAAlreadyRunning()

        MultiIDA._running = True

        MultiIDA._script_file = script

        MultiIDA._params = [] if params is None else params

        MultiIDA._timeout = timeout

        pool = Pool(workers)
        task = pool.map_async(MultiIDA._worker_handle, generator, chunksize=1)
        while True:
            try:
                data = MultiIDA._data_queue.get(True)
                if data:
                    yield data
            except queue.Empty:
                pass
            if task.ready():
                break
        MultiIDA._running = False
