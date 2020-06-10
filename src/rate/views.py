import csv
import io

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, View


from rate import model_choices as mch
from rate.models import Rate
from rate.utils import display

import xlsxwriter


class RateList(ListView):
    queryset = Rate.objects.all()
    template_name = 'rate-list.html'

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

        object_list = []
        for source in mch.SOURCE_CHOICES:
            source = source[0]
            for currency_type in mch.CURRENCY_TYPE_CHOICES:
                currency_type = currency_type[0]
                for type_rate in mch.RATE_TYPE_CHOICES:
                    type_rate = type_rate[0]

                    rate = Rate.objects.filter(
                        source=source,
                        type_rate=type_rate,
                        currency_type=currency_type,
                    ).last()

                    if rate is not None:
                        object_list.append(rate)

        context['object_list'] = object_list
        return context


class RateDownloadCSV(View):
    HEADERS = (
        'id',
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
        'id',
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
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
