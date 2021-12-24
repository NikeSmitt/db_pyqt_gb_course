import logging
import logging.handlers
import os


formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs', 'client.log'))


log_file = logging.FileHandler(
    filename=file_path,
    encoding='utf-8',
)
log_file.setFormatter(formatter)

logger = logging.getLogger('client')
logger.addHandler(log_file)
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    logger.critical('Some critical error')
    logger.error('Some error')
    logger.warning('Some warning')
    logger.debug('Debug info')
    logger.info('Information')
