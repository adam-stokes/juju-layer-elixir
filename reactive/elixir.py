from charms.reactive import (
    set_state,
    when_not,
    when
)

from charms import apt

from charmhelpers.core import (hookenv, unitdata)

config = hookenv.config()
kv = unitdata.kv()


@when_not('elixir.available')
def install_elixir():
    """ Installs elixir

    Emits:
    elixir.available: Emitted once the runtime has been installed
    """

    kv.set('elixir.url', config.get('install_sources'))

    apt.queue_install(['elixir'])


@when('apt.installed.elixir')
@when_not('elixir.available')
def elixir_ready():
    hookenv.status_set('active', 'Elixir is ready')
    set_state('elixir.available')
