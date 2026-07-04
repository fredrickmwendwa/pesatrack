from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from finance.models import Transaction, Category, Budget

class DashboardView(LoginRequiredMixin, TemplateView):
  template_name = 'dashboard/dashboard.html'