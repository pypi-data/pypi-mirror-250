# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import socket

from contrast import AGENT_CURR_WORKING_DIR
from contrast.utils.string_utils import truncate
from contrast_vendor.ruamel import yaml

from contrast.agent.protect.rule import ProtectionRule

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


CONFIG_LOCATIONS = [
    AGENT_CURR_WORKING_DIR,
    os.path.join(AGENT_CURR_WORKING_DIR, "settings"),
    "/etc/contrast/python/",
    "/etc/contrast/",
    "/etc/",
]

CONFIG_FILE_NAMES = ["contrast_security.yaml", "contrast_security.yml"]

# Valid options are defined in the spec:
# https://bitbucket.org/contrastsecurity/assess-specifications/src/master/vulnerability/capture-stacktrace.md
STACKTRACE_OPTIONS = ["ALL", "SOME", "NONE"]


def get_hostname():
    """
    Order of precedence for reporting server name:
    contrast_security.yaml (server.name) --> socket.gethostname() --> localhost
    """
    hostname = "localhost"

    try:
        hostname = socket.gethostname() or hostname
    except Exception as e:
        logger.debug(e)

    return truncate(hostname)


def load_yaml_config():
    """
    Checks for a yaml file at preconfigured file system location.

    See official documentation because this is valid across agents.

    Current order of precedence:
        file specified by CONTRAST_CONFIG_PATH env var
        os.getcwd()
        os.path.join(os.getcwd(), 'settings')
        /etc/contrast/python/
        /etc/contrast/
        /etc/

    :return: a dict object representation of the yaml config. {'enable': True, ....}
    """
    locations = CONFIG_LOCATIONS
    names = CONFIG_FILE_NAMES

    if "CONTRAST_CONFIG_PATH" in os.environ:
        filename = os.environ.get("CONTRAST_CONFIG_PATH")
        if os.path.isfile(filename):
            config = _load_config(filename)
            if config is not None:
                config["loaded_configuration_filename"] = filename
            return config
        logger.warning(
            "The path specified by CONTRAST_CONFIG_PATH is not a file -"
            " searching for configuration file in default locations",
            contrast_config_path=filename,
        )

    for path in locations:
        for name in names:
            file_path = os.path.join(path, name)

            if os.path.exists(file_path):
                # Common config dictates that agents should look only at the first
                # valid config file and not continue searching config files, even
                # if the first config cannot be loaded (due to format or else)
                config = _load_config(file_path)
                if config is not None:
                    config["loaded_configuration_filename"] = file_path
                return config

    return None


def _load_config(file_path):
    logger.info("Loading configuration file: %s", os.path.abspath(file_path))

    with open(file_path) as config_file:
        try:
            return yaml.YAML(typ="safe", pure=True).load(config_file)
        except yaml.scanner.ScannerError as ex:
            # config yaml cannot be loaded but agent should continue on in case
            # env vars are configured
            msg_prefix = "YAML validator found an error."
            msg = f"{msg_prefix} Configuration path: [{ex.problem_mark.name}]. Line [{ex.problem_mark.line}]. Error: {ex.problem}"
            logger.warning(msg)

    return None


def flatten_config(config):
    """
    Convert a nested dict such as
        {'enable': True,
        'application':
            {'name': 'dani-flask'},
        'foo':
        'agent':
            {'python':

    into
        'enable': True,
        'application.name': 'dani-flask',

    :param config: dict config with nested keys and values
    :return: dict, flattened where each key has one value.
    """
    flattened_config = {}

    def flatten(x, name=""):
        if isinstance(x, dict):
            for key in x:
                flatten(x[key], name + key + ".")
        elif x is not None:
            flattened_config[name[:-1]] = x

    flatten(config)
    return flattened_config


def str_to_bool(val):
    """
    Converts a str to a bool

    true -> True, false -> False
    """
    if isinstance(val, bool):
        return val
    if not isinstance(val, str):
        return False

    # The remainder of this function was ported from distutils
    val = val.lower()

    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"invalid truth value {val!r}")


def get_env_key(key):
    return os.environ.get(key)


def parse_disabled_rules(disabled_rules):
    if not disabled_rules:
        return []

    return [rule.lower() for rule in disabled_rules.split(",")]


def parse_stacktraces_options(option):
    option = option.upper()
    if option in STACKTRACE_OPTIONS:
        return option

    return "ALL"


def str_to_protect_mode_enum(mode):
    """
    Converts str config value to protect mode enum that the agent understands
    """
    if not mode:
        return ProtectionRule.OFF

    return getattr(ProtectionRule, mode.upper(), ProtectionRule.MONITOR)
