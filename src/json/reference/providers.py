"""
    json.reference.providers
    ~~~~~~~~~~~~~~~~~~~~~~~~

"""


__all__ = ['Provider', 'FilesystemProvider', 'PkgProvider']

import json
import logging
import pkg_resources
from .bases import Provider
from .exceptions import NotFound
from .util import loop

logger = logging.getLogger(__name__)


class PkgProvider(Provider):
    """
    Autoload providers declared into setuptools ``entry_points``.

    For example, with this setup.cfg::

        [entry_points]
        json.reference.contributions =
            spec = json.misc.providers:SpecProvider

    """

    namespace = 'json.reference.contributions'

    def __init__(self, namespace=None, configuration=None):
        self.namespace = namespace or self.namespace
        self.configuration = configuration or {}
        self.loaded = False

    def load(self):
        providers = {}
        for entrypoint in pkg_resources.iter_entry_points(self.namespace):
            kwargs = self.configuration.get(entrypoint.name, {})
            providers[entrypoint.name] = entrypoint.load()(**kwargs)
            logger.debug('loaded %s from %s', entrypoint, entrypoint.dist)
        self.providers = providers
        self.loaded = True


    def __getitem__(self, uri):
        if not self.loaded:
            self.load()

        for name, provider in self.providers.items():
            try:
                value = provider[uri]
                logger.info('got %s from %s', uri, name)
                return value
            except (KeyError, NotFound):
                pass
        raise NotFound('no providers could return {!r}'.format(uri))

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class FilesystemProvider(Provider):
    """
    Exposes json documents stored into filesystem.

    for example, with ``prefix=my:pref:`` and ``directory=my/directory``,
    this filesystem will be loaded as::

        my/directory/
            foo.json        -> my:pref:foo#
            bar.json        -> my:pref:bar#
            baz/
                quux.json   -> my:pref:baz/quux#

    """

    def __init__(self, directory, prefix=None):
        self.directory = directory
        self.prefix = prefix or ''
        self.loaded = False

    def load(self):
        data = {}

        l = len(self.directory)
        for filename in loop(self.directory, '*.json'):
            spec = filename[l:-5]
            with open(filename, 'r') as file:
                schema = json.load(file)
            data[spec] = schema

        # set the fallbacks
        for spec in sorted(data.keys(), reverse=True):
            if spec.startswith('draft-'):
                metaspec = spec.split('/', 1)[1]
                if metaspec not in data:
                    data[metaspec] = data[spec]

        self.data = data
        self.loaded = True

    def __getitem__(self, uri):
        if not self.loaded:
            self.load()

        if uri.startswith(self.prefix) and uri.endswith('#'):
            spec = uri[len(self.prefix):-1]

        try:
            return self.data[spec]
        except (KeyError, UnboundLocalError):
            raise NotFound(uri)

    def __iter__(self):
        for spec in self.data.keys():
            yield '{}{}#'.format(self.prefix, spec)

    def __len__(self):
        return len(self.data.keys())
