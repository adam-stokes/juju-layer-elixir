import os
import sys
from shell import shell

from charmhelpers.core.hookenv import status_set
from charmhelpers.core.hookenv import storage_get
from charmhelpers.core.hookenv import storage_list


def elixir_dist_dir():
    """ Absolute path of Elixir application dir

    Returns:
    Absolute string of elixir application directory
    """
    storage_id = storage_list('app')[0]
    return storage_get('location', storage_id)


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
    status_set(
        'maintenance',
        'Running Mix build tool')
    if not os.path.exists(elixir_dist_dir()):
        os.makedirs(elixir_dist_dir())
    os.chdir(elixir_dist_dir())
    if not isinstance(cmd, str):
        status_set('blocked', '{}: should be a string'.format(cmd))
        sys.exit(0)
    cmd = ("yes | mix {}".format(cmd))
    sh = shell(cmd)
    if sh.code > 0:
        status_set("blocked", "Mix error: {}".format(sh.errors()))
        sys.exit(0)
