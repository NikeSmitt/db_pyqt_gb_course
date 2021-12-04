import inspect
import logging
import sys

if 'client' in sys.argv[0]:
    logger = logging.getLogger('client')
else:
    logger = logging.getLogger('server')


def log(func_to_log):
    def decorator(*args, **kwargs):
        logger.debug(f'Вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs} '
                     f'Вызов из модуля {func_to_log.__module__} '
                     f'Вызов из функции {inspect.stack()[1].function}', stacklevel=2)
        return func_to_log(*args, **kwargs)
    return decorator


class Log:
    def __call__(self, func_to_log,  *args, **kwargs):
        def save_log(*args, **kwargs):
            logger.debug(f'Вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs} '
                         f'Вызов из модуля {func_to_log.__module__} '
                         f'Вызов из функции {inspect.stack()[1].function}', stacklevel=2)
            return func_to_log(*args, **kwargs)
        return save_log

