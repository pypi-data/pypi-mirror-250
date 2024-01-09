import inspect
import json
import logging
import os
import sys
import traceback

from dotenv import load_dotenv

load_dotenv()  # noqa: E402
from sdk.src.validate import validate_enviroment_variables
from user_context_remote.user_context import UserContext

from .Component import Component
from .debug_mode import DebugMode
from .fields import Fields
from .LoggerOutputEnum import LoggerOutputEnum
from .MessageSeverity import MessageSeverity
from .SendToLogzIo import SendTOLogzIo
from .Writer import Writer

logzio_token = os.getenv("LOGZIO_TOKEN")
logzio_url = "https://listener.logz.io:8071"
COMPUTER_LANGUAGE = "Python"
loggers = {}


class Logger(logging.Logger):
    @staticmethod
    def create_logger(**kwargs):
        validate_enviroment_variables()
        mandatory_fields = ('component_id', 'component_name', 'component_category', 'developer_email')
        if not all(k in kwargs.get('object', {}) for k in mandatory_fields):
            raise Exception(
                "please insert component_id, component_name, component_category and developer_email in your object")
        component_id = kwargs['object']['component_id']

        if component_id in loggers:  # cache
            return loggers.get(component_id)
        else:
            logger = Logger(**kwargs)
            loggers[component_id] = logger
            return logger

    def __init__(self, *,
                 handler: logging.Handler = logging.StreamHandler(stream=sys.stdout),
                 formatter: logging.Formatter = None,
                 level: int | str = None,
                 **kwargs) -> None:
        if logzio_token is None:
            # TODO: if we show the token anyway, we can simply use it as default value
            raise Exception(
                "Please set in your .env file LOGZIO_TOKEN=cXNHuVkkffkilnkKzZlWExECRlSKqopE")

        self.debug_mode = DebugMode(logger_minimum_severity=level)
        self.component_id = kwargs['object']['component_id']
        self.fields = {}
        self._writer = Writer()
        self.logzio_handler = SendTOLogzIo()
        self.write_to_sql = False
        self.user_context = None
        self.additional_fields = {}

        self.logger = self.initiate_logger(handler=handler, formatter=formatter,
                                           level=self.debug_mode.logger_minimum_severity)

        super().__init__(name=self.logger.name)

        self.init(**kwargs)

    @staticmethod
    def initiate_logger(*,
                        handler: logging.Handler = logging.StreamHandler(stream=sys.stdout),
                        formatter: logging.Formatter = None,
                        level: int = None) -> logging.Logger:
        if not formatter:
            if isinstance(handler, logging.StreamHandler) and stream_supports_colour(handler.stream):
                formatter = _ColourFormatter()
            else:
                dt_fmt = '%H:%M:%S'  # '%Y-%m-%d %H:%M:%S'
                formatter = logging.Formatter('[{asctime}] [{levelname:<8}]: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)

        logger = logging.getLogger()

        our_levels_to_logging = {
            MessageSeverity.Debug: logging.DEBUG,
            MessageSeverity.Verbose: logging.DEBUG,
            MessageSeverity.Init: logging.INFO,
            MessageSeverity.Start: logging.INFO,
            MessageSeverity.End: logging.INFO,
            MessageSeverity.Information: logging.INFO,
            MessageSeverity.Warning: logging.WARNING,
            MessageSeverity.Error: logging.ERROR,
            MessageSeverity.Exception: logging.ERROR,
            MessageSeverity.Critical: logging.CRITICAL,
        }
        # Debug = 100, Verbose = 200. If level = 101 we want the one that is bigger than 101, i.e. Verbose
        level = min(our_levels_to_logging.keys(),
                    key=lambda x: x.value if x.value >= level else MessageSeverity.Debug.value)

        logger.setLevel(our_levels_to_logging[MessageSeverity(level)])
        logger.addHandler(handler)
        return logger

    def __log(self, *, function, message_severity: MessageSeverity, log_message, **kwargs):
        if self.debug_mode.is_logger_output(self.component_id, LoggerOutputEnum.Console, message_severity.value):
            # TODO: should we use self.isEnabledFor(level)?
            #  https://docs.python.org/3/library/logging.html#logging.Logger.getEffectiveLevel
            if log_message or kwargs:  # filter empty logger.start() and logger.end()
                kwargs_to_print = kwargs.get('object', kwargs)
                function(f'{log_message or ""}'
                         f'{" | " if log_message and kwargs else ""}'
                         f'{("kwargs=" + str(kwargs_to_print) if kwargs else "")}')

        log_object = {
            'severity_id': message_severity.value,
            'severity_name': message_severity.name
        }
        if log_message:
            log_object['log_message'] = log_message

        if isinstance(kwargs.get('object'), Exception):
            stack_trace = traceback.format_exception(
                type(kwargs['object']), kwargs['object'], kwargs['object'].__traceback__)
            kwargs['object'] = {}  # it is now exception
            kwargs['object']['error_stack'] = f'{str(stack_trace)}'

        if 'object' not in kwargs:
            kwargs['object'] = {}
        kwargs['object'].update(log_object)

        kwargs = self.insert_to_payload_extra_vars(**kwargs)
        self.insert_to_object(**kwargs)

        if self.write_to_sql and self.debug_mode.is_logger_output(
                self.component_id, LoggerOutputEnum.MySQLDatabase, message_severity.value):
            self._writer.add_message_and_payload(log_message, **kwargs)
        if self.debug_mode.is_logger_output(self.component_id, LoggerOutputEnum.Logzio, message_severity.value):
            self.logzio_handler.send_to_logzio(kwargs['object'])

    def init(self, log_message=None, **kwargs):
        self.__log(function=logging.info, message_severity=MessageSeverity.Init, log_message=log_message, **kwargs)

    def start(self, log_message=None, **kwargs):
        self.__log(function=logging.info, message_severity=MessageSeverity.Start, log_message=log_message, **kwargs)

    def end(self, log_message=None, **kwargs):
        self.__log(function=logging.info, message_severity=MessageSeverity.End, log_message=log_message, **kwargs)

    def info(self, log_message=None, **kwargs):
        self.__log(function=logging.info, message_severity=MessageSeverity.Information,
                   log_message=log_message, **kwargs)

    def error(self, log_message=None, **kwargs):
        self.__log(function=logging.error, message_severity=MessageSeverity.Error, log_message=log_message, **kwargs)

    def warn(self, log_message=None, **kwargs):
        print("warn is deprecated, please use warning instead", file=sys.stderr)
        self.warning(log_message=log_message, **kwargs)

    def warning(self, log_message=None, **kwargs):
        self.__log(function=logging.warning, message_severity=MessageSeverity.Warning, log_message=log_message,
                   **kwargs)

    def debug(self, log_message=None, **kwargs):
        self.__log(function=logging.debug, message_severity=MessageSeverity.Debug, log_message=log_message, **kwargs)

    def critical(self, log_message=None, **kwargs):
        self.__log(function=logging.critical, message_severity=MessageSeverity.Critical, log_message=log_message,
                   **kwargs)

    def verbose(self, log_message=None, **kwargs):
        # verbose =~ debug
        self.__log(function=logging.debug, message_severity=MessageSeverity.Verbose, log_message=log_message, **kwargs)

    def exception(self, log_message=None, **kwargs):
        self.__log(function=logging.exception, message_severity=MessageSeverity.Exception, log_message=log_message,
                   **kwargs)

    def _insert_variables(self, **kwargs):
        object_data = kwargs.get("object", {})
        for field in self.fields.keys():
            if field in object_data.keys():
                self.fields[field] = object_data[field]
        for field in object_data.keys():
            if field not in self.fields:
                self.additional_fields[field] = object_data.get(field)

    def insert_to_object(self, **kwargs):
        object_data = kwargs.get("object", {})
        for field in self.fields.keys():
            if field not in object_data:
                field_value = self.fields[field]
                if field_value is not None:
                    object_data[field] = field_value

    def get_logger_table_fields(self):
        if self.write_to_sql:
            fields = Fields.getFieldsSingelton()
            for field in fields:
                self.fields[field] = None
        return self.fields

    def clean_variables(self):
        for field in self.fields:
            self.fields[field] = None
        self.additional_fields.clear()

    def insert_to_payload_extra_vars(self, **kwargs):
        self.user_context = UserContext.login_using_user_identification_and_password()
        if self.user_context is not None:
            # TODO Shall we change in the database column to real_user_id?
            kwargs['object']['user_id'] = self.user_context.get_real_user_id()
            kwargs['object']['created_user_id'] = self.user_context.get_real_user_id()
            # TODO Shall we change the database to store real_profile_id and effective_profile?
            kwargs['object']['profile_id'] = self.user_context.get_real_profile_id()
            # TODO: change to display_as like we have in contact ...
            if self.user_context.real_display_name is not None:
                # TODO Shall we change current_runner to real_name?
                kwargs['object']['current_runner'] = self.user_context.get_real_name()
            else:
                kwargs['object']['current_runner'] = os.getenv("PRODUCT_USER_IDENTIFIER")
        message = kwargs['object'].pop('message', None)
        kwargs['object']['function_name'] = self.get_current_function_name()
        kwargs['object']['environment'] = os.getenv("ENVIRONMENT_NAME")
        kwargs['object']['class'] = self.get_calling_class()
        kwargs['object']['line_number'] = self.get_calling_line_number()
        kwargs['object']['computer_language'] = COMPUTER_LANGUAGE
        for field in self.fields.keys():
            if field not in kwargs['object']:
                field_value = self.fields[field]
                if field_value is not None:
                    kwargs['object'][field] = field_value
        for field in self.additional_fields.keys():
            if field not in kwargs['object']:
                field_value = self.additional_fields[field]
                kwargs['object'][field] = field_value
        if self.write_to_sql:
            component_info = self.get_component_info(self.component_id)
            if component_info:
                for field in component_info.keys():
                    if field not in kwargs['object']:
                        field_value = component_info[field]
                        if field_value is not None:
                            kwargs['object'][field] = field_value
        if message is not None:
            kwargs['object']['message'] = message
        object_data = kwargs.get("object", {})
        object_data["record"] = json.dumps({key: str(value) for key, value in object_data.items()})
        if self.write_to_sql:
            object_data = {key: value for key, value in object_data.items() if key in self.fields.keys()}
            kwargs["object"] = object_data
        return kwargs

    @staticmethod
    def get_current_function_name():
        stack = inspect.stack()
        # 0 = 'get_current_function_name', 1 = 'insert_to_payload_extra_vars', 2 = '__log', 3 = start/end/info...
        caller_frame = stack[4]
        function_name = caller_frame.function
        return function_name

    @staticmethod
    def get_calling_class():
        stack = inspect.stack()
        calling_module = inspect.getmodule(stack[4].frame)
        return calling_module.__name__

    @staticmethod
    def get_calling_line_number():
        stack = inspect.stack()
        calling_frame = stack[4]
        line_number = calling_frame.lineno
        return line_number

    def get_component_info(self, component_id):
        result = Component.getDetailsByComponentId(component_id)
        if result:
            name, component_type, component_category, testing_framework, api_type = result
            component_info = {
                'component_id': component_id,
                'component_name': name,
                'component_type': component_type,
                'component_category': component_category,
                'testing_framework': testing_framework,
                'api_type': api_type
            }
            for field in component_info.keys():
                self.fields[field] = component_info[field]
            return component_info
        else:
            return None

    def is_component_complete(self):
        return (getattr(self, 'component_name') is None
                or getattr(self, 'component_type') is None
                or getattr(self, 'component_category') is None
                or getattr(self, 'testing_framework') is None
                or getattr(self, 'api_type') is None
                )

    def set_write_to_sql(self, value):
        self.write_to_sql = value
        if self.write_to_sql:
            self.get_logger_table_fields()


# Copyright: https://github.com/Rapptz/discord.py/blob/master/discord/utils.py#L1241
def is_docker() -> bool:
    path = '/proc/self/cgroup'
    return os.path.exists('/.dockerenv') or (os.path.isfile(path) and any('docker' in line for line in open(path)))


def stream_supports_colour(stream) -> bool:
    # Pycharm and Vscode support colour in their inbuilt editors
    COLORS_IN_LOGS = os.getenv("COLORS_IN_LOGS", "")
    if COLORS_IN_LOGS.lower() == "true":
        return True
    elif COLORS_IN_LOGS.lower() == "false":
        return False

    if 'PYCHARM_HOSTED' in os.environ or os.environ.get('TERM_PROGRAM') == 'vscode':
        return True

    is_a_tty = hasattr(stream, 'isatty') and stream.isatty()  # TTY = terminal
    if sys.platform != 'win32':
        # Docker does not consistently have a tty attached to it
        return is_a_tty or is_docker()

    # ANSICON checks for things like ConEmu
    # WT_SESSION checks if this is Windows Terminal
    return is_a_tty or ('ANSICON' in os.environ or 'WT_SESSION' in os.environ)


class _ColourFormatter(logging.Formatter):
    # ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher
    # It starts off with a format like \x1b[XXXm where XXX is a semicolon separated list of commands
    # The important ones here relate to colour.
    # 30-37 are black, red, green, yellow, blue, magenta, cyan and white in that order
    # 40-47 are the same except for the background
    # 90-97 are the same but "bright" foreground
    # 100-107 are the same as the bright ones but for the background.
    # '1' means bold, '2' means dim, '0' means reset, and '4' means underline.

    # TODO: add start/end levels & colours
    LEVEL_COLOURS = [
        (logging.DEBUG, '\x1b[40;1m'),
        (logging.INFO, '\x1b[34;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]

    FORMATS = {
        level: logging.Formatter(
            f'\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[0m %(message)s',
            '%H:%M:%S',  # '%Y-%m-%d %H:%M:%S'
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno, self.FORMATS[logging.DEBUG])

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output
