import csv
import io

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView, View

from rate.models import Rate
from rate.selectors import get_latest_rates
from rate.utils import display

import xlsxwriter


class RateList(ListView):
    queryset = Rate.objects.all().order_by('created')
    template_name = 'rate-list.html'
    paginate_by = 25

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.queryset.is_authenticated
    #     return queryset

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['Helo'] = 'World'
    #     return context


class LatestRatesView(TemplateView):
    template_name = 'latest-rates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['object_list'] = get_latest_rates()
        return context


class RateDownloadCSV(View):
    HEADERS = (
        'created',  # rate.created
        'amount',
        'source',  # rate.get_source_display()
        'currency_type',
        'type_rate',
    )
    queryset = Rate.objects.all().iterator()

    def get_response(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rates.csv"'
        return response

    def get(self, request):

        response = self.get_response()

        writer = csv.writer(response)
        writer.writerow(self.__class__.HEADERS)

        for rate in self.queryset:

            value = []
            for attr in self.__class__.HEADERS:
                value.append(display(rate, attr))

            writer.writerow(value)

        return response


class RateDownloadXLSX(View):
    HEADERS = (
        'created',
        'amount',
        'source',
        'currency_type',
        'type_rate',
    )
    queryset = Rate.objects.all().iterator()

    def get(self, request):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, options={'remove_timezone': True})
        worksheet = workbook.add_worksheet('rates')

        worksheet.set_column(0, 5, width=15)

        row = 0
        col = 0
        for attr in self.__class__.HEADERS:
            worksheet.write_string(row, col, attr)
            col += 1

        row = 1
        col = 0
        for rate in self.queryset:

            for attr in self.__class__.HEADERS:
                worksheet.write(row, col, display(rate, attr))
                if attr == 'type_rate':
                    row += 1
                    col = -1
                if attr == 'created':
                    dt = display(rate, attr).strftime("%m/%d/%Y, %H:%M")
                    worksheet.write_string(row, col, dt)
                col += 1

        workbook.close()

        output.seek(0)

        filename = 'rates.xlsx'
        response = HttpResponse(output,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


def page_not_found_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)


def permission_denied_403(request, exception):
    return render(request, '403.html', status=403)


def bad_request_400(request, exception):
    return render(request, '400.html', status=400)


class EditRate(UserPassesTestMixin, UpdateView):
    template_name = 'edit-rate.html'
    queryset = Rate.objects.all()
    fields = ('amount', 'source', 'currency_type', 'type_rate')
    success_url = reverse_lazy('rate:list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class DeleteRate(LoginRequiredMixin, DeleteView):
    queryset = Rate.objects.all()
    success_url = reverse_lazy('rate:list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
