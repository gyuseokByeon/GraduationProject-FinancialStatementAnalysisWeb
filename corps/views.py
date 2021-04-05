from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from . import models
from stocks import models as stock_models
import pandas as pd

class CorpDetailView(DetailView):
    model = models.Corp
    template_name = "corps/corp_detail.html"



    #주가 데이터 가져오기

    def get_context_data(self, **kwargs):
        context = super(CorpDetailView, self).get_context_data(**kwargs)
        stocks_df = pd.DataFrame.from_records(stock_models.Stock.objects.filter(code=self.kwargs['corp_code']).values_list('date', 'open', 'high', 'low', 'close'))
        context['stocks'] = stocks_df
        print(context['stocks'])
        return context


    def get_object(self):
        object = get_object_or_404(models.Corp, corp_code = self.kwargs['corp_code'])
        return object

