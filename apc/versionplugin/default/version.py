"""
This file contains only functions that deal with the version
of the repository. It can set a new version as a tag and look
up the current version.
"""
import subprocess
import logging

from apc.version.shared import VersionError, VersionNotFound, Version


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('apc.versionplugin.default')


__all__ = ('get_version', 'set_version')


def get_version():
    """
    Retrieve the version from the repo.
    
    It can be assumed that this script will be ran in the
    root of the repository.
    """
    # First try to get the current version using "git describe".
    # look for tags below the current commit, so we will never
    # tag the same commit twice!
    args = ['git', 'describe', '--abbrev=0', '--tags', 'HEAD^']
    version = None
    try:
        line = subprocess.check_output(args, stderr=None)
        version = line.strip()
    except subprocess.CalledProcessError as e:
        log.error("Git error: {0}".format(e))

    if not version:
        raise VersionNotFound("cannot find the current version. Please create an annotated tag x.y.z!")

    return Version(version)



def set_version(version):
    """
    Create a new tag on this repo with the version as specified.
    """
    if version.annotated:
        log.debug("writing annotated version {0}".format(version))
        if version.changelog and version.changelog != "":
            args = ["git", "tag", "-a", str(version), "-m", version.changelog]
            subprocess.check_call(args)
        else:
            raise VersionError("Changelog can not be empty when writing an annotated tag.")
    else:
        log.debug("writing version {0}".format(version))
        args = ["git", "tag", str(version)]
        subprocess.check_call(args)
