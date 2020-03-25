"""
Cango: A library for executing commands asynchronously.
"""
import queue
import subprocess
from threading import Event, Thread
from typing import IO, Callable, Iterator, List


class BackGroundPipeline(Thread):
    def __init__(self,
                 stdpipe: IO,
                 on_line: Callable,
                 name: str,
                 sentinel: str = ""):
        super().__init__(name=name)
        self.__stdpipe = stdpipe
        self.__on_line = on_line
        self.__finished = Event()
        self.__sentinel = sentinel

    def wait(self, timeout):
        return self.__finished.wait(timeout)

    def is_finished(self):
        return self.__finished.is_set()

    def run(self):
        self.__finished.clear()
        for line in iter(self.__stdpipe.readline, self.__sentinel):
            line = line.strip()
            self.__on_line(line)
        self.__finished.set()


def execute_cmd_async(cmd: List,
                      on_line: Callable = lambda line: None,
                      on_err_line: Callable = lambda line: None,
                      cwd: str = None):
    cmd_str = " ".join(cmd)
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            cwd=cwd)
    stdout = BackGroundPipeline(proc.stdout, on_line, "[out %s]" % cmd_str)
    stderr = BackGroundPipeline(proc.stderr, on_err_line, "[err %s]" % cmd_str)

    stdout.start()
    stderr.start()

    class R:
        @classmethod
        def join(cls):
            nonlocal stdout, stderr
            stdout.join()
            stderr.join()

        @classmethod
        def finished(cls):
            nonlocal stdout, stderr
            return stdout.is_finished() and stderr.is_finished()

        @classmethod
        def kill(cls):
            nonlocal proc
            proc.kill()

    return R


class ABCango:
    def __init__(self,
                 cmd: List,
                 cwd: str = None):
        self.cmd = cmd
        self.cwd = cwd
        self.result_queue = queue.Queue()

    def process_stdout(self, line: str):
        self.result_queue.put(line)

    def process_stderr(self, line: str):
        pass

    @property
    def finished(self) -> bool:
        return self._r.finished()

    def run(self):
        self._r = execute_cmd_async(
            cmd=self.cmd,
            on_line=self.process_stdout,
            on_err_line=self.process_stderr)

    def genresult(self) -> Iterator:
        while not self.finished:
            try:
                if not self.result_queue.empty():
                    yield self.result_queue.get(timeout=1)
            except queue.Empty:
                pass
            except KeyboardInterrupt:
                self._r.kill()
            finally:
                yield None

        self._r.join()

    def stop(self):
        self._r.kill()
