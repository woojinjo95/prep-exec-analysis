import logging

from app.db.session import db_session
from tenacity import (after_log, before_log, retry, stop_after_attempt,
                      wait_fixed)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db_session
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    init()


if __name__ == "__main__":
    main()
