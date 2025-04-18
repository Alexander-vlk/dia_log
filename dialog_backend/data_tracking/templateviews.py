from lib2to3.fixes.fix_input import context
from tempfile import template

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from data_tracking.forms import DailyLogForm, WeeklyLogForm
from data_tracking.models import DailyLog, WeeklyLog


@login_required
@require_http_methods(['GET', 'POST'])
def weekly_log(request):
    """View для обработки еженедельного отчета"""
    weekly_log_instance = WeeklyLog.objects.get(
        user=request.user,
        week_start__lte=timezone.now(),
        week_end__gte=timezone.now(),
    )
    if request.method == "GET":
        form = WeeklyLogForm(instance=weekly_log_instance)

        context_data = {
            'form': form,
        }

        template_name = 'weekly_log.html'

        return render(request, template_name, context_data)

    form = WeeklyLogForm(request.POST, instance=weekly_log_instance)

    if not form.is_valid():
        return HttpResponseBadRequest()

    form.save()

    cabinet_url = reverse('cabinet')
    return redirect(f'{cabinet_url}?filled_weekly_log=true')


@login_required
@require_http_methods(['GET', 'POST'])
def daily_log(request):
    """View для обработки ежедневного отчета"""
    daily_log_instance = DailyLog.objects.get(user=request.user, date=timezone.now())
    if request.method == "GET":
        form = DailyLogForm(instance=daily_log_instance)

        context_data = {
            'form': form,
        }

        template_name = 'daily_log.html'

        return render(request, template_name, context_data)

    form = DailyLogForm(request.POST, instance=daily_log_instance)

    if not form.is_valid():
        return HttpResponseBadRequest()

    form.save()

    cabinet_url = reverse('cabinet')
    return redirect(f'{cabinet_url}?filled_daily_log=true')


class DailyLogListView(ListView):
    """Страница со списком дневных отчетов"""

    template_name = 'data_tracking/daily_log_list.html'
    context_object_name = 'daily_logs'
    paginate_by = 7

    def get_queryset(self):
        return DailyLog.objects.filter(user=self.request.user).annotate(
            glucose_count=Count('glucoses', distinct=True),
            pressure_count=Count('pressures', distinct=True),
            temperature_count=Count('body_temperatures', distinct=True),
            avg_glucose=Avg('glucoses__level', distinct=True),
            avg_temperature=Avg('body_temperatures__temperature', distinct=True),
            avg_systolic=Avg('pressures__systolic', distinct=True),
            avg_diastolic=Avg('pressures__diastolic', distinct=True),
        ).order_by('-date')
