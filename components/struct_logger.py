from pathlib import Path
import structlog
import logging


def create_logger(log_path: str, log_level: str = logging.WARNING):
    structlog.configure(
        # The structlog.make_filtering_bound_logger() method allows you to set a desired minimum level
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.WriteLoggerFactory(
            file=Path(log_path).with_suffix(".json").open("a"),
        ),
    )

    return structlog.get_logger()
