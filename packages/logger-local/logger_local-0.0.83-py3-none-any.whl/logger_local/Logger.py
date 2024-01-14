from .LoggerLocal import LoggerLocal


class Logger(LoggerLocal):
    # TODO: For backward compatibility. added at 14/01/24, remove after a while.
    @staticmethod
    def create_logger(**kwargs):
        return LoggerLocal.create_logger(**kwargs)
