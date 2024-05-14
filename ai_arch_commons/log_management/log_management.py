import logging
import logging.config
import os


class CorrIdFilter(logging.Filter):
    """
    A simple log filter to ensure corr-id is populated
    """
    def filter(self, record):
        record.corrId = record.args.get("corrId") if 'corrId' in record.args else "no-corr"
        return True


def configure_logger(arg_log_config_file: str) -> None:
    logging.config.fileConfig(arg_log_config_file,
                              defaults={'logfilename': os.getenv('LOG_FILE_PATH', 'app.log')},
                              disable_existing_loggers=False)
    logger = logging.getLogger()

    logger.info('Log file creation done. Put a lot of log!')


