from django.views.generic import ListView

from rate.models import Rate


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
