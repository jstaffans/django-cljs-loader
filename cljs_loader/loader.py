from django.conf import settings
import edn_format
import re


def _remove_line_comments(lines):
    return [l for l in lines if not re.match(r'^\s*;', l)]


def _strip_meta(raw):
    return re.sub(r'\^{.*?}', '', raw)


def get_bundle():
    with open(settings.CLJS_LOADER['PROJECT_FILE'], 'r') as project_file:
        raw = ''.join(_remove_line_comments(project_file.readlines()))

    content = _strip_meta(raw)
    project_settings = edn_format.loads(content)

    # TODO: fish out output bundle 

    return project_settings
