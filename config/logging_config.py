import logging

SUCCESS = "\033[92m"
FAIL = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: RESET + "%(asctime)s - %(message)s" + RESET,
        logging.INFO: "%(asctime)s - %(message)s" + RESET,
        logging.WARNING: BOLD + "%(asctime)s - %(message)s" + RESET,
        logging.ERROR: FAIL + "%(asctime)s - %(message)s" + RESET,
        logging.CRITICAL: BOLD + FAIL + "%(asctime)s - %(message)s" + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        if "TEST COMPILATION SUCCESSFUL" in record.getMessage():
            log_fmt = SUCCESS + "%(asctime)s - %(message)s" + RESET
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)
