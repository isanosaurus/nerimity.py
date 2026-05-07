import logging
import traceback
import datetime
from nerimity._enums import Colors

_OK_LEVEL = 25
logging.addLevelName(_OK_LEVEL, "OK")

_LEVEL_COLORS = {
    logging.DEBUG:   Colors.CYAN,
    logging.INFO:    Colors.MAGENTA,
    _OK_LEVEL:       Colors.GREEN,
    logging.WARNING: Colors.YELLOW,
    logging.ERROR:   Colors.RED,
}

class _ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        color = _LEVEL_COLORS.get(record.levelno, Colors.WHITE)
        timestamp = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f')
        return f"{color}[{timestamp}]{Colors.WHITE} | {record.getMessage()}"


class _Logger:
    def __init__(self) -> None:
        self._log = logging.getLogger("nerimity")
        self._log.setLevel(logging.DEBUG)
        self._log.propagate = False
        handler = logging.StreamHandler()
        handler.setFormatter(_ColorFormatter())
        self._log.addHandler(handler)

    def log(self, message: str) -> None:
        self._log.info(message)

    def ok(self, message: str) -> None:
        self._log.log(_OK_LEVEL, message)

    def warn(self, message: str) -> None:
        self._log.warning(message)

    def error(self, message: str, exc: BaseException = None) -> None:
        self._log.error(message)
        if exc is not None:
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            self._log.error(f"{Colors.RED}{tb.rstrip()}{Colors.WHITE}")

    def debug(self, message: str) -> None:
        self._log.debug(message)


logger = _Logger()
