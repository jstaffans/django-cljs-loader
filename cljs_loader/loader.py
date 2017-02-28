from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import edn_format
from edn_format.edn_lex import Keyword
import re

class Loader():

    _bundles = {}

    def _remove_line_comments(self, lines):
        return [l for l in lines if not re.match(r'^\s*;', l)]


    def _strip_meta(self, raw):
        return re.sub(r'\^{.*?}', '', raw)


    def _get_output_to(self, build_config):
        return build_config.get(Keyword('compiler'), {}).get(Keyword('output-to'))


    def _get_output_bundles(self, builds):
        bundles = {}

        if type(builds) is edn_format.immutable_dict.ImmutableDict:
            for id, build_config in builds.items():
                bundles[id.name] = self._get_output_to(build_config)
        else:
            for build_config in builds:
                bundles[build_config.get(Keyword('id'))] = self._get_output_to(build_config)

        return bundles


    def get_bundles(self):
        if self._bundles != {}:
            return self._bundles

        with open(settings.CLJS_LOADER['PROJECT_FILE'], 'r') as project_file:
            raw = ''.join(self._remove_line_comments(project_file.readlines()))

        content = self._strip_meta(raw)

        project_settings = edn_format.loads(content)

        # Get cljs output filenames

        key = Keyword('cljsbuild')
        if key in project_settings:
            cljsbuild = project_settings[project_settings.index(key) + 1]
        else:
            raise ImproperlyConfigured(':cljsbuild key not found in Leiningen project settings!')

        output_bundles = self._get_output_bundles(cljsbuild.get(Keyword('builds')))

        # Fish out figwheel port
        # TODO: production will not use "localhost"

        host = 'localhost'
        port = 3449
        if Keyword('figwheel') in project_settings:
            port = project_settings[project_settings.index(Keyword('figwheel')) + 1] \
                .get(Keyword('server-port'), 3449)

        self._bundles = {k: 'http://{}:{}/{}'.format(host, port, v) for k, v in output_bundles.items()}

        return self._bundles


    def get_bundle(self, name):
        return self.get_bundles()[name]

