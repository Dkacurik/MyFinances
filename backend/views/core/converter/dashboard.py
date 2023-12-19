import re

from django.http import HttpRequest
from django.shortcuts import render
import requests
import xmltodict


def get_currencies():
    res = {}

    try:
        response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
        xml = xmltodict.parse(response.text)
        currencies = xml['gesmes:Envelope']['Cube']['Cube']['Cube']
        for currency in currencies:
            res[currency['@currency']] = currency['@rate']
        res['EUR'] = 1
        return res
    except requests.RequestException as e:
        print(f"Error fetching XML: {e}")
        return None


def converter_dashboard(request: HttpRequest):
    context = {}
    currencies = get_currencies()

    context['currency_from'] = 'EUR'
    context['amount_from'] = 0
    context['currency_to'] = 'USD'
    context['amount_to'] = 0

    if request.method == 'POST':
        currency_from = request.POST.get('currency_from')
        amount_from = request.POST.get('amount_from')
        currency_to = request.POST.get('currency_to')

        if not re.match(r'^[0-9]+$', amount_from):
            context['currencies'] = currencies
            return render(request, "pages/converter/dashboard/dashboard.html", context, status=400)

        if currency_from not in currencies or currency_to not in currencies or float(amount_from) < 0:
            context['currencies'] = currencies
            return render(request, "pages/converter/dashboard/dashboard.html", context, status=400)

        amount_to = round(float(amount_from) / float(currencies[currency_from]) * float(currencies[currency_to]), 2)
        context['amount_to'] = amount_to
        context['currency_from'] = currency_from
        context['currency_to'] = currency_to
        context['amount_from'] = amount_from

    context['currencies'] = currencies
    return render(request, "pages/converter/dashboard/dashboard.html", context, status=200)
