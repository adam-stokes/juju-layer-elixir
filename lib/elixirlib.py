import os
import sys
from shell import shell

from charmhelpers.core import hookenv


def elixir_dist_dir():
    """ Absolute path of Elixir application dir

    Returns:
    Absolute string of elixir application directory
    """
    config = hookenv.config()
    return os.path.join(config['app-path'])


def mix(cmd):
    """ Runs Mix

    Usage:

       mix('compile')
       mix('test')
       mix('run')

    Arguments:
    cmd: Command to run can be string or list

    Returns:
    Will halt on error
    """
    hookenv.status_set(
        'maintenance',
        'Running Mix build tool')
    os.chdir(elixir_dist_dir())
    if not isinstance(cmd, str):
        hookenv.status_set('blocked', '{}: should be a string'.format(cmd))
        sys.exit(0)
    cmd = ("mix {}".format(cmd))
    sh = shell(cmd)
    if sh.code > 0:
        hookenv.status_set("blocked", "Mix error: {}".format(sh.errors()))
        sys.exit(0)
