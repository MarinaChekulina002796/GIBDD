# Create your views here.
import operator
from functools import reduce

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, F
from django.db.models.functions import Concat
from django.shortcuts import redirect, get_object_or_404, render_to_response
from gibdd_app.forms import *
from gibdd_app.models import *
from django.shortcuts import render

from chartit import DataPool, PivotDataPool, Chart, PivotChart
from django.db.models import Avg, Count, Sum


def statistics(request):
    previous_date = datetime.date.today() - relativedelta(days=1)
    number_of_accidents = AccidentReport.objects.filter(accident_date=previous_date).count()
    number_people = AccidentReport.objects.filter(accident_date=previous_date).aggregate(
        Sum('accident_number_of_people'))['accident_number_of_people__sum']
    accident_death = AccidentReport.objects.filter(accident_date=previous_date).aggregate(
        Sum('accident_death'))['accident_death__sum']
    accident_children = AccidentReport.objects.filter(accident_date=previous_date).aggregate(
        Sum('accident_children'))['accident_children__sum']
    accident_children_death = AccidentReport.objects.filter(accident_date=previous_date).aggregate(
        Sum('accident_children_death'))['accident_children_death__sum']
    return render(request, 'gibdd_app/statistics.html',
                  {'previous_date': previous_date, 'number_of_accidents': number_of_accidents,
                   'number_people': number_people, 'accident_death': accident_death,
                   'accident_children': accident_children, 'accident_children_death': accident_children_death})


def chart_view_1_1(request):
    query1 = request.GET.get('q')
    query2 = request.GET.get('p')

    if query1 is None or query2 is None:
        date1 = datetime.date.today() - relativedelta(days=7)
        date2 = datetime.date.today()
        ds = PivotDataPool(
            series=[
                {'options': {
                    'source': AccidentReport.objects.all().filter(Q(accident_date__range=[date1, date2])),
                    'categories': 'accident_date'},
                    'terms': {
                        'Всего_пострадавших_взрослых': Sum('accident_number_of_people'),
                        'Всего_пострадавших_детей': Sum('accident_children'),
                    }}])

        chart = PivotChart(
            datasource=ds,
            series_options=[
                {'options': {
                    'type': 'column',
                    'stacking': False,
                    'allowPointSelect': True,
                    'lineWidth': 5,
                    # 'colors': 'red'

                },
                    'terms': ['Всего_пострадавших_взрослых', 'Всего_пострадавших_детей']}],

            chart_options=
            {
                'title': {
                    'text': 'Количество пострадавших за выбранный период'},
                'xAxis': {
                    'title': {
                        'text': 'Дата ДТП'}},
                'yAxis': {
                    'title': {
                        'text': 'Количество пострадавших людей'}},
                # 'Всего_пострадавших_детей':{'color': 'red'}
            }
        )

    else:
        ds = PivotDataPool(
            series=[
                {'options': {
                    'source': AccidentReport.objects.all().filter(Q(accident_date__range=[query1, query2])),
                    'categories': 'accident_date'},
                    'terms': {
                        'Всего_пострадавших_взрослых': Sum('accident_number_of_people'),
                        'Всего_пострадавших_детей': Sum('accident_children'),
                    }}])

        chart = PivotChart(
            datasource=ds,
            series_options=[
                {'options': {
                    'type': 'column',
                    'stacking': False,
                    'allowPointSelect': True,
                    'lineWidth': 5,
                    # 'colors': 'red'

                },
                    'terms': ['Всего_пострадавших_взрослых', 'Всего_пострадавших_детей']}],

            chart_options=
            {
                'title': {
                    'text': 'Количество пострадавших за выбранный период'},
                'xAxis': {
                    'title': {
                        'text': 'Дата ДТП'}},
                'yAxis': {
                    'title': {
                        'text': 'Количество пострадавших людей'}},
                # 'Всего_пострадавших_детей':{'color': 'red'}
            }
        )
    return render(request, 'gibdd_app/statistics_1.html', {'query1': query1, 'query2': query2, 'chart': chart})


def chart_view_1_2(request):
    query1 = request.GET.get('q')
    query2 = request.GET.get('p')

    if query1 is None or query2 is None:
        date1 = datetime.date.today() - relativedelta(days=7)
        date2 = datetime.date.today()
        # Step 1: Create a DataPool with the data we want to retrieve.
        data = DataPool(series=
        [{'options': {
            'source': AccidentReport.objects.values('accident_severity').filter(
                Q(accident_date__range=[date1, date2])).annotate(
                Count('pk'))
        },
            'terms': [
                'accident_severity',
                {'Количество аварий': 'pk__count'}]
        }]
        )
        # Step 2: Create the Chart object

        chart2 = Chart(
            datasource=data,
            series_options=
            [{'options': {
                'type': 'pie',
                'stacking': False},
                'terms': {
                    'accident_severity': ['Количество аварий']
                }
            }],
            chart_options=
            {'title': {
                'text': 'Соотношение степеней тяжести ДТП'},
                'xAxis': {
                    'crosshair': True,
                    'labels': {'format': '{value}'},
                    'title': {
                        'text': 'Степень тяжести ДТП'}},
                'yAxis': {
                    'title': {
                        'text': 'Количество людей'}},
                'chart': {'zoomType': 'x'}
            })  # Step 3: Send the chart object to the template.
        all_accidents = AccidentReport.objects.filter(
            Q(accident_date__range=[date1, date2])).aggregate(Count('pk'))['pk__count']
        not_define = AccidentReport.objects.filter(accident_severity__exact='не указано').filter(
            Q(accident_date__range=[date1, date2])).count()
        not_define_per = (not_define / all_accidents) * 100
        light = AccidentReport.objects.filter(accident_severity__exact='легкая').filter(
            Q(accident_date__range=[date1, date2])).count()
        light_per = (light / all_accidents) * 100
        middle = AccidentReport.objects.filter(accident_severity__exact='средней тяжести').filter(
            Q(accident_date__range=[date1, date2])).count()
        middle_per = ((middle / all_accidents) * 100)
        high = AccidentReport.objects.filter(accident_severity__exact='тяжкий вред').filter(
            Q(accident_date__range=[date1, date2])).count()
        high_per = (high / all_accidents) * 100
        without = AccidentReport.objects.filter(accident_severity__exact='без вреда здоровью').filter(
            Q(accident_date__range=[date1, date2])).count()
        without_per = (without / all_accidents) * 100
    else:
        data = DataPool(series=
        [{'options': {
            'source': AccidentReport.objects.values('accident_severity').filter(
                Q(accident_date__range=[query1, query2])).annotate(
                Count('pk'))
        },
            'terms': [
                'accident_severity',
                {'Количество аварий': 'pk__count'}]
        }]
        )
        # Step 2: Create the Chart object

        chart2 = Chart(
            datasource=data,
            series_options=
            [{'options': {
                'type': 'pie',
                'stacking': False},
                'terms': {
                    'accident_severity': ['Количество аварий']
                }
            }],
            chart_options=
            {'title': {
                'text': 'Соотношение степеней тяжести ДТП'},
                'xAxis': {
                    'crosshair': True,
                    'labels': {'format': '{value}'},
                    'title': {
                        'text': 'Степень тяжести ДТП'}},
                'yAxis': {
                    'title': {
                        'text': 'Количество людей'}},
                'chart': {'zoomType': 'x'}
            })  # Step 3: Send the chart object to the template.
        all_accidents = AccidentReport.objects.filter(Q(accident_date__range=[query1, query2])).aggregate(Count('pk'))[
            'pk__count']
        not_define = AccidentReport.objects.filter(accident_severity__exact='не указано').filter(
            Q(accident_date__range=[query1, query2])).count()
        not_define_per = (not_define / all_accidents) * 100
        light = AccidentReport.objects.filter(accident_severity__exact='легкая').filter(
            Q(accident_date__range=[query1, query2])).count()
        light_per = (light / all_accidents) * 100
        middle = AccidentReport.objects.filter(accident_severity__exact='средней тяжести').filter(
            Q(accident_date__range=[query1, query2])).count()
        middle_per = ((middle / all_accidents) * 100)
        high = AccidentReport.objects.filter(accident_severity__exact='тяжкий вред').filter(
            Q(accident_date__range=[query1, query2])).count()
        high_per = (high / all_accidents) * 100
        without = AccidentReport.objects.filter(accident_severity__exact='без вреда здоровью').filter(
            Q(accident_date__range=[query1, query2])).count()
        without_per = (without / all_accidents) * 100

    return render(request, 'gibdd_app/statistics_2.html',
                  {'chart2': chart2, 'query1': query1, 'query2': query2, 'all_accidents': all_accidents,
                   'not_define_per': not_define_per,
                   'light_per': light_per, 'middle_per': middle_per, 'high_per': high_per, 'without_per': without_per})


def chart_view_3(request):

    query1 = request.GET.get('q')
    query2 = request.GET.get('p')

    if query1 is None or query2 is None:
        date1 = datetime.date.today() - relativedelta(days=7)
        date2 = datetime.date.today()
        ds = PivotDataPool(
            series=[
                {'options': {
                    'source': Lisense_Category.objects.all().filter(Q(categ__date_open_category__range=[date1, date2])),
                    'categories': 'categ__category_name',
                    'legend_by': 'categ__category_name',
                },
                    'terms': {
                        'Всего': Count('pk')
                    }
                }],
            top_n_term='Всего',
            top_n=20
        )

        chart3 = PivotChart(
            datasource=ds,
            series_options=[
                {'options': {
                    'type': 'column',
                    'stacking': True,
                    'xAxis': 0,
                    'yAxis': 0
                },
                    'terms': ['Всего']
                }],

            chart_options=
            {'title': {
                'text': 'Cоотношение категорий прав'},
                'xAxis': {
                    'title': {
                        'text': 'Категория прав'}},
                'yAxis': {
                    'title': {
                        'text': 'Количество категорий'}},

            })

    else:
        ds = PivotDataPool(
            series=[
                {'options': {
                    'source': Lisense_Category.objects.all().filter(
                        Q(categ__date_open_category__range=[query1, query2])),
                    'categories': 'categ__category_name',
                    'legend_by': 'categ__category_name',
                },
                    'terms': {
                        'Всего': Count('pk')
                    }
                }],
            top_n_term='Всего',
            top_n=20
        )

        chart3 = PivotChart(
            datasource=ds,
            series_options=[
                {'options': {
                    'type': 'column',
                    'stacking': True,
                    'xAxis': 0,
                    'yAxis': 0
                },
                    'terms': ['Всего']
                }],

            chart_options=
            {'title': {
                'text': 'Cоотношение категорий прав'},
                'xAxis': {
                    'title': {
                        'text': 'Категория прав'}},
                'yAxis': {
                    'title': {
                        'text': 'Количество категорий'}},

            })

    return render(request, 'gibdd_app/statistics_3.html', {'query1': query1, 'query2': query2, 'chart3': chart3})


def chart_view_4(request):
    # all_people = AccidentReport.objects.aggregate(total=Sum(F('accident_number_of_people') + F('accident_children')))[
    #     'total']

    query1 = request.GET.get('q')
    query2 = request.GET.get('p')

    if query1 is None or query2 is None:
        date1 = datetime.date.today() - relativedelta(days=7)
        date2 = datetime.date.today()
        data = DataPool(series=
        [{'options': {
            'source': AccidentReport.objects.values('accident_date').filter(
                Q(accident_date__range=[date1, date2])).annotate(
                Sum('accident_number_of_people'),
                Sum('accident_death'),
                Sum('accident_children'),
                Sum('accident_children_death')
            )
        },

            'terms': [{'accident_date': 'accident_date'},
                      {'Пострадало взрослых': 'accident_number_of_people__sum'},
                      {'Погибло взрослых': 'accident_death__sum'},
                      {'Пострадало детей': 'accident_children__sum'},
                      {'Погибло детей': 'accident_children_death__sum'}
                      ]
        }]
        )  # Step 2: Create the Chart object

        chart4 = Chart(
            datasource=data,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'accident_date': ['Пострадало взрослых', 'Погибло взрослых', 'Пострадало детей',
                                      'Погибло детей']
                }
            }],
            chart_options=
            {'title': {
                'text': 'Количество пострадавших за день'},
                'xAxis': {
                    'title': {
                        'text': 'Дата ДТП'}
                },
                'yAxis': {
                    'title': {
                        'text': 'Количество людей'}},

            })  # Step 3: Send the chart object to the template.
    else:
        data = DataPool(series=
        [{'options': {
            'source': AccidentReport.objects.values('accident_date').filter(
                Q(accident_date__range=[query1, query2])).annotate(
                Sum('accident_number_of_people'),
                Sum('accident_death'),
                Sum('accident_children'),
                Sum('accident_children_death')
            )
        },

            'terms': [{'accident_date': 'accident_date'},
                      {'Пострадало взрослых': 'accident_number_of_people__sum'},
                      {'Погибло взрослых': 'accident_death__sum'},
                      {'Пострадало детей': 'accident_children__sum'},
                      {'Погибло детей': 'accident_children_death__sum'}
                      ]
        }]
        )  # Step 2: Create the Chart object

        chart4 = Chart(
            datasource=data,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'accident_date': ['Пострадало взрослых', 'Погибло взрослых', 'Пострадало детей',
                                      'Погибло детей']
                }
            }],
            chart_options=
            {'title': {
                'text': 'Количество пострадавших за день'},
                'xAxis': {
                    'title': {
                        'text': 'Дата ДТП'}
                },
                'yAxis': {
                    'title': {
                        'text': 'Количество людей'}},

            })

    return render(request, 'gibdd_app/statistics_4.html',
                  {'chart4': chart4, 'query1': query1, 'query2': query2})  # главная страница ГИБДД


def main(request):
    return render(request, 'gibdd_app/main.html')


def forbidden(request):
    return render(request, 'gibdd_app/forbidden.html')


# список всех справок (таблица)
@login_required
def med_list(request):
    template = 'gibdd_app/MedicalCertificate_list.html'
    objects_list = MedicalCertificate.objects.all().order_by('medical_number', 'medical_date')

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def accident_list(request):
    template = 'gibdd_app/AccidentReport_list.html'
    objects_list = AccidentReport.objects.all().order_by('number_accident', 'accident_paper_date')

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_list_reg_auto_fine(request):
    template = 'gibdd_app/Mix.html'
    list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
            'fine_amount', 'fine_discount',
            'fine_car_data__car_registr_certificate__registr_certificate_number',
            'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
            'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']

    objects_list = Fine.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_list_licen_fine(request):
    template = 'gibdd_app/Mix_licen_fine.html'
    list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
            'fine_amount', 'fine_discount',
            'fine_car_data__car_registr_certificate__registr_certificate_number',
            'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
            'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']

    objects_list = Fine.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_list_VIN_stealing(request):
    template = 'gibdd_app/Mix_VIN_stealing.html'
    list = ['pk', 'car_registr_certificate__registr_certificate_VIN',
            'car_registr_certificate__registr_certificate_number',
            'car_registr_certificate__registr_certificate_car_model',
            'car_registr_certificate__registr_certificate_colour',
            'car_owner__owner_surname', 'car_owner__owner_name',
            'car_stealing__stealing_status', 'car_stealing__stealing_date', 'car_stealing__stealing_town']
    objects_list = Car.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_search_VIN_stealing(request):
    template = 'gibdd_app/Mix_VIN_stealing.html'
    query = request.GET.get('q')

    if query:
        list = ['pk', 'car_registr_certificate__registr_certificate_VIN',
                'car_registr_certificate__registr_certificate_number',
                'car_registr_certificate__registr_certificate_car_model',
                'car_registr_certificate__registr_certificate_colour',
                'car_owner__owner_surname', 'car_owner__owner_name',
                'car_stealing__stealing_status', 'car_stealing__stealing_date', 'car_stealing__stealing_town']

        regs = Car.objects.filter(car_registr_certificate__registr_certificate_VIN__icontains=query).values(*list)

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)
    return render(request, template, {'regs': regs, 'query': query})


def mix_list_VIN_history(request):
    template = 'gibdd_app/Mix_VIN_CarHistory.html'
    list = ['pk', 'car_item__car_registr_certificate__registr_certificate_VIN',
            'car_item__car_registr_certificate__registr_certificate_car_model',
            'car_item__car_registr_certificate__registr_certificate_colour',
            'car_item__car_registr_certificate__registr_certificate_year',
            'history_date_from', 'history_date_to', 'history_country', 'history_town'
            ]
    objects_list = CarHistory.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_search_VIN_history(request):
    template = 'gibdd_app/Mix_VIN_CarHistory.html'
    query = request.GET.get('q')

    if query:
        list = ['pk', 'car_item__car_registr_certificate__registr_certificate_VIN',
                'car_item__car_registr_certificate__registr_certificate_car_model',
                'car_item__car_registr_certificate__registr_certificate_colour',
                'car_item__car_registr_certificate__registr_certificate_year',
                'history_date_from', 'history_date_to', 'history_country', 'history_town'
                ]

        regs = CarHistory.objects.filter(
            car_item__car_registr_certificate__registr_certificate_VIN__icontains=query).values(
            *list)

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)
    return render(request, template, {'regs': regs, 'query': query})


def mix_list_VIN_accident(request):
    template = 'gibdd_app/Mix_VIN_Accident.html'
    list = ['pk', 'car__car_registr_certificate__registr_certificate_VIN',
            'car__car_registr_certificate__registr_certificate_number',
            'car__car_registr_certificate__registr_certificate_car_model',
            'car__car_registr_certificate__registr_certificate_colour',
            'accid__accident_date', 'accid__accident_severity',
            'car__car_owner__owner_name', 'car__car_owner__owner_surname',
            'car__car_owner__owner_patronymic', 'car__car_stealing__stealing_status',
            'car__car_stealing__stealing_date', 'car__car_stealing__stealing_town'
            ]
    objects_list = Accident_Car.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_search_VIN_accident(request):
    template = 'gibdd_app/Mix_VIN_Accident.html'
    query = request.GET.get('q')

    if query:
        list = ['pk', 'car__car_registr_certificate__registr_certificate_VIN',
                'car__car_registr_certificate__registr_certificate_number',
                'car__car_registr_certificate__registr_certificate_car_model',
                'car__car_registr_certificate__registr_certificate_colour',
                'accid__accident_date', 'accid__accident_severity'
                ]
        regs = Accident_Car.objects.filter(
            car__car_registr_certificate__registr_certificate_VIN__icontains=query).values(
            *list)
        return render(request, template, {'regs': regs, 'query': query})

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)


def med_search(request):
    template = 'gibdd_app/MedicalCertificate_list.html'
    query = request.GET.get('q')
    if query:
        meds = MedicalCertificate.objects.filter(Q(medical_number__icontains=query))
    else:
        return HttpResponse('Пожалуйста, заполните строку поиска.')
    return render(request, template, {'meds': meds, 'query': query})


def license_search(request):
    template = 'gibdd_app/License_list.html'
    query1 = request.GET.get('q')
    query2 = request.GET.get('p')
    query3 = request.GET.get('r')

    if query1 and query2 and query3:
        ls = License.objects.filter(Q(series_dr_license__exact=query1),
                                    Q(number_dr_license__exact=query2), Q(date_issue_dr_license__exact=query3))
    else:
        return HttpResponse('Пожалуйста, заполните строку поиска.')
    return render(request, template, {'ls': ls, 'query1': query1, 'query2': query2, 'query3': query3})


def accident_search(request):
    template = 'gibdd_app/AccidentReport_list.html'
    query1 = request.GET.get('q')
    query2 = request.GET.get('p')

    if query1 and query2:
        accids = AccidentReport.objects.filter(Q(number_accident__exact=query1),
                                               Q(accident_date__exact=query2))
    else:
        return HttpResponse('Пожалуйста, заполните строку поиска.')
    return render(request, template, {'accids': accids, 'query1': query1, 'query2': query2})


def insurance_search(request):
    template = 'gibdd_app/InsuranceLicense_list.html'
    query1 = request.GET.get('q')
    query2 = request.GET.get('p')
    query3 = request.GET.get('r')
    query4 = request.GET.get('t')

    if query1 and query2:
        insurs = InsuranceLicense.objects.values('pk', 'insur', 'licen', 'insur__insurance_car__car_number',
                                                 'insur__insurance_car__car_region', 'licen__series_dr_license',
                                                 'licen__number_dr_license', 'licen__date_issue_dr_license',
                                                 'insur__insurance_number', 'insur__insurance_company',
                                                 'insur__insurance_type', 'insur__insurance_date_from',
                                                 'insur__insurance_date_to').filter(
            Q(insur__insurance_number__exact=query1), Q(insur__insurance_car__car_number__exact=query2),
            Q(insur__insurance_car__car_region__exact=query4), Q(insur__insurance_date_from__exact=query3))
    else:
        return HttpResponse('Пожалуйста, заполните строку поиска.')
    return render(request, template,
                  {'insurs': insurs, 'query1': query1, 'query2': query2, 'query3': query3, 'query4': query4})


def mix_search(request):
    template = 'gibdd_app/Mix.html'
    query1 = request.GET.get('q')
    query2 = request.GET.get('p')

    if query1 and query2:
        list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
                'fine_amount', 'fine_discount',
                'fine_car_data__car_registr_certificate__registr_certificate_number',
                'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
                'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']

        # regs = Fine.objects.annotate(
        #     search_name=Concat('fine_car_data__car_registr_certificate__registr_certificate_number', V(' '),
        #                        'fine_car_data__car_registr_certificate__registr_certificate_registr_sign'
        #                        )).filter(search_name__icontains=query).values(*list)
        regs = Fine.objects.filter(
            Q(fine_car_data__car_registr_certificate__registr_certificate_number__icontains=query1),
            Q(fine_car_data__car_registr_certificate__registr_certificate_registr_sign__exact=query2)).values(
            *list)
        return render(request, template, {'regs': regs, 'query1': query1, 'query2': query2})

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)


def search_accidents_by_date(request):
    template = 'gibdd_app/Search_accidents_by_date.html'
    query1 = request.GET.get('q')
    query2 = request.GET.get('p')
    # if query1 and query2:
    list = ['pk', 'accid__number_accident', 'car__car_registr_certificate__registr_certificate_VIN',
            'car__car_registr_certificate__registr_certificate_number',
            'car__car_registr_certificate__registr_certificate_car_model',
            'car__car_registr_certificate__registr_certificate_colour',
            'accid__accident_date', 'accid__accident_severity']

    regs = Accident_Car.objects.all().order_by('accid__accident_date')
    regs = regs.filter(Q(accid__accident_date__range=[query1, query2])).values(*list)
    data_count = AccidentReport.objects.all().filter(Q(accident_date__range=[query1, query2]))
    return render(request, template, {'regs': regs, 'query1': query1, 'query2': query2, 'data_count': data_count})
    # if not query1 or not query2:
    #     text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
    #     button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
    #     tex = (text, button)
    #     return HttpResponse(tex)


def mix_search_licen_fine(request):
    template = 'gibdd_app/Mix_licen_fine.html'
    query = request.GET.get('q')

    if query:
        list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
                'fine_amount', 'fine_discount',
                'fine_car_data__car_registr_certificate__registr_certificate_number',
                'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
                'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']

        regs = Fine.objects.annotate(
            search_name=Concat('fine_license_data__series_dr_license',
                               'fine_license_data__number_dr_license'
                               )).filter(search_name__icontains=query).values(*list)

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)
    return render(request, template, {'regs': regs, 'query': query})


# def mix_search_licen_fine(request):
#     template = 'gibdd_app/Mix_licen_fine.html'
#     query1 = request.GET.get('q')
#     query2 = request.GET.get('t')
#
#     if query1 and query2:
#         if query2.exists():
#             list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
#                     'fine_amount', 'fine_discount',
#                     'fine_car_data__car_registr_certificate__registr_certificate_number',
#                     'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
#                     'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']
#             criterion1 = Q(fine_license_data__series_dr_license__icontains=query1) & \
#                          Q(fine_license_data__series_dr_license__isnull=False)
#             criterion2 = Q(fine_license_data__number_dr_license__isnull=False) & \
#                          Q(fine_license_data__number_dr_license__icontains=query2)
#
#             regs = Fine.objects.all().filter(criterion1 & criterion2)
#             regs = regs.values(*list)
#             # regs = a.filter(Q(fine_license_data__number_dr_license__icontains=query2)).values(*list)
#
#             # search_name = Concat('fine_license_data__series_dr_license',
#             #                      'fine_license_data__number_dr_license'
#             #                      )).filter(search_name__icontains=query).values(*list)
#         else:
#             text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
#             button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
#             tex = (text, button)
#             return HttpResponse(tex)
#     else:
#         text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
#         button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
#         tex = (text, button)
#         return HttpResponse(tex)
#     return render(request, template, {'regs': regs, 'query1': query1, 'query2': query2})


@login_required
def categ_list(request):
    template = 'gibdd_app/Category_list.html'
    objects_list = Category.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def license_list_for_drivers(request):
    template = 'gibdd_app/License_list.html'
    objects_list = License.objects.all().order_by('series_dr_license', 'number_dr_license')

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def license_list(request):
    template = 'gibdd_app/License_list.html'
    objects_list = License.objects.all().order_by('series_dr_license', 'number_dr_license')

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def driver_list(request):
    template = 'gibdd_app/Driver_list.html'
    objects_list = Driver.objects.all().order_by('driver_surname', 'driver_name', 'driver_patronymic')

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def disq_list(request):
    template = 'gibdd_app/LicenseDisqualification_list.html'
    objects_list = LicenseDisqualification.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def car_list(request):
    template = 'gibdd_app/Car_list.html'
    objects_list = Car.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def lic_cat_list(request):
    template = 'gibdd_app/Licen_Cat_list.html'
    objects_list = Lisense_Category.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def witness_list(request):
    template = 'gibdd_app/Witness_list.html'
    objects_list = Witness.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def licen_accid_list(request):
    template = 'gibdd_app/Lisense_Accident_list.html'
    objects_list = Lisense_Accident.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def inspector_list(request):
    template = 'gibdd_app/Inspector_list.html'
    objects_list = Inspector.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def fine_list(request):
    template = 'gibdd_app/Fine_list.html'
    objects_list = Fine.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def registr_list(request):
    template = 'gibdd_app/RegistrationCertificate_list.html'
    objects_list = RegistrationCertificate.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def owner_list(request):
    template = 'gibdd_app/Owner_list.html'
    objects_list = Owner.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def steal_list(request):
    template = 'gibdd_app/Stealing_list.html'
    objects_list = Stealing.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def decree_list(request):
    template = 'gibdd_app/Decree_list.html'
    objects_list = Decree.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def camera_list(request):
    template = 'gibdd_app/Camera_list.html'
    objects_list = Camera.objects.all()
    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def autoschool_list(request):
    template = 'gibdd_app/AutoSchool_list.html'
    objects_list = AutoSchool.objects.all()
    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def history_list(request):
    template = 'gibdd_app/History_list.html'
    # list = ['car_item__car_registr_certificate__registr_certificate_VIN', ]
    objects_list = CarHistory.objects.all() \
        # .values(*list)
    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def diagnostic_card_list(request):
    template = 'gibdd_app/DiagnosticCard_list.html'
    objects_list = DiagnosticCard.objects.all()
    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def insurance_list(request):
    template = 'gibdd_app/Insurance_list.html'
    objects_list = Insurance.objects.all()
    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def insurance_license_list(request):
    template = 'gibdd_app/InsuranceLicense_list.html'
    objects_list = InsuranceLicense.objects.all().values('pk', 'insur', 'licen', 'insur__insurance_car__car_number',
                                                         'insur__insurance_car__car_region', 'licen__series_dr_license',
                                                         'licen__number_dr_license', 'licen__date_issue_dr_license',
                                                         'insur__insurance_number', 'insur__insurance_company',
                                                         'insur__insurance_type', 'insur__insurance_date_from',
                                                         'insur__insurance_date_to')
    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def autostudent_list(request):
    template = 'gibdd_app/Autoschool_Driver_list.html'
    objects_list = Autoschool_Driver.objects.all()
    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def accident_car_list(request):
    template = 'gibdd_app/Accident_Car_list.html'
    objects_list = Accident_Car.objects.all()
    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def europrotocol_list(request):
    template = 'gibdd_app/Europrotocol_list.html'
    objects_list = Europrotocol.objects.all()
    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def accident_car_detail(request, pk):
    template = 'gibdd_app/Accident_Car_detail.html'
    obj = get_object_or_404(Accident_Car, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def insurance_license_detail(request, pk):
    template = 'gibdd_app/InsuranceLicense_detail.html'
    obj = get_object_or_404(InsuranceLicense, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def insurance_detail(request, pk):
    template = 'gibdd_app/Insurance_detail.html'

    obj = get_object_or_404(Insurance, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def autostudent_detail(request, pk):
    template = 'gibdd_app/Autoschool_Driver_detail.html'

    obj = get_object_or_404(Autoschool_Driver, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def diagnostic_card_detail(request, pk):
    template = 'gibdd_app/DiagnosticCard_detail.html'

    obj = get_object_or_404(DiagnosticCard, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def history_detail(request, pk):
    template = 'gibdd_app/History_detail.html'

    obj = get_object_or_404(CarHistory, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def autoschool_detail(request, pk):
    template = 'gibdd_app/AutoSchool_detail.html'

    obj = get_object_or_404(AutoSchool, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def decree_detail(request, pk):
    template = 'gibdd_app/Decree_detail.html'

    obj = get_object_or_404(Decree, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def registr_detail(request, pk):
    template = 'gibdd_app/RegistrationCertificate_detail.html'

    obj = get_object_or_404(RegistrationCertificate, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def witness_detail(request, pk):
    template = 'gibdd_app/Witness_detail.html'

    obj = get_object_or_404(Witness, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def lic_cat_detail(request, pk):
    template = 'gibdd_app/Licen_Cat_detail.html'

    obj = get_object_or_404(Lisense_Category, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def categ_detail(request, pk):
    template = 'gibdd_app/Category_detail.html'

    obj = get_object_or_404(Category, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


def accident_detail(request, pk):
    template = 'gibdd_app/AccidentReport_detail.html'

    obj = get_object_or_404(AccidentReport, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def med_detail(request, pk):
    template = 'gibdd_app/MedicalCertificate_detail.html'

    obj = get_object_or_404(MedicalCertificate, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def license_detail(request, pk):
    template = 'gibdd_app/License_detail.html'

    obj = get_object_or_404(License, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def driver_detail(request, pk):
    template = 'gibdd_app/Driver_detail.html'

    obj = get_object_or_404(Driver, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def disq_detail(request, pk):
    template = 'gibdd_app/LicenseDisqualification_detail.html'

    obj = get_object_or_404(LicenseDisqualification, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def car_detail(request, pk):
    template = 'gibdd_app/Car_detail.html'

    obj = get_object_or_404(Car, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def licen_accid_detail(request, pk):
    template = 'gibdd_app/Lisense_Accident_detail.html'

    obj = get_object_or_404(Lisense_Accident, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def inspector_detail(request, pk):
    template = 'gibdd_app/Inspector_detail.html'

    obj = get_object_or_404(Inspector, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def fine_detail(request, pk):
    template = 'gibdd_app/Fine_detail.html'
    obj = get_object_or_404(Fine, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def owner_detail(request, pk):
    template = 'gibdd_app/Owner_detail.html'
    obj = get_object_or_404(Owner, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def steal_detail(request, pk):
    template = 'gibdd_app/Stealing_detail.html'
    obj = get_object_or_404(Stealing, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def europrotocol_detail(request, pk):
    template = 'gibdd_app/Europrotocol_detail.html'
    obj = get_object_or_404(Europrotocol, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def camera_detail(request, pk):
    template = 'gibdd_app/Camera_detail.html'
    obj = get_object_or_404(Camera, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def delete_med(request, pk):
    template = 'gibdd_app/MedicalCertificate_form.html'

    obj = get_object_or_404(MedicalCertificate, pk=pk)
    if request.method == 'POST':
        form = MedicalCertificateForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('med_list'))
    else:
        form = MedicalCertificateForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_autostudent(request, pk):
    template = 'gibdd_app/Autoschool_Driver_form.html'
    obj = get_object_or_404(Autoschool_Driver, pk=pk)
    if request.method == 'POST':
        form = Autoschool_DriverForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('autostudent_list'))
    else:
        form = Autoschool_DriverForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_categ(request, pk):
    template = 'gibdd_app/Category_form.html'

    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('categ_list'))
    else:
        form = CategoryForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_license(request, pk):
    template = 'gibdd_app/License_form.html'

    obj = get_object_or_404(License, pk=pk)
    if request.method == 'POST':
        form = LicenseForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('license_list'))
    else:
        form = LicenseForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_driver(request, pk):
    template = 'gibdd_app/Driver_form.html'

    obj = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('driver_list'))
    else:
        form = DriverForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_disq(request, pk):
    template = 'gibdd_app/LicenseDisqualification_form.html'

    obj = get_object_or_404(LicenseDisqualification, pk=pk)
    if request.method == 'POST':
        form = LicenseDisqualificationForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('disq_list'))
    else:
        form = LicenseDisqualificationForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_accident(request, pk):
    template = 'gibdd_app/AccidentReport_form.html'

    obj = get_object_or_404(AccidentReport, pk=pk)
    if request.method == 'POST':
        form = AccidentReportForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('license_list'))
    else:
        form = AccidentReportForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_car(request, pk):
    template = 'gibdd_app/Car_form.html'

    obj = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('car_list'))
    else:
        form = CarForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_lic_cat(request, pk):
    template = 'gibdd_app/Licen_CatForm.html'

    obj = get_object_or_404(Lisense_Category, pk=pk)
    if request.method == 'POST':
        form = Licen_CatForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('car_list'))
    else:
        form = Licen_CatForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_witness(request, pk):
    template = 'gibdd_app/Witness_form.html'

    obj = get_object_or_404(Witness, pk=pk)
    if request.method == 'POST':
        form = WitnessForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('witness_list'))
    else:
        form = WitnessForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_licen_accid(request, pk):
    template = 'gibdd_app/Lisense_Accident_form.html'
    obj = get_object_or_404(Lisense_Accident, pk=pk)
    if request.method == 'POST':
        form = Lisense_AccidentForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('licen_accid_list'))
    else:
        form = Lisense_AccidentForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_inspector(request, pk):
    template = 'gibdd_app/Inspector_form.html'
    obj = get_object_or_404(Inspector, pk=pk)
    if request.method == 'POST':
        form = InspectorForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('inspector_list'))
    else:
        form = InspectorForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_fine(request, pk):
    template = 'gibdd_app/Fine_form.html'
    obj = get_object_or_404(Fine, pk=pk)
    if request.method == 'POST':
        form = FineForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('fine_list'))
    else:
        form = FineForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_registr(request, pk):
    template = 'gibdd_app/RegistrationCertificate_form.html'
    obj = get_object_or_404(RegistrationCertificate, pk=pk)
    if request.method == 'POST':
        form = RegistrationCertificateForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('registr_list'))
    else:
        form = RegistrationCertificateForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_owner(request, pk):
    template = 'gibdd_app/Owner_form.html'
    obj = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('owner_list'))
    else:
        form = OwnerForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_steal(request, pk):
    template = 'gibdd_app/Stealing_form.html'
    obj = get_object_or_404(Stealing, pk=pk)
    if request.method == 'POST':
        form = StealingForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('steal_list'))
    else:
        form = StealingForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_decree(request, pk):
    template = 'gibdd_app/Decree_form.html'
    obj = get_object_or_404(Decree, pk=pk)
    if request.method == 'POST':
        form = DecreeForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('decree_list'))
    else:
        form = DecreeForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_camera(request, pk):
    template = 'gibdd_app/Camera_form.html'
    obj = get_object_or_404(Camera, pk=pk)
    if request.method == 'POST':
        form = CameraForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('camera_list'))
    else:
        form = CameraForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_autoschool(request, pk):
    template = 'gibdd_app/AutoSchool_form.html'
    obj = get_object_or_404(AutoSchool, pk=pk)
    if request.method == 'POST':
        form = AutoschoolForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('autoschool_list'))
    else:
        form = AutoschoolForm(instance=obj)
    return render(request, template, {'form': form})


@login_required
def delete_history(request, pk):
    template = 'gibdd_app/History_form.html'
    obj = get_object_or_404(CarHistory, pk=pk)
    if request.method == 'POST':
        form = HistoryForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('history_list'))
    else:
        form = HistoryForm(instance=obj)
    return render(request, template, {'form': form})


@login_required
def delete_diagnostic_card(request, pk):
    template = 'gibdd_app/DiagnosticCard_form.html'
    obj = get_object_or_404(DiagnosticCard, pk=pk)
    if request.method == 'POST':
        form = DiagnosticCardForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('diagnostic_card_list'))
    else:
        form = DiagnosticCardForm(instance=obj)
    return render(request, template, {'form': form})


@login_required
def delete_insurance(request, pk):
    template = 'gibdd_app/Insurance_form.html'
    obj = get_object_or_404(Insurance, pk=pk)
    if request.method == 'POST':
        form = InsuranceForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('insurance_list'))
    else:
        form = InsuranceForm(instance=obj)
    return render(request, template, {'form': form})


@login_required
def delete_insurance_license(request, pk):
    template = 'gibdd_app/InsuranceLicense_form.html'
    obj = get_object_or_404(InsuranceLicense, pk=pk)
    if request.method == 'POST':
        form = InsuranceLicenseForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('insurance_license_list'))
    else:
        form = InsuranceLicenseForm(instance=obj)
    return render(request, template, {'form': form})


@login_required
def delete_europrotocol(request, pk):
    template = 'gibdd_app/Europrotocol_form.html'
    obj = get_object_or_404(Europrotocol, pk=pk)
    if request.method == 'POST':
        form = EuroprotocolForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('europrotocol_list'))
    else:
        form = EuroprotocolForm(instance=obj)
    return render(request, template, {'form': form})


@login_required
def delete_accident_car(request, pk):
    template = 'gibdd_app/Accident_Car_form.html'
    obj = get_object_or_404(Accident_Car, pk=pk)
    if request.method == 'POST':
        form = Accident_CarForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('accident_car_list'))
    else:
        form = Accident_CarForm(instance=obj)
    return render(request, template, {'form': form})


def services(request):
    return render(request, 'gibdd_app/services_for_drivers.html')


def gibdd(request):
    return render(request, 'gibdd_app/gibdd.html')


def participants(request):
    return render(request, 'gibdd_app/participants.html')


@login_required()
def workers(request):
    return render(request, 'gibdd_app/workers.html')


def contacts(request):
    return render(request, 'gibdd_app/contacts.html')


def car_reg_plan(request):
    return render(request, 'gibdd_app/car_reg_plan.html')


def reg_accident(request):
    return render(request, 'gibdd_app/reg_accident.html')


def europrotocol(request):
    return render(request, 'gibdd_app/europrotocol.html')


def change_dr_license(request):
    return render(request, 'gibdd_app/change_dr_license.html')


def med003(request):
    return render(request, 'gibdd_app/med003.html')


# для авторизации уже зарегистрированного пользователя
def login(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user is not None:
                auth_login(request, user)
            return redirect(reverse('main'))
    else:
        form = AuthorizationForm()
    return render(request, 'gibdd_app/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect(reverse('main'))


@login_required
def add_license(request):
    if request.method == 'POST':
        form = LicenseForm(request.POST, request.FILES)  # тут возвращается словарь вместе с csrf
        if form.is_valid():
            licen = License(**form.cleaned_data)
            licen.save()
            return redirect(reverse('workers'), args=[licen.pk])
    else:
        form = LicenseForm()
    template = 'gibdd_app/License_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_autostudent(request):
    if request.method == 'POST':
        form = Autoschool_DriverForm(request.POST, request.FILES)  # тут возвращается словарь вместе с csrf
        if form.is_valid():
            licen = Autoschool_Driver(**form.cleaned_data)
            licen.save()
            return redirect(reverse('autostudent_create'))
    else:
        form = Autoschool_DriverForm()
    template = 'gibdd_app/Autoschool_Driver_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_europrotocol(request):
    if request.method == 'POST':
        form = EuroprotocolForm(request.POST, request.FILES)  # тут возвращается словарь вместе с csrf
        if form.is_valid():
            licen = Europrotocol(**form.cleaned_data)
            licen.save()
            return redirect(reverse('europrotocol_create'))
    else:
        form = EuroprotocolForm()
    template = 'gibdd_app/Europrotocol_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def update_europrotocol(request, pk):
    europrotocol = get_object_or_404(Europrotocol, pk=pk)
    if request.method == 'POST':
        form = EuroprotocolForm(request.POST, request.FILES, instance=europrotocol)
        if form.is_valid():
            form.save()
        return redirect('europrotocol_detail', pk)
    else:
        form = EuroprotocolForm(instance=europrotocol)

    template = 'gibdd_app/Europrotocol_form.html'
    context = {
        'form': form,
        'europrotocol': europrotocol,
    }

    return render(request, template, context)


@login_required
def update_autostudent(request, pk):
    autostudent = get_object_or_404(Autoschool_Driver, pk=pk)
    if request.method == 'POST':
        form = Autoschool_DriverForm(request.POST, request.FILES, instance=autostudent)
        if form.is_valid():
            form.save()
        return redirect('autostudent_detail', pk)
    else:
        form = Autoschool_DriverForm(instance=autostudent)

    template = 'gibdd_app/Autoschool_Driver_form.html'
    context = {
        'form': form,
        'autostudent': autostudent,
    }

    return render(request, template, context)


@login_required
def update_license(request, pk):
    licen = get_object_or_404(License, pk=pk)
    if request.method == 'POST':
        form = LicenseForm(request.POST, request.FILES, instance=licen)
        if form.is_valid():
            form.save()
        return redirect('license_detail', pk)
    else:
        form = LicenseForm(instance=licen)

    template = 'gibdd_app/License_form.html'
    context = {
        'form': form,
        'licen': licen,
    }

    return render(request, template, context)


@login_required
def update_accident(request, pk):
    accident = get_object_or_404(AccidentReport, pk=pk)
    if request.method == 'POST':
        form = AccidentReportForm(request.POST, request.FILES, instance=accident)
        if form.is_valid():
            form.save()
        return redirect('accident_detail', pk)
    else:
        form = AccidentReportForm(instance=accident)

    template = 'gibdd_app/AccidentReport_form.html'
    context = {
        'form': form,
        'accident': accident,
    }

    return render(request, template, context)


@login_required
def update_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
        return redirect('car_detail', pk)
    else:
        form = CarForm(instance=car)

    template = 'gibdd_app/Car_form.html'
    context = {
        'form': form,
        'car': car,
    }

    return render(request, template, context)


@login_required
def update_lic_cat(request, pk):
    lic_cat = get_object_or_404(Lisense_Category, pk=pk)
    if request.method == 'POST':
        form = Licen_CatForm(request.POST, request.FILES, instance=lic_cat)
        if form.is_valid():
            form.save()
        return redirect('lic_cat_detail', pk)
    else:
        form = Licen_CatForm(instance=lic_cat)

    template = 'gibdd_app/Licen_CatForm.html'
    context = {
        'form': form,
        'lic_cat': lic_cat,
    }

    return render(request, template, context)


@login_required
def update_witness(request, pk):
    witness = get_object_or_404(Witness, pk=pk)
    if request.method == 'POST':
        form = WitnessForm(request.POST, request.FILES, instance=witness)
        if form.is_valid():
            form.save()
        return redirect('witness_detail', pk)
    else:
        form = WitnessForm(instance=witness)

    template = 'gibdd_app/Witness_form.html'
    context = {
        'form': form,
        'witness': witness,
    }

    return render(request, template, context)


@login_required
def update_licen_accid(request, pk):
    licen_accid = get_object_or_404(Lisense_Accident, pk=pk)
    if request.method == 'POST':
        form = Lisense_AccidentForm(request.POST, request.FILES, instance=licen_accid)
        if form.is_valid():
            form.save()
        return redirect('licen_accid_detail', pk)
    else:
        form = Lisense_AccidentForm(instance=licen_accid)

    template = 'gibdd_app/Lisense_Accident_form.html'
    context = {
        'form': form,
        'licen_accid': licen_accid,
    }

    return render(request, template, context)


@login_required
def update_inspector(request, pk):
    inspect = get_object_or_404(Inspector, pk=pk)
    if request.method == 'POST':
        form = InspectorForm(request.POST, request.FILES, instance=inspect)
        if form.is_valid():
            form.save()
        return redirect('inspector_detail', pk)
    else:
        form = InspectorForm(instance=inspect)

    template = 'gibdd_app/Inspector_form.html'
    context = {
        'form': form,
        'inspect': inspect,
    }

    return render(request, template, context)


@login_required
def update_fine(request, pk):
    fine = get_object_or_404(Fine, pk=pk)
    if request.method == 'POST':
        form = FineForm(request.POST, request.FILES, instance=fine)
        if form.is_valid():
            form.save()
        return redirect('fine_detail', pk)
    else:
        form = FineForm(instance=fine)

    template = 'gibdd_app/Fine_form.html'
    context = {
        'form': form,
        'fine': fine,
    }

    return render(request, template, context)


@login_required
def update_registr(request, pk):
    reg = get_object_or_404(RegistrationCertificate, pk=pk)
    if request.method == 'POST':
        form = RegistrationCertificateForm(request.POST, request.FILES, instance=reg)
        if form.is_valid():
            form.save()
        return redirect('registr_detail', pk)
    else:
        form = RegistrationCertificateForm(instance=reg)

    template = 'gibdd_app/RegistrationCertificate_form.html'
    context = {
        'form': form,
        'reg': reg,
    }

    return render(request, template, context)


@login_required
def update_owner(request, pk):
    own = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES, instance=own)
        if form.is_valid():
            form.save()
        return redirect('owner_detail', pk)
    else:
        form = OwnerForm(instance=own)

    template = 'gibdd_app/Owner_form.html'
    context = {
        'form': form,
        'own': own,
    }

    return render(request, template, context)


@login_required
def update_steal(request, pk):
    steal = get_object_or_404(Stealing, pk=pk)
    if request.method == 'POST':
        form = StealingForm(request.POST, request.FILES, instance=steal)
        if form.is_valid():
            form.save()
        return redirect('steal_detail', pk)
    else:
        form = StealingForm(instance=steal)

    template = 'gibdd_app/Stealing_form.html'
    context = {
        'form': form,
        'steal': steal,
    }

    return render(request, template, context)


@login_required
def update_decree(request, pk):
    decree = get_object_or_404(Decree, pk=pk)
    if request.method == 'POST':
        form = DecreeForm(request.POST, request.FILES, instance=decree)
        if form.is_valid():
            form.save()
        return redirect('decree_detail', pk)
    else:
        form = DecreeForm(instance=decree)

    template = 'gibdd_app/Decree_form.html'
    context = {
        'form': form,
        'decree': decree,
    }

    return render(request, template, context)


@login_required
def update_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    if request.method == 'POST':
        form = CameraForm(request.POST, request.FILES, instance=camera)
        if form.is_valid():
            form.save()
        return redirect('camera_detail', pk)
    else:
        form = CameraForm(instance=camera)

    template = 'gibdd_app/Camera_form.html'
    context = {
        'form': form,
        'camera': camera,
    }

    return render(request, template, context)


@login_required
def update_autoschool(request, pk):
    school = get_object_or_404(AutoSchool, pk=pk)
    if request.method == 'POST':
        form = AutoschoolForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            form.save()
        return redirect('autoschool_detail', pk)
    else:
        form = AutoschoolForm(instance=school)

    template = 'gibdd_app/AutoSchool_form.html'
    context = {
        'form': form,
        'school': school,
    }
    return render(request, template, context)


@login_required
def update_history(request, pk):
    history = get_object_or_404(CarHistory, pk=pk)
    if request.method == 'POST':
        form = HistoryForm(request.POST, request.FILES, instance=history)
        if form.is_valid():
            form.save()
        return redirect('history_detail', pk)
    else:
        form = HistoryForm(instance=history)

    template = 'gibdd_app/History_form.html'
    context = {
        'form': form,
        'history': history,
    }
    return render(request, template, context)


@login_required
def update_diagnostic_card(request, pk):
    diagnostic = get_object_or_404(DiagnosticCard, pk=pk)
    if request.method == 'POST':
        form = DiagnosticCardForm(request.POST, request.FILES, instance=diagnostic)
        if form.is_valid():
            form.save()
        return redirect('diagnostic_card_detail', pk)
    else:
        form = DiagnosticCardForm(instance=diagnostic)

    template = 'gibdd_app/DiagnosticCard_form.html'
    context = {
        'form': form,
        'diagnostic': diagnostic,
    }
    return render(request, template, context)


@login_required
def update_insurance(request, pk):
    insurance = get_object_or_404(Insurance, pk=pk)
    if request.method == 'POST':
        form = InsuranceForm(request.POST, request.FILES, instance=insurance)
        if form.is_valid():
            form.save()
        return redirect('insurance_detail', pk)
    else:
        form = InsuranceForm(instance=insurance)
    template = 'gibdd_app/Insurance_form.html'
    context = {
        'form': form,
        'insurance': insurance,
    }
    return render(request, template, context)


@login_required
def update_insurance_license(request, pk):
    insurance_license = get_object_or_404(InsuranceLicense, pk=pk)
    if request.method == 'POST':
        form = InsuranceLicenseForm(request.POST, request.FILES, instance=insurance_license)
        if form.is_valid():
            form.save()
        return redirect('insurance_license_detail', pk)
    else:
        form = InsuranceLicenseForm(instance=insurance_license)
    template = 'gibdd_app/InsuranceLicense_form.html'
    context = {
        'form': form,
        'insurance_license': insurance_license,
    }
    return render(request, template, context)


@login_required
def update_accident_car(request, pk):
    accident_car = get_object_or_404(Accident_Car, pk=pk)
    if request.method == 'POST':
        form = Accident_CarForm(request.POST, request.FILES, instance=accident_car)
        if form.is_valid():
            form.save()
        return redirect('accident_car_detail', pk)
    else:
        form = Accident_CarForm(instance=accident_car)
    template = 'gibdd_app/Accident_Car_form.html'
    context = {
        'form': form,
        'accident_car': accident_car,
    }
    return render(request, template, context)


@login_required
def update_med(request, pk):
    med = get_object_or_404(MedicalCertificate, pk=pk)
    if request.method == 'POST':
        form = MedicalCertificateForm(request.POST, request.FILES, instance=med)
        if form.is_valid():
            form.save()
        return redirect('med_detail', pk)
    else:
        form = MedicalCertificateForm(instance=med)
    template = 'gibdd_app/MedicalCertificate_form.html'
    context = {
        'form': form,
        'med': med,
    }
    return render(request, template, context)


@login_required
def update_categ(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
        return redirect('categ_detail', pk)
    else:
        form = CategoryForm(instance=category)
    template = 'gibdd_app/Category_form.html'
    context = {
        'form': form,
        'category': category,
    }
    return render(request, template, context)


@login_required
def update_driver(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()
        return redirect('driver_detail', pk)
    else:
        form = DriverForm(instance=driver)
    template = 'gibdd_app/Driver_form.html'
    context = {
        'form': form,
        'driver': driver,
    }
    return render(request, template, context)


@login_required
def update_disq(request, pk):
    disq = get_object_or_404(LicenseDisqualification, pk=pk)
    if request.method == 'POST':
        form = LicenseDisqualificationForm(request.POST, request.FILES, instance=disq)
        if form.is_valid():
            form.save()
        return redirect('disq_detail', pk)
    else:
        form = LicenseDisqualificationForm(instance=disq)
    template = 'gibdd_app/LicenseDisqualification_form.html'
    context = {
        'form': form,
        'disq': disq,
    }
    return render(request, template, context)


@login_required
def add_med(request):
    if request.method == 'POST':
        form = MedicalCertificateForm(request.POST, request.FILES)  # тут возвращается словарь вместе с csrf
        if form.is_valid():
            med = MedicalCertificate(**form.cleaned_data)
            med.save()
            return redirect(reverse('license_create'))
    else:
        form = MedicalCertificateForm()

    template = 'gibdd_app/MedicalCertificate_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def add_disq(request):
    if request.method == 'POST':
        form = LicenseDisqualificationForm(request.POST, request.FILES)  # тут возвращается словарь вместе с csrf
        if form.is_valid():
            med = LicenseDisqualification(**form.cleaned_data)
            med.save()
            return redirect(reverse('disq_create'))
    else:
        form = LicenseDisqualificationForm()

    template = 'gibdd_app/LicenseDisqualification_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


# @permission_required("can_add_lisense_category", login_url='forbidden')
@permission_required("can_add_lisense_category")
@login_required
def add_lic_cat(request):
    if request.method == 'POST':
        form = Licen_CatForm(request.POST, request.FILES)
        if form.is_valid():
            main_form = Lisense_Category(**form.cleaned_data)
            main_form.save()
            return redirect(reverse('workers'), args=[main_form.pk])
        else:
            text = '<i><b>Пожалуйста, введите корректные данные.Данная пара ВУ_категория уже существует.</b></i> '
            button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
            tex = (text, button)
            return HttpResponse(tex)
    else:
        form = Licen_CatForm()

    template = 'gibdd_app/Licen_CatForm.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
# @permission_required('accident_create')
def add_accident(request):
    if request.method == 'POST':
        form = AccidentReportForm(request.POST, request.FILES)
        if form.is_valid():
            accid = AccidentReport(**form.cleaned_data)
            accid.save()
            return redirect(reverse('workers'), args=[accid.pk])
    else:
        form = AccidentReportForm()

    template = 'gibdd_app/AccidentReport_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


#
# @has_add_permission()
# @permission_required("can_add_witness")
@login_required
def add_witness(request):
    if request.method == 'POST':
        form = WitnessForm(request.POST, request.FILES)
        if form.is_valid():
            wit = Witness(**form.cleaned_data)
            wit.save()
            return redirect(reverse('workers'), args=[wit.pk])
    else:
        form = WitnessForm()

    template = 'gibdd_app/Witness_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_licen_accid(request):
    if request.method == 'POST':
        form = Lisense_AccidentForm(request.POST, request.FILES)
        if form.is_valid():
            l_a = Lisense_Accident(**form.cleaned_data)
            l_a.save()
            return redirect(reverse('workers'), args=[l_a.pk])
    else:
        form = Lisense_AccidentForm()

    template = 'gibdd_app/Lisense_Accident_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


# @permission_required("can_add_inspector",)
@login_required
def add_inspector(request):
    if request.method == 'POST':
        form = InspectorForm(request.POST, request.FILES)
        if form.is_valid():
            insp = Inspector(**form.cleaned_data)
            insp.save()
            return redirect(reverse('workers'), args=[insp.pk])
    else:
        form = InspectorForm()

    template = 'gibdd_app/Inspector_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_fine(request):
    if request.method == 'POST':
        form = FineForm(request.POST, request.FILES)
        if form.is_valid():
            fine = Fine(**form.cleaned_data)
            fine.save()
            return redirect(reverse('workers'), args=[fine.pk])
    else:
        form = FineForm()

    template = 'gibdd_app/Fine_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = Car(**form.cleaned_data)
            car.save()
            return redirect(reverse('workers'), args=[car.pk])
    else:
        form = CarForm()

    template = 'gibdd_app/Car_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_registr(request):
    if request.method == 'POST':
        form = RegistrationCertificateForm(request.POST, request.FILES)
        if form.is_valid():
            reg = RegistrationCertificate(**form.cleaned_data)
            reg.save()
            return redirect(reverse('workers'), args=[reg.pk])
    else:
        form = RegistrationCertificateForm()

    template = 'gibdd_app/RegistrationCertificate_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES)
        if form.is_valid():
            reg = Owner(**form.cleaned_data)
            reg.save()
            return redirect(reverse('workers'), args=[reg.pk])
    else:
        form = OwnerForm()

    template = 'gibdd_app/Owner_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_steal(request):
    if request.method == 'POST':
        form = StealingForm(request.POST, request.FILES)
        if form.is_valid():
            steal = Stealing(**form.cleaned_data)
            steal.save()
            return redirect(reverse('workers'), args=[steal.pk])
    else:
        form = StealingForm()

    template = 'gibdd_app/Stealing_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_decree(request):
    if request.method == 'POST':
        form = DecreeForm(request.POST, request.FILES)
        if form.is_valid():
            decree = Decree(**form.cleaned_data)
            decree.save()
            return redirect(reverse('workers'), args=[decree.pk])
    else:
        form = DecreeForm()

    template = 'gibdd_app/Decree_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_camera(request):
    if request.method == 'POST':
        form = CameraForm(request.POST, request.FILES)
        if form.is_valid():
            cam = Camera(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = CameraForm()

    template = 'gibdd_app/Camera_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_autoschool(request):
    if request.method == 'POST':
        form = AutoschoolForm(request.POST, request.FILES)
        if form.is_valid():
            cam = AutoSchool(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = AutoschoolForm()

    template = 'gibdd_app/AutoSchool_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_history(request):
    if request.method == 'POST':
        form = HistoryForm(request.POST, request.FILES)
        if form.is_valid():
            cam = CarHistory(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = HistoryForm()

    template = 'gibdd_app/History_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_diagnostic_card(request):
    if request.method == 'POST':
        form = DiagnosticCardForm(request.POST, request.FILES)
        if form.is_valid():
            cam = DiagnosticCard(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = DiagnosticCardForm()

    template = 'gibdd_app/DiagnosticCard_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            cam = Driver(**form.cleaned_data)
            cam.save()
            return redirect(reverse('license_create'), args=[cam.pk])
    else:
        form = DriverForm()

    template = 'gibdd_app/Driver_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cam = Category(**form.cleaned_data)
            cam.save()
            return redirect(reverse('categ_create'), args=[cam.pk])
    else:
        form = CategoryForm()

    template = 'gibdd_app/Category_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_insurance(request):
    if request.method == 'POST':
        form = InsuranceForm(request.POST, request.FILES)
        if form.is_valid():
            cam = Insurance(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = InsuranceForm()

    template = 'gibdd_app/Insurance_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_insurance_license(request):
    if request.method == 'POST':
        form = InsuranceLicenseForm(request.POST, request.FILES)
        if form.is_valid():
            cam = InsuranceLicense(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = InsuranceLicenseForm()

    template = 'gibdd_app/InsuranceLicense_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_accident_car(request):
    if request.method == 'POST':
        form = Accident_CarForm(request.POST, request.FILES)
        if form.is_valid():
            cam = Accident_Car(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
        else:
            text = '<i><b>Пожалуйста, введите корректные данные.Данная пара ДТП - автомобиль уже существует.</b></i> '
            button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
            tex = (text, button)
            return HttpResponse(tex)
    else:
        form = Accident_CarForm()

    template = 'gibdd_app/Accident_Car_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
