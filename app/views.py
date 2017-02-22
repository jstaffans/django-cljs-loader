from django.views.generic.base import TemplateView

from cljs_loader import loader

class TestPageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(TestPageView, self).get_context_data(**kwargs)
        context['project_settings'] = loader.get_bundle()
        return context
