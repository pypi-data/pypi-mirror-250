#!/usr/bin/env python3

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

"""
This library is a wrapper for uuid, provided to generate repeatable UUIDs if requested.
"""

__version__ = "0.3.2"

import logging
import os
import pathlib
import sys
import typing
import uuid
import warnings

DEMO_UUID_BASE: typing.Optional[str] = None

DEMO_UUID_COUNTER: int = 0

_logger = logging.getLogger(pathlib.Path(__file__).name)


def _is_relative_to(p1: pathlib.Path, p2: pathlib.Path) -> bool:
    """
    This function provides pathlib.is_relative_to to Pythons before 3.9.  After the End of Life of Python 3.8, this function can be removed.
    """
    if sys.version_info < (3, 9):
        try:
            _ = p1.relative_to(p2)
            return True
        except ValueError:
            return False
    else:
        return p1.is_relative_to(p2)


def configure() -> None:
    global DEMO_UUID_BASE

    # _logger.debug("sys.argv = %r.", sys.argv)

    if os.getenv("DEMO_UUID_REQUESTING_NONRANDOM") == "NONRANDOM_REQUESTED":
        warnings.warn(
            "Environment variable DEMO_UUID_REQUESTING_NONRANDOM is deprecated.  See case_utils.local_uuid.demo_uuid for usage notes on its replacement, CASE_DEMO_NONRANDOM_UUID_BASE.  Proceeding with random UUIDs.",
            FutureWarning,
        )
        return

    env_base_dir_name = os.getenv("CASE_DEMO_NONRANDOM_UUID_BASE")
    if env_base_dir_name is None:
        return

    base_dir_original_path = pathlib.Path(env_base_dir_name)
    if not base_dir_original_path.exists():
        warnings.warn(
            "Environment variable CASE_DEMO_NONRANDOM_UUID_BASE is expected to refer to an existing directory.  Proceeding with random UUIDs.",
            RuntimeWarning,
        )
        return
    if not base_dir_original_path.is_dir():
        warnings.warn(
            "Environment variable CASE_DEMO_NONRANDOM_UUID_BASE is expected to refer to a directory.  Proceeding with random UUIDs.",
            RuntimeWarning,
        )
        return

    # Component: An emphasis this is an example.
    demo_uuid_base_parts = ["example.org"]

    # Component: Present working directory, relative to CASE_DEMO_NONRANDOM_UUID_BASE if that environment variable is an ancestor of pwd.
    base_dir_resolved_path = base_dir_original_path.resolve()
    srcdir_original_path = pathlib.Path(os.getcwd())
    srcdir_resolved_path = srcdir_original_path.resolve()
    # _logger.debug("base_dir_resolved_path = %r.", base_dir_resolved_path)
    # _logger.debug("srcdir_resolved_path = %r.", srcdir_resolved_path)
    try:
        srcdir_relative_path = srcdir_resolved_path.relative_to(base_dir_resolved_path)
        # _logger.debug("srcdir_relative_path = %r.", srcdir_relative_path)
        demo_uuid_base_parts.append(str(srcdir_relative_path))
    except ValueError:
        # If base_dir is not an ancestor directory of srcdir, default to srcdir.
        # _logger.debug("PWD is not relative to base path.")
        demo_uuid_base_parts.append(str(srcdir_resolved_path))

    # Component: Command of argument vector.
    env_venv_name = os.getenv("VIRTUAL_ENV")
    if env_venv_name is None:
        demo_uuid_base_parts.append(sys.argv[0])
    else:
        command_original_path = pathlib.Path(sys.argv[0])
        # _logger.debug("command_original_path = %r.", command_original_path)
        command_resolved_path = command_original_path.resolve()
        # _logger.debug("command_resolved_path = %r.", command_resolved_path)

        # The command could be a command embedded in a virtual
        # environment, or it could be a script external to any virtual
        # environment.
        venv_original_path = pathlib.Path(env_venv_name)
        venv_resolved_path = venv_original_path.resolve()
        if _is_relative_to(command_resolved_path, venv_resolved_path):
            command_relative_path = command_resolved_path.relative_to(
                venv_resolved_path
            )
            # _logger.debug("command_relative_path = %r.", command_relative_path)
            demo_uuid_base_parts.append(str(command_relative_path))
        else:
            demo_uuid_base_parts.append(str(command_original_path))

    if len(sys.argv) > 1:
        # Component: Arguments of argument vector.
        demo_uuid_base_parts.extend(sys.argv[1:])

    # _logger.debug("demo_uuid_base_parts = %r.", demo_uuid_base_parts)

    DEMO_UUID_BASE = "/".join(demo_uuid_base_parts)


def demo_uuid() -> str:
    """
    This function generates a repeatable UUID, drawing on non-varying elements of the environment and process call for entropy.

    WARNING: This function was developed for use ONLY for reducing (but not eliminating) version-control edits to identifiers when generating sample data.  It creates UUIDs that are decidedly NOT random, and should remain consistent on repeated calls to the importing script.

    To prevent accidental non-random UUID usage, an environment variable, CASE_DEMO_NONRANDOM_UUID_BASE, must be set to a string provided by the caller.  The variable's required value is the path to some directory.  The variable's recommended value is the equivalent of the Make variable "top_srcdir" - that is, the root directory of the containing Git repository, some parent of the current process's current working directory.
    """
    global DEMO_UUID_BASE
    global DEMO_UUID_COUNTER

    if os.getenv("CASE_DEMO_NONRANDOM_UUID_BASE") is None:
        raise ValueError(
            "demo_uuid() called without CASE_DEMO_NONRANDOM_UUID_BASE in environment."
        )

    if DEMO_UUID_BASE is None:
        raise ValueError("demo_uuid() called with DEMO_UUID_BASE unset.")

    parts = [DEMO_UUID_BASE]

    # Component: Incrementing counter.
    DEMO_UUID_COUNTER += 1
    parts.append(str(DEMO_UUID_COUNTER))

    return str(uuid.uuid5(uuid.NAMESPACE_URL, "/".join(parts)))


def local_uuid() -> str:
    """
    Generate either a UUID4, or if requested via environment configuration, a non-random demo UUID.
    """
    global DEMO_UUID_BASE
    if DEMO_UUID_BASE is None:
        return str(uuid.uuid4())
    else:
        return demo_uuid()
