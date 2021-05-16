import json
from django.core import serializers
from django.http import JsonResponse
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from . import models
from stocks import models as stock_models
from financial_statements import models as fi_sta_models
from income_states import models as income_sta_models


class CorpDetailView(DetailView):
    model = models.Corp
    template_name = "corps/corp_detail.html"



    #주가 데이터 가져오기

    def get_context_data(self, **kwargs):
        context = super(CorpDetailView, self).get_context_data(**kwargs)



        # 주가정보
        stocks_query = stock_models.Stock.objects.filter(code=self.kwargs['corp_code'])
        stocks_list = list(stocks_query.values_list('datestamp', 'open', 'high', 'low', 'close', 'volume'))
        stocks_json = json.dumps(stocks_list)

        # 재무상태표
        fi_sta_query = fi_sta_models.Financial.objects.filter(code = self.kwargs['corp_code'])



        # 손익계산서
        fi_income_query = income_sta_models.Income.objects.filter(code = self.kwargs['corp_code'])


        context['stocks'] = stocks_json
        context['finances'] = fi_sta_query
        context['incomes'] = fi_income_query
        return context




    def get_object(self):
        object = get_object_or_404(models.Corp, corp_code = self.kwargs['corp_code'])
        return object


def ajax_finance(request, **kwargs):
    fi_sta_query = fi_sta_models.Financial.objects.filter(code = kwargs['corp_code']).order_by('date')
    fi_json = serializers.serialize('json', fi_sta_query)

    return JsonResponse(fi_json, safe=False)

def ajax_income(request, **kwargs):
    income_query = income_sta_models.Income.objects.filter(code = kwargs['corp_code']).order_by('date')
    income_json = serializers.serialize('json', income_query)

    return JsonResponse(income_json, safe=False)