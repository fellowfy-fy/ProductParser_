import logging
from dataclasses import dataclass
from datetime import datetime
from functools import partialmethod

log = logging.getLogger(__name__)


@dataclass
class CachedLog:
    level: str
    message: str
    time: str
    exception: str = ""


class CacheLogger:
    use_default: bool = True  # Use default logging.log
    logs: list[CachedLog] = list()

    def __init__(self) -> None:
        self.logs = list()

    def log(self, level: str, message: str = "", exc_info: Exception | None = None):
        log_entry = CachedLog(level=level, message=message, time=datetime.now().isoformat())

        if exc_info is not None:
            log_entry.exception = str(exc_info)

        self.logs.append(log_entry)

        if self.use_default:
            log.log(getattr(logging, level.upper()), message)

    def clear(self):
        self.logs.clear()

    def level_count(self, level: str):
        return len(list(filter(lambda x: x.level == level, self.logs)))

    debug = partialmethod(log, "debug")
    info = partialmethod(log, "info")
    warning = partialmethod(log, "warning")
    error = partialmethod(log, "error")
    critical = partialmethod(log, "critical")
