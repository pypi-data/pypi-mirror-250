# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import hashlib

from contrast_vendor.importlib_metadata import packages_distributions

CONTRAST_AGENT_DIST = "contrast-agent"

# Both of these metadata files contain a file list of what is installed under the top level dirs
RECORD = "RECORD"
SOURCES = "SOURCES.txt"

NAMESPACE_PACKAGE = "namespace_packages.txt"
TOP_LEVEL_TXT = "top_level.txt"

PY_SUFFIX = ".py"
SO_SUFFIX = ".so"

SITE_PACKAGES_DIR = f"{os.sep}site-packages{os.sep}"
DIST_PACKAGES_DIR = f"{os.sep}dist-packages{os.sep}"

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

INSTALLED_DISTRIBUTIONS = None
INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS = None


def _load_installed_dist_top_level_imports(cache):
    """
    Returns a dictionary containing a mapping of the package name to each of its top level importable packages by name.
    """
    if cache is None:
        cache = {}

    for top_level_import, dist_names in packages_distributions().items():
        dist_names = set(dist_names)

        for dist in dist_names:
            if cache.get(dist, None) is None:
                cache[dist] = {
                    top_level_import,
                }
            else:
                cache[dist].add(top_level_import)

    return cache


def load_packages_cache():
    global INSTALLED_DISTRIBUTIONS
    global INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS

    INSTALLED_DISTRIBUTIONS = None
    INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS = {}

    _load_installed_dist_top_level_imports(INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS)

    INSTALLED_DISTRIBUTIONS = list(INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS.keys())


def get_installed_dist_names():
    return INSTALLED_DISTRIBUTIONS


def is_editable_install(dist, version, all_files):
    editable_install_metadata_fname = f"__editable__{dist.lower()}-{version}.pth"

    return editable_install_metadata_fname in all_files


def normalize_file_name(file_path):
    """
    This function converts a file ending in .pyc to .py. The reason for this
    is due to how screener is configured to verify a file was reported (only supports
    exact match not a regex)
    @param file_path: full path to a python file ending in .pyc or .py
    @return: file_path ending in .py
    """
    file_to_report = file_path.rpartition(SITE_PACKAGES_DIR)

    if not file_to_report[1]:
        file_to_report = file_path.rpartition(DIST_PACKAGES_DIR)
        if not file_to_report[1]:
            return None

    normalized_file_name = file_to_report[2]
    if normalized_file_name.endswith(".pyc"):
        normalized_file_name = normalized_file_name[: len(normalized_file_name) - 1]

    return normalized_file_name


def _parse_top_level_dirs_from_manifest_file(dist, namespace, metadata_filename):
    """
    @param dist: Distribution object used to check to see what
    metadata files exist for us to parse
    @type dist: pkg_resources.DistInfoDistribution
    @param namespace: The name of the namespace to search
    @type namespace: string
    @param metadata_filename: Name of metadata file to parse
    @type metadata_filename: string
    """
    top_level_dirs = set()

    if dist.has_metadata(metadata_filename):
        for line in dist.get_metadata_lines(metadata_filename):
            if line.startswith(namespace + os.sep):
                dirs = line.split(os.sep)
                if len(dirs) > 1:
                    top_level_dirs.add(dirs[1])

    return top_level_dirs


def get_top_level_directories_namespace_pkg(dist, namespace):
    """
    @param dist: Distribution object used to check to see what
    metadata files exist for us to parse
    @type dist: pkg_resources.DistInfoDistribution
    @param namespace: The name of the namespace to search
    @type namespace: string
    @return: The top level importable packages/modules under the namespace
    @rtype: string
    """
    top_level_dirs = set()
    manifest_files = (RECORD, SOURCES)

    if not dist:
        return top_level_dirs

    for manifest in manifest_files:
        top_level_dirs = _parse_top_level_dirs_from_manifest_file(
            dist, namespace, manifest
        )
        if top_level_dirs:
            break

    return top_level_dirs


def get_top_level_directories(dist):
    """
    Parse the top_level.txt or RECORD file for a dist to get the dist's
    top level directories.

    :param dist: instance of pkg_resources.DistInfoDistribution
    :return: list of strs representing names of top level dist directories
    """
    top_level_dirs = []

    if dist.has_metadata(TOP_LEVEL_TXT):
        top_level_dirs = list(dist.get_metadata_lines(TOP_LEVEL_TXT))
    elif dist.has_metadata(RECORD):
        top_level_dirs = _parse_record_lines(dist.get_metadata_lines(RECORD))
    else:
        logger.debug("Cannot find top level dirs for %s", dist)

    return top_level_dirs


def _parse_record_lines(record_data_generator):
    """
    For lines in a RECORD file, parse out the name(s) of the top level directories.

    :param record_data_generator: generator containing lines in RECORD file
    :return: list of strs representing names of top level dist directories
    """
    top_level_dirs = []
    for full_name in record_data_generator:
        name = full_name.split(",")[0]
        if os.sep in name and name.split(os.sep)[1] == "__init__.py":
            top_level_dirs.append(name.split(os.sep)[0])
        elif name.endswith(SO_SUFFIX):
            # Handle special case where an .so file is a top level importable module.
            # This library is loaded by importing the name of the file excluding
            # the platform specific name convention of the file
            # i.e remove .cpython-PY_VERSION-platform.so from module.cpython-PY_VERSION-platform.so
            top_level_dirs.append(name.split(".")[0])

    return top_level_dirs


def get_file_from_module(module):
    if hasattr(module, "__file__") and module.__file__:
        return os.path.realpath(module.__file__)

    return None


def get_url_from_dist(dist):
    """
    Gets the library url from either PKG-INFO or METADATA files
    :param dist: the distribution package where data is being parsed
    :return: the url of the package or "" if one wasn't discovered
    """
    home_page = "Home-page: "
    url = ""

    metadata = list(dist.get_metadata_lines(dist.PKG_INFO))
    for line in metadata:
        if line.startswith(home_page):
            url = line.split(home_page)[1]
            break
    else:
        logger.debug("Cannot find url for %s", dist)

    return url


def get_data(dist):
    """
    Given a dist, pulls name, version, manifest, and url out of the metadata
    :param dist: the distribution package whose package info is being retrieved
    :return: the package info from the metadata
    """
    version = dist.version
    manifest = dist.get_metadata(dist.PKG_INFO)
    url = get_url_from_dist(dist)
    return version, manifest, str(url)


def get_hash(name, version):
    """
    DO NOT ALTER OR REMOVE
    """
    to_hash = name + " " + version

    return hashlib.sha1(to_hash.encode("utf-8")).hexdigest()
