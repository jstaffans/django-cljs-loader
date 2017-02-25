from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import edn_format
from edn_format.edn_lex import Keyword
import re


def _remove_line_comments(lines):
    return [l for l in lines if not re.match(r'^\s*;', l)]


def _strip_meta(raw):
    return re.sub(r'\^{.*?}', '', raw)


def _get_output_to(build_config):
    return build_config.get(Keyword('compiler'), {}).get(Keyword('output-to'))

def _get_output_bundles(builds):
    bundles = {}

    if type(builds) is edn_format.immutable_dict.ImmutableDict:
        for id, build_config in builds.items():
            bundles[id.name] = _get_output_to(build_config)
    else:
        for build_config in builds:
            bundles[build_config.get(Keyword('id'))] = _get_output_to(build_config)

    return bundles


def get_bundles():
    with open(settings.CLJS_LOADER['PROJECT_FILE'], 'r') as project_file:
        raw = ''.join(_remove_line_comments(project_file.readlines()))

    content = _strip_meta(raw)

    project_settings = edn_format.loads(content)

    key = Keyword('cljsbuild')
    if key in project_settings:
        cljsbuild = project_settings[project_settings.index(key) + 1]
    else:
        raise ImproperlyConfigured(':cljsbuild key not found in Leiningen project settings!')

    output_bundles = _get_output_bundles(cljsbuild.get(Keyword('builds')))

    return output_bundles

    # return [_bundle_name(b) for b in output_bundles]
