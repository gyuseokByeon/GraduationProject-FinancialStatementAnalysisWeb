import json
import numpy as np
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

        # 주가 데이터
        stocks_query = stock_models.Stock.objects.filter(code_id=self.kwargs['corp_code']).order_by('date')
        stocks_list = list(stocks_query.values_list('datestamp', 'open', 'high', 'low', 'close', 'volume'))
        stocks_json = json.dumps(stocks_list)
        context['stocks'] = stocks_json

        # 재무상태표 데이터
        fi_sta_query = fi_sta_models.Financial.objects.filter(code=self.kwargs['corp_code']).order_by('date')
        for i in fi_sta_query:
            temp = str(i.date)
            i.date = temp[:4]+"년 "+temp[4:]+"월"

        context['finances'] = fi_sta_query

        return context

    def get_object(self):
        object = get_object_or_404(models.Corp, corp_code = self.kwargs['corp_code'])
        return object




#재무상태표 table data 출력
def ajax_finance(request, **kwargs):
    fi_sta_query = fi_sta_models.Financial.objects.filter(code = kwargs['corp_code']).order_by('date')
    fi_json = serializers.serialize('json', fi_sta_query)

    return JsonResponse(fi_json, safe=False)

# 손익계산서 table data 출력
def ajax_income(request, **kwargs):
    income_query = income_sta_models.Income.objects.filter(code = kwargs['corp_code']).order_by('date')
    income_json = serializers.serialize('json', income_query)

    return JsonResponse(income_json, safe=False)

#재무상태표 항목과 주가 상관관계 출력
def ajax_income_analysis(request, **kwargs):

    # 전송할 dict 데이터
    answer = {}

    # 2015년도 이후 주가 / 손익계산서 데이터 받아오기
    stocks_query = stock_models.Stock.objects.filter(code_id = kwargs['corp_code'], date__range=["2015-01-01", "2021-05-01"]).order_by("date")
    income_sta_query = income_sta_models.Income.objects.filter(code=kwargs['corp_code'], date__gte =201503 , date__lte =202012).order_by("date")




    # 매출액 / 매출원가 / 매출총이익 / 판관비 / 영업이익 / 당기순이익 / 주가 데이터 리스트 생성
    revenue = []
    cost = []
    gross_profit = []
    operating_expense = []
    operating_profit = []
    net_income = []
    price = []

    # 자산 / 부채 / 자본 데이터 삽입 (단, 자산, 자본, 부채가 모두 0이라면 삽입하지 않고 one 변수를 1 증가시킨다.)
    one = 0
    for income in income_sta_query:
        if(income.revenue == 0 and income.cost == 0 and income.gross_profit == 0 and income.operating_expense == 0 and income.operating_profit == 0 and income.net_income == 0):
            one += 1
        else:
            revenue.append(income.revenue)
            cost.append(income.cost)
            gross_profit.append(income.gross_profit)
            operating_expense.append(income.operating_expense)
            operating_profit.append(income.operating_profit)
            net_income.append(income.net_income)

    # 만약 유효한 손익계산서 Data가 20개 미만일 경우 상관 분석 수행 불가
    if (len(revenue) < 20):
       answer['winner'] = '부족'
       return JsonResponse(answer, safe=False)


    # 가격 데이터 추가
    # 기업 실적 공개일 1분기 5/15, 2분기 8/14, 3분기 11/16, 4분기 이듬해 3/30
    ranges = [["2015-05-01", "2015-05-31"], ["2015-08-01", "2015-08-31"], ["2015-11-01", "2015-11-30"], ["2016-03-15", "2016-04-15"],
             ["2016-05-01", "2016-05-31"], ["2016-08-01", "2016-08-31"], ["2016-11-01", "2016-11-30"], ["2017-03-15", "2017-04-15"],
             ["2017-05-01", "2017-05-31"], ["2017-08-01", "2017-08-31"], ["2017-11-01", "2017-11-30"], ["2018-03-15", "2018-04-15"],
             ["2018-05-01", "2018-05-31"], ["2018-08-01", "2018-08-31"], ["2018-11-01", "2018-11-30"], ["2019-03-15", "2019-04-15"],
             ["2019-05-01", "2019-05-31"], ["2019-08-01", "2019-08-31"], ["2019-11-01", "2019-11-30"], ["2020-03-15", "2020-04-15"],
             ["2020-05-01", "2020-05-31"], ["2020-08-01", "2020-08-31"], ["2020-11-01", "2020-11-30"], ["2021-03-15", "2021-04-15"]]

    for days in ranges[one:]:
        temp_stock = stocks_query.filter(date__range = days)
        sumPrice = 0

        for stock_price in temp_stock:
            sumPrice += stock_price.close

        if(sumPrice == 0 or len(temp_stock) == 0):
            answer['winner'] = '부족'
            return JsonResponse(answer, safe=False)

        sumPrice /= len(temp_stock)
        price.append(sumPrice)

    # 각 항목 별 상관관계 계산
    revenue_cov = np.corrcoef(revenue, price)[0,1]
    cost_cov = np.corrcoef(cost, price)[0,1]
    gross_profit_cov = np.corrcoef(gross_profit, price)[0,1]
    operating_expense_cov = np.corrcoef(operating_expense, price)[0,1]
    operating_profit_cov = np.corrcoef(operating_profit, price)[0,1]
    net_income_cov = np.corrcoef(net_income, price)[0,1]


    # 상관계수 1위 찾기
    maxCov = max(abs(revenue_cov), abs(cost_cov), abs(gross_profit_cov), abs(operating_expense_cov),abs(operating_profit_cov), abs(net_income_cov))


    # 상관계수 매출액이 1위
    if(maxCov == abs(revenue_cov)):
        answer['winner'] = '매출액'
        answer['value'] = round(revenue_cov, 4)

        temp = [[0 for i in range(2)] for j in range(len(revenue))]
        for i in range(len(temp)):
            temp[i][1] = price[i]
            temp[i][0] = revenue[i]
        answer['list'] = temp


    # 상관계수 매출원가이 1위
    if(maxCov == abs(cost_cov)):
        answer['winner'] = '매출원가'
        answer['value'] = round(cost_cov, 4)

        temp = [[0 for i in range(2)] for j in range(len(cost))]
        for i in range(len(temp)):
            temp[i][1] = price[i]
            temp[i][0] = cost[i]
        answer['list'] = temp

    # 상관계수 매출총이익이 1위
    if(maxCov == abs(gross_profit_cov)):
        answer['winner'] = '매출총이익'
        answer['value'] = round(gross_profit_cov, 4)

        temp = [[0 for i in range(2)] for j in range(len(gross_profit))]
        for i in range(len(temp)):
            temp[i][1] = price[i]
            temp[i][0] = gross_profit[i]
        answer['list'] = temp

    # 상관계수 판관비이 1위
    if(maxCov == abs(operating_expense_cov)):
        answer['winner'] = '판매비와 관리비'
        answer['value'] = round(operating_expense_cov, 4)

        temp = [[0 for i in range(2)] for j in range(len(operating_expense))]
        for i in range(len(temp)):
            temp[i][1] = price[i]
            temp[i][0] = operating_expense[i]
        answer['list'] = temp

    # 상관계수 영업이익이 1위
    if(maxCov == abs(operating_profit_cov)):
        answer['winner'] = '영업이익'
        answer['value'] = round(operating_profit_cov, 4)

        temp = [[0 for i in range(2)] for j in range(len(operating_profit))]
        for i in range(len(temp)):
            temp[i][1] = price[i]
            temp[i][0] = operating_profit[i]
        answer['list'] = temp

    # 상관계수 당기순이익이 1위
    if(maxCov == abs(net_income_cov)):
        answer['winner'] = '당기순이익'
        answer['value'] = round(net_income_cov, 4)

        temp = [[0 for i in range(2)] for j in range(len(net_income))]
        for i in range(len(temp)):
            temp[i][1] = price[i]
            temp[i][0] = net_income[i]
        answer['list'] = temp

    return JsonResponse(answer, safe=False)

#손익계산서 항목과 주가 상관관계 출력
def ajax_finance_analysis(request, **kwargs):

    # 전송할 dict 데이터
    answer = {}

    # 2015년도 이후 주가 / 손익계산서 데이터 받아오기
    stocks_query = stock_models.Stock.objects.filter(code_id = kwargs['corp_code'], date__range=["2015-01-01", "2021-05-01"]).order_by("date")
    finance_sta_query = fi_sta_models.Financial.objects.filter(code=kwargs['corp_code'], date__gte =201503 , date__lte =202012).order_by("date")



    # 자산 / 부채 / 자본 / 주가 데이터 리스트 생성
    asset = []
    liability = []
    capital = []
    price = []

    # 자산 / 부채 / 자본 데이터 삽입 (단, 자산, 자본, 부채가 모두 0이라면 삽입하지 않고 one 변수를 1 증가시킨다.)
    one = 0
    for finance in finance_sta_query:
        if(finance.total_asset == 0 and finance.total_liabilities == 0 and finance.capital == 0):
            one += 1
        else:
            asset.append(finance.total_asset)
            liability.append(finance.total_liabilities)
            capital.append(finance.capital)

    # 만약 재무상태표 Data가 20개 미만일 경우 상관 분석 수행 불가
    if (len(asset) < 20):
       answer['winner'] = '부족'
       return JsonResponse(answer, safe=False)


    # 가격 데이터 추가
    # 기업 실적 공개일 1분기 5/15, 2분기 8/14, 3분기 11/16, 4분기 이듬해 3/30
    ranges = [["2015-05-01", "2015-05-31"], ["2015-08-01", "2015-08-31"], ["2015-11-01", "2015-11-30"], ["2016-03-15", "2016-04-15"],
             ["2016-05-01", "2016-05-31"], ["2016-08-01", "2016-08-31"], ["2016-11-01", "2016-11-30"], ["2017-03-15", "2017-04-15"],
             ["2017-05-01", "2017-05-31"], ["2017-08-01", "2017-08-31"], ["2017-11-01", "2017-11-30"], ["2018-03-15", "2018-04-15"],
             ["2018-05-01", "2018-05-31"], ["2018-08-01", "2018-08-31"], ["2018-11-01", "2018-11-30"], ["2019-03-15", "2019-04-15"],
             ["2019-05-01", "2019-05-31"], ["2019-08-01", "2019-08-31"], ["2019-11-01", "2019-11-30"], ["2020-03-15", "2020-04-15"],
             ["2020-05-01", "2020-05-31"], ["2020-08-01", "2020-08-31"], ["2020-11-01", "2020-11-30"], ["2021-03-15", "2021-04-15"]]


    for i in ranges[one:]:


        temp_stock = stocks_query.filter(date__range = i)
        sumPrice = 0


        for stock_price in temp_stock:
            sumPrice += stock_price.close

        if(sumPrice == 0 or len(temp_stock) == 0):
            answer['winner'] = '부족'
            return JsonResponse(answer, safe=False)

        sumPrice /= len(temp_stock)
        price.append(sumPrice)


    asset_cov =np.corrcoef(asset, price)[0,1]
    liability_cov = np.corrcoef(liability, price)[0, 1]
    capital_cov = np.corrcoef(capital, price)[0, 1]


    # 상관계수 1위 보내기
    maxCov = max(abs(asset_cov), abs(liability_cov), abs(capital_cov))

    answer = {}

    # 상관계수 자산이 1위
    if(maxCov == abs(asset_cov)):
        answer['winner'] = '자산'
        answer['value'] = round(asset_cov, 4)

        temp = [[0 for i in range(2)] for j in range(len(asset))]
        for i in range(len(temp)):
            temp[i][1] = price[i]
            temp[i][0] = asset[i]
        answer['list'] = temp


    # 상관계수 부채가 1위
    if(maxCov == abs(liability_cov)):
        answer['winner'] = '부채'
        answer['value'] = round(liability_cov, 4)
        temp = [[0 for i in range(2)] for j in range(len(liability))]
        for i in range(len(temp)):
            temp[i][1] = price[i]
            temp[i][0] = liability[i]
        answer['list'] = temp

    # 상관계수 자본이 1위
    if(maxCov == abs(capital_cov)):
        answer['winner'] = '자본'
        answer['value'] = round(capital_cov, 4)

        temp = [[0 for i in range(2)] for j in range(len(capital))]
        for i in range(len(capital)):
            temp[i][1] = capital[i]
            temp[i][0] = price[i]
        answer['list'] = temp


    return JsonResponse(answer, safe=False)




# 재무상태표 자산 그래프
def asset_graph(request, **kwargs):

    answer = {}

    # 재무상태표 Data 수집, 날짜 수정
    fi_sta_query = fi_sta_models.Financial.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in fi_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    asset = []
    date = []

    for finance in fi_sta_query:
        if finance.total_asset != 0:
            asset.append(finance.total_asset)
            date.append(finance.date)

    answer['asset'] = asset
    answer['date'] = date



    return JsonResponse(answer, safe=False)


# 재무상태표 부채 그래프
def liability_graph(request, **kwargs):

    answer = {}

    # 재무상태표 Data 수집, 날짜 수정
    fi_sta_query = fi_sta_models.Financial.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in fi_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    liability = []
    date = []

    for finance in fi_sta_query:
        if finance.total_liabilities != 0:
            liability.append(finance.total_liabilities)
            date.append(finance.date)

    answer['liability'] = liability
    answer['date'] = date



    return JsonResponse(answer, safe=False)


# 재무상태표 자본 그래프
def capital_graph(request, **kwargs):

    answer = {}

    # 재무상태표 Data 수집, 날짜 수정
    fi_sta_query = fi_sta_models.Financial.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in fi_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    capital = []
    date = []

    for finance in fi_sta_query:
        if finance.total_liabilities != 0:
            capital.append(finance.capital)
            date.append(finance.date)

    answer['capital'] = capital
    answer['date'] = date



    return JsonResponse(answer, safe=False)






# 손익계산서 매출액 그래프
def revenue_graph(request, **kwargs):
    answer = {}

    # 손익계산서 Data 수집, 날짜 수정
    income_sta_query = income_sta_models.Income.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in income_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    revenue = []
    date = []

    for income in income_sta_query:
        if income.revenue != 0:
            revenue.append(income.revenue)
            date.append(income.date)

    answer['revenue'] = revenue
    answer['date'] = date

    return JsonResponse(answer, safe=False)


# 손익계산서 매출원가 그래프
def cost_graph(request, **kwargs):
    answer = {}

    # 손익계산서 Data 수집, 날짜 수정
    income_sta_query = income_sta_models.Income.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in income_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    cost = []
    date = []

    for income in income_sta_query:
        if income.cost != 0:
            cost.append(income.cost)
            date.append(income.date)

    answer['cost'] = cost
    answer['date'] = date

    return JsonResponse(answer, safe=False)


# 손익계산서 매출총이익 그래프
def gross_porfit_graph(request, **kwargs):
    answer = {}

    # 손익계산서 Data 수집, 날짜 수정
    income_sta_query = income_sta_models.Income.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in income_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    gross_porfit = []
    date = []

    for income in income_sta_query:
        if income.gross_profit != 0:
            gross_porfit.append(income.gross_profit)
            date.append(income.date)

    answer['gross_profit'] = gross_porfit
    answer['date'] = date

    return JsonResponse(answer, safe=False)


# 손익계산서 판매비와 관리비 그래프
def operating_expense_graph(request, **kwargs):
    answer = {}

    # 손익계산서 Data 수집, 날짜 수정
    income_sta_query = income_sta_models.Income.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in income_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    operating_expense = []
    date = []

    for income in income_sta_query:
        if income.operating_expense != 0:
            operating_expense.append(income.operating_expense)
            date.append(income.date)

    answer['operating_expense'] = operating_expense
    answer['date'] = date

    return JsonResponse(answer, safe=False)


# 손익계산서 영업이익 그래프
def operating_profit_graph(request, **kwargs):
    answer = {}

    # 손익계산서 Data 수집, 날짜 수정
    income_sta_query = income_sta_models.Income.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in income_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    operating_profit = []
    date = []

    for income in income_sta_query:
        if income.operating_profit != 0:
            operating_profit.append(income.operating_profit)
            date.append(income.date)

    answer['operating_profit'] = operating_profit
    answer['date'] = date

    return JsonResponse(answer, safe=False)


# 손익계산서 금융수익 그래프
def financial_income_graph(request, **kwargs):
    answer = {}

    # 손익계산서 Data 수집, 날짜 수정
    income_sta_query = income_sta_models.Income.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in income_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    financial_income = []
    date = []

    for income in income_sta_query:
        if income.financial_income != 0:
            financial_income.append(income.financial_income)
            date.append(income.date)

    answer['financial_income'] = financial_income
    answer['date'] = date

    return JsonResponse(answer, safe=False)


# 손익계산서 당기순이익 그래프
def net_income_graph(request, **kwargs):
    answer = {}

    # 손익계산서 Data 수집, 날짜 수정
    income_sta_query = income_sta_models.Income.objects.filter(code=kwargs['corp_code']).order_by('date')
    for i in income_sta_query:
        temp = str(i.date)
        i.date = temp[:4] + "년 " + temp[4:] + "월"

    net_income = []
    date = []

    for income in income_sta_query:
        if income.net_income != 0:
            net_income.append(income.net_income)
            date.append(income.date)

    answer['net_income'] = net_income
    answer['date'] = date

    return JsonResponse(answer, safe=False)