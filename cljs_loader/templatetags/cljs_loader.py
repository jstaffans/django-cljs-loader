from django import template
from django.utils.safestring import mark_safe

from cljs_loader import loader, utils

register = template.Library()

ldr = loader.Loader()

@register.simple_tag
def render_bundle(bundle_name):
    bundle = ldr.get_bundle(bundle_name)
    tag = utils.to_tag(bundle)
    return mark_safe(tag)
