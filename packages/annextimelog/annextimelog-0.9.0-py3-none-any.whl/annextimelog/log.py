# system modules
import logging
import locale

# external modules
from rich.console import Console
from rich.logging import RichHandler

logger = logging.getLogger(__name__)

stdout = Console()
stderr = Console(stderr=True)

# Allow locale for strftime etc.
locale.setlocale(locale.LC_ALL, "")


def setup_logging(**kwargs):
    default_kwargs = dict(
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=stderr,  # log to stderr
                rich_tracebacks=True,
                show_path=kwargs.get("level", logging.INFO) < logging.DEBUG - 10,
            )
        ],
    )
    logging.basicConfig(**{**default_kwargs, **kwargs})
