from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Category, Transaction
from .forms import TransactionForm
class CategoryListView(LoginRequiredMixin, ListView):
  model = Category
  template_name = 'finance/category_list.html'
  context_object_name = 'categories'

  def get_queryset(self):
    return Category.objects.filter(user=self.request.user)
  
class CategoryCreateView(LoginRequiredMixin, CreateView):
  model = Category
  fields = ['name']
  template_name = 'finance/category_form.html'
  success_url = reverse_lazy('category_list')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Category
  fields = ['name']
  template_name = 'finance/category_form.html'
  success_url = reverse_lazy('category_list')

  def test_func(self):
    return self.get_object().user == self.request.user
  
class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Category
  template_name = 'finance/category_confirm_delete.html'
  success_url = reverse_lazy('category_list')

  def test_func(self):
    return self.get_object().user == self.request.user
  
class TransactionListView(LoginRequiredMixin, ListView):
  model = Transaction
  template_name = 'finance/transaction_list.html'
  context_object_name = 'transactions'
  paginate_by = 20

  def get_queryset(self):
    return Transaction.objects.filter(user=self.request.user).select_related('category')
  
class TransactionCreateView(LoginRequiredMixin, CreateView):
  model = Transaction
  form_class = TransactionForm
  template_name = 'finance/transaction_form.html'
  success_url = reverse_lazy('transaction_list')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Transaction
  form_class = TransactionForm
  template_name = 'finance/transaction_form.html'
  success_url = reverse_lazy('transaction_list')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs
  
  def test_func(self):
    return self.get_object().user == self.request.user
  
class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   model = Transaction
   template_name = 'finance/transaction_confirm_delete.html'
   success_url = reverse_lazy('transaction_list')

   def test_func(self):
    return self.get_object().user == self.request.user