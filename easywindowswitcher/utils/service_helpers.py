import logging
import shlex
import subprocess
from typing import Callable, Dict, List, Sequence, Tuple, Union


logger = logging.getLogger(__name__)

# Type aliases for the various apply_options() arguments
OptionKeyType = str
OptionValueType = Union[str, bool, Sequence[str]]
OptionsType = List[Tuple[OptionKeyType, OptionValueType]]
OptionsMapType = Dict[OptionKeyType, Callable[[OptionValueType], str]]

STDERR_INTO_OUTPUT = "STDERR_INTO_OUTPUT"
STDERR_SUPPRESS = "STDERR_SUPPRESS"
STDERR_DISPLAY = "STDERR_DISPLAY"

STDERR_OPTIONS = {
    STDERR_INTO_OUTPUT: subprocess.STDOUT,
    STDERR_SUPPRESS: subprocess.DEVNULL,
    STDERR_DISPLAY: None
}


def get_command_output(
    command: List[str],
    shell: bool = False,
    stderr_redirect: str = STDERR_SUPPRESS
) -> str:
    """
    Runs a command and cleans the result for use elsewhere.

    :param command: The command to run
    :param shell: Whether or not to run the command with an actual shell interpreter
    :param stderr_redirect: How to redirect stderr; one of STDERR_OPTIONS

    :return: The resulting output from the command being run.
    """
    logger.debug("Get command output: {}".format(" ".join(command)))

    try:
        stderr_option = STDERR_OPTIONS.get(stderr_redirect, subprocess.STDOUT)
        out = subprocess.check_output(_format_command(command, shell), stderr=stderr_option, shell=shell)

        # out is a utf-8 encoded byte string that must be converted to a literal string for use
        # rstrip() takes off the seemingly always present \n that's at the end of the result
        # strip("'") removes the single quotes that surround the result
        cleaned_out = out.decode("utf8").rstrip().strip("'")
        logger.debug("Command output: " + cleaned_out)

        if cleaned_out == "null":  # Some of the docker commands like to return literal "null"
            return ""
        else:
            return cleaned_out
    except subprocess.CalledProcessError as e:  # Return code was 1 or some other error code
        logger.debug(
            "Exception occured while trying to get command output: {}"
            "\nCommand output: {}".format(str(e), e.output.decode("utf8").rstrip())
        )
        logger.debug("Stacktrace: ", exc_info=True)

        return ""
    except Exception as e:  # Who knows what else went wrong
        logger.debug("Exception occured while trying to get command output: {}".format(str(e)))
        logger.debug("Stacktrace: ", exc_info=True)

        return ""


def call_command(command: List[str], shell: bool = False, **kwargs) -> bool:
    """
    Logs a command, calls it, and then returns the exit code.

    :param command: The command (in list form) to call
    :param shell: Whether or not to run the command using a system shell
    :param kwargs: Extra args to be passed to subprocess.call; see its docs for options

    :return: Whether or not the command was successful
    """
    log_command(command)
    exit_code = subprocess.call(_format_command(command, shell), shell=shell, **kwargs)
    logger.debug("Command exit code: {}".format(exit_code))

    return not bool(exit_code)


def log_command(command: List[str]) -> None:
    """Logs the given command."""
    logger.debug("Command: " + " ".join(command))


def escape_value(value: OptionValueType) -> OptionValueType:
    """Escapes an option value based on its type."""
    if isinstance(value, str):
        return shlex.quote(value)
    elif isinstance(value, Sequence):
        return [shlex.quote(v) for v in value]
    else:
        return value


def _format_command(command: List[str], shell: bool = False) -> Union[Sequence[str], str]:
    """
    Formats a command depending on whether or not it needs to be called with a shell
    (i.e. either a list or a string).
    """
    return command if not shell else " ".join(command)
