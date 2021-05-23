import json
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from corps.models import Corp
from income_states import models as income_sta_models
from corps import models as corp_models


class HomePageView(TemplateView):
    template_name = 'core/home.html'


class SearchResultsView(ListView):

    model = Corp
    template_name = 'core/search_result.html'

    def get_queryset(self): # new
        corp = self.request.GET.get('corp')
        corp_list = Corp.objects.filter(
            Q(corp_name__icontains=corp)
        )
        return corp_list


# 랭킹 페이지
class RankingView(TemplateView):
    template_name = 'core/ranking.html'


    #주가 데이터 가져오기
    def get_context_data(self, **kwargs):
        context = super(RankingView, self).get_context_data(**kwargs)

        # 손익계산서 데이터 (20년도 4분기, 20년도 3분기)
        income_sta_query_New = income_sta_models.Income.objects.filter(date = 202012).order_by('date')
        income_sta_query_Old = income_sta_models.Income.objects.filter(date = 202009).order_by('date')

        # 기업 데이터
        corps_query = corp_models.Corp.objects.all()


        corps = {}

        for corp in corps_query:
            corps[corp.corp_code] = corp.corp_name

        revenue_growth = {}
        result = []

        for income in income_sta_query_New:
            revenue_growth[income.code] = income.revenue

        i = 1

        for income in income_sta_query_Old:
            if(revenue_growth.get(income.code) != None and income.revenue != 0 ):
                revenue_growth[income.code] = round(revenue_growth[income.code]/income.revenue, 5)
                result.append([income.code, corps[income.code], revenue_growth[income.code]])
                i += 1

        result = sorted(result, key = lambda x:x[2], reverse=True)

        result = result[:100]
        context['revenue_growth'] = result


        return context


# 매출액 성장률 순
def ajax_revenue_growth(request, **kwargs):

    # 손익계산서 데이터 (20년도 4분기, 20년도 3분기)
    income_sta_query_New = income_sta_models.Income.objects.filter(date=202012).order_by('date')
    income_sta_query_Old = income_sta_models.Income.objects.filter(date=202009).order_by('date')

    # 기업 데이터
    corps_query = corp_models.Corp.objects.all()

    corps = {}

    for corp in corps_query:
        corps[corp.corp_code] = corp.corp_name

    revenue_growth = {}
    result = []

    for income in income_sta_query_New:
        revenue_growth[income.code] = income.revenue

    i = 1

    for income in income_sta_query_Old:
        if (revenue_growth.get(income.code) != None and income.revenue != 0):
            revenue_growth[income.code] = round(revenue_growth[income.code] / income.revenue, 5)
            result.append([income.code, corps[income.code], revenue_growth[income.code]])
            i += 1

    result = sorted(result, key=lambda x: x[2], reverse=True)

    result = json.dumps(result[:100])


    return JsonResponse(result, safe=False)


# 당기순이익 순
def ajax_income_growth(request, **kwargs):

    # 손익계산서 데이터 (20년도 4분기, 20년도 3분기)
    income_sta_query_New = income_sta_models.Income.objects.filter(date=202012).order_by('date')
    income_sta_query_Old = income_sta_models.Income.objects.filter(date=202009).order_by('date')

    # 기업 데이터
    corps_query = corp_models.Corp.objects.all()

    corps = {}

    for corp in corps_query:
        corps[corp.corp_code] = corp.corp_name

    net_income_growth = {}
    result = []

    for income in income_sta_query_New:
        net_income_growth[income.code] = income.net_income

    i = 1

    for income in income_sta_query_Old:
        if (net_income_growth.get(income.code) != None and income.revenue != 0):
            net_income_growth[income.code] = round(net_income_growth[income.code] / income.net_income, 5)
            result.append([income.code, corps[income.code], net_income_growth[income.code]])
            i += 1

    result = sorted(result, key=lambda x: x[2], reverse=True)

    result = json.dumps(result[:100])


    return JsonResponse(result, safe=False)