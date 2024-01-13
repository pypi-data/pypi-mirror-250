from django_filters.views import FilterView
from taggit.models import Tag


class QueryView(FilterView):
    url_name = None
    template_name = 'query_view/query.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tags'] = Tag.objects.all()
        context['url_name'] = self.url_name
        return context
