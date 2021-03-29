from django.db.models import Q
from django.views.generic import TemplateView, ListView
from corps.models import Corp


class HomePageView(TemplateView):
    template_name = 'home.html'


class SearchResultsView(ListView):

    model = Corp
    template_name = 'search_result.html'

    def get_queryset(self): # new
        corp = self.request.GET.get('corp')
        corp_list = Corp.objects.filter(
            Q(corp_name__icontains=corp)
        )
        return corp_list