import json
import time
from datetime import datetime
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from . import models
from stocks import models as stock_models


class CorpDetailView(DetailView):
    model = models.Corp
    template_name = "corps/corp_detail.html"



    #주가 데이터 가져오기

    def get_context_data(self, **kwargs):
        context = super(CorpDetailView, self).get_context_data(**kwargs)
        stocks_query = stock_models.Stock.objects.filter(code=self.kwargs['corp_code'])
        stocks_list = list(stocks_query.values_list('date', 'open', 'high', 'low', 'close'))



        for i in range(len(stocks_list)):
            stocks_list[i] = list(stocks_list[i])
            date = stocks_list[i][0].__str__()
            stocks_list[i][0] = date
            if i == 999:
                print(date)
                date += " 03:00:00"
                date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                time.time()
                print(date_time_obj.time())

        stocks_json = json.dumps(stocks_list)
        context['stocks'] = stocks_json
        return context




    def get_object(self):
        object = get_object_or_404(models.Corp, corp_code = self.kwargs['corp_code'])
        return object

