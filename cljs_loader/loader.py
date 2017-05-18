from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import edn_format
from edn_format.edn_lex import Keyword
from functools import partial
import re


class CljsBuildSettings():

    """
    A wrapper for the cljsbuild section of a Leiningen project file.
    Responsible for parsing the bits of information needed for Django integration.
    """

    def __init__(self, cljsbuild_edn):
        self.root = settings.CLJS_LOADER['ROOT']
        self.cljsbuild_edn = cljsbuild_edn

    def _get_output_to(self, build_config):
        return build_config\
            .get(Keyword('compiler'), {})\
            .get(Keyword('output-to'), '')\
            .replace(self.root, '')

    def _get_on_jsload(self, build_config):
        on_jsload = build_config\
                    .get(Keyword('figwheel'), {})\
                    .get(Keyword('on-jsload'), None)

        if on_jsload:
            return on_jsload

        # fish out the "main" namespace, assume there's an (exported) function called "main"
        main = build_config.get(Keyword('compiler'), {}).get(Keyword('main'), None)

        if main:
            return '{}/main'.format(main)

        raise ImproperlyConfigured('Couldn\'t determine JavaScript function to call on page load!')


    def get_output_bundles(self):
        bundles = {}

        builds = self.cljsbuild_edn.get(Keyword('builds'), None)

        if builds is None:
            raise ImproperlyConfigured('No builds found in cljsbuild section!')

        if type(builds) is edn_format.immutable_dict.ImmutableDict:
            for id, build_config in builds.items():
                bundles[id.name] = {
                    'url': self._get_output_to(build_config),
                    'on-jsload': self._get_on_jsload(build_config)
                }
        else:
            for build_config in builds:
                bundles[build_config.get(Keyword('id'))] = {
                    'url': self._get_output_to(build_config),
                    'on-jsload': self._get_on_jsload(build_config)
                }

        return bundles


class Loader():

    """
    Determines loadable bundles from a Leiningen project file.

    TODO: default settings (merge with Django settings)
    """

    def __init__(self):
        # setup cache
        self._bundles = {}

    def _remove_line_comments(self, lines):
        return [l for l in lines if not re.match(r'^\s*;', l)]

    def _strip_meta(self, raw):
        return re.sub(r'\^{.*?}', '', raw)

    def _format_for_output_figwheel(self, host, port, bundle):
        return {
            'url': 'http://{}:{}/{}'.format(host, port, bundle['url']),
            'on-jsload': '{}()'.format(bundle['on-jsload'].replace('/', '.'))
        }

    def _format_for_output_static(self, bundle):
        return {
            'url': '{}{}'.format(
                settings.STATIC_URL,
                bundle['url']),
            'on-jsload': '{}()'.format(bundle['on-jsload'].replace('/', '.'))
        }

    def get_bundles(self):
        if self._bundles != {}:
            return self._bundles

        with open(settings.CLJS_LOADER['PROJECT_FILE'], 'r') as project_file:
            raw = ''.join(self._remove_line_comments(project_file.readlines()))

        content = self._strip_meta(raw)

        project_settings = edn_format.loads(content)

        # Get cljs output filenames

        if Keyword('cljsbuild') in project_settings:
            cljsbuild = project_settings[project_settings.index(Keyword('cljsbuild')) + 1]
        else:
            raise ImproperlyConfigured(':cljsbuild key not found in Leiningen project settings!')

        cljsbuild_settings = CljsBuildSettings(cljsbuild)
        output_bundles = cljsbuild_settings.get_output_bundles()

        if settings.CLJS_LOADER['FIGWHEEL']:
            host = 'localhost'
            port = 3449

            if Keyword('figwheel') in project_settings:
                port = project_settings[project_settings.index(Keyword('figwheel')) + 1] \
                    .get(Keyword('server-port'), 3449)

            format_for_output = partial(self._format_for_output_figwheel, host, port)
        else:
            format_for_output = self._format_for_output_static

        self._bundles = {k: format_for_output(v) for k, v in output_bundles.items()}

        return self._bundles


    def get_bundle(self, name):

        return self.get_bundles()[name]

