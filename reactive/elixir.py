import os
import sys
from shell import shell

from charms.reactive import (
    hook,
    set_state,
    remove_state,
    main
)

from charmhelpers.core import hookenv
from charmhelpers.fetch import (
    apt_purge,
    apt_install,
    apt_update
)

config = hookenv.config()


@hook('install')
def install_elixir():
    """ Installs elixir

    Emits:
    elixir.available: Emitted once the runtime has been installed
    """
    remove_state('elixir.available')
    hookenv.status_set('maintenance', 'Installing Elixir')

    if os.path.isfile('/etc/apt/sources.list.d/erlang-solutions.list'):
        os.remove('/etc/apt/sources.list.d/erlang-solutions.list')

    url = "https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb"
    sh = shell('wget -q -O /tmp/elixir.deb {} && '
               'sudo dpkg -i /tmp/elixir.deb'.format(url))
    if sh.code > 0:
        hookenv.status_set(
            'blocked',
            'Problem installing Elixir: {}'.format(sh.errors()))
        sys.exit(0)

    apt_update()
    apt_purge(['elixir'])
    apt_install(['elixir'])
    hookenv.status_set('maintenance', 'Installing Elixir completed.')

    hookenv.status_set('active', 'Elixir is ready!')
    set_state('elixir.available')


if __name__ == "__main__":
    main()
