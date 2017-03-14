from django.views.generic.base import TemplateView


class TestPageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(TestPageView, self).get_context_data(**kwargs)
        return context
