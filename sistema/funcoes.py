import datetime
from calendar import monthrange
from sistema.models import Venda
from django.db.models import Sum
from random import random
from django.db.models import Q

def stringToFloat(string):
    return float(string.replace(",", "."))

def datas_mes_atual():
    hoje = datetime.datetime.now()
    day= monthrange(hoje.year, hoje.month)[1]
    mes = hoje.strftime("%m")
    return [f"{hoje.year}-{mes}-01", f"{hoje.year}-{mes}-{day}"]

def mascara_data(data):
    d = datetime.datetime.strptime(data, 'yyyy-mm-dd')
    return d.strftime('%d/%m/%Y')

def convert_data(data):
    return data.strftime('%d/%m/%Y')

def verificar_atraso(venda:object):
    if datetime.datetime.now() > venda.vencimento:
        return 'atrasado'
    else:
        return ''

def calcular_mes(mes, ano, val):
    mes = mes - val
    if mes <= 0:
        mes = mes + 12
        ano -= 1
    return ano, mes


def periodos_data(periodo):
    hoje = datetime.date.today()
    year = hoje.year
    if periodo == 'ultima_semana':
        return hoje - datetime.timedelta(7), hoje
    elif periodo == 'ultima_quinzena':
        return hoje - datetime.timedelta(15), hoje
    elif periodo == 'mes_atual':
        return datetime.date(hoje.year, hoje.month, 1), hoje
    elif periodo == 'mes_anterior':
        year, mes = calcular_mes(hoje.month, year, 1)
        day = monthrange(hoje.year, mes)[1]
        return datetime.date(year, mes, 1), datetime.date(year, mes, day)
    elif periodo == 'ultimo_trimestre':
        year, mes = calcular_mes(hoje.month, year, 2)
        return datetime.date(year, mes, 1), datetime.date(hoje.year, hoje.month, hoje.day)
    elif periodo == 'ultimo_semestre':
        year, mes = calcular_mes(hoje.month, year, 5)
        return datetime.date(year, mes, 1), datetime.date(hoje.year, hoje.month, hoje.day)
    elif periodo == 'ultimo_ano':
        year, mes = calcular_mes(hoje.month, year, 12)
        return datetime.date(year, 1, 1), datetime.date(hoje.year, hoje.month, hoje.day)



def total_vendas_ultimos_meses(meses: int):
    hoje = datetime.date.today()
    mes = hoje.month
    ano = hoje.year
    lista = []
    for i in range(meses):
        lista.append({'mes': nome_mes(mes), 'total': vendas_total_mes([data_inicio(ano, mes), data_fim(ano, mes)]),
                      'cor': '#0e0dcf'})
        ano, mes = calcular_mes(mes, ano, 1)
    return lista

def nome_mes(mes):
    meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
             9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    return meses[mes]
def data_inicio(year, month):
    return datetime.date(year, month, 1)

def data_fim(year, month):
    day = monthrange(year, month)[1]
    return datetime.date(year, month, day)

def gerar_cor_hex():
    return '#%06X' % round(random() * 0xffffff)

def vendas_total_mes(datas: list):
    try:
        return int(Venda.objects.filter(~Q(status='cancelado'), data__range=(datas[0], datas[1])).aggregate(
            Sum('total'))['total__sum'])
    except:
        return 0

def vendas_status_mes():
    hoje = datetime.date.today()
    dados = {
        'em_aberto': total_venda_status(hoje.year, hoje.month, 'Em Aberto'),
        'pago': total_venda_status(hoje.year, hoje.month, 'Pago'),
        'vencido': total_venda_vencido(hoje, 'Em Aberto')}
    return dados


def total_venda_vencido(data, status):
    val = Venda.objects.filter(data__year=data.year, data__month=data.month, vencimento__lte=data, status=status)
    if val:
        return int(val.aggregate(Sum(
            'total'))['total__sum'])
    else:
        return 0


def total_venda_status(ano, mes, status):
    val = Venda.objects.filter(data__year=ano, data__month=mes, status=status)
    if val:
        return int(val.aggregate(Sum(
            'total'))['total__sum'])
    else:
        return 0

