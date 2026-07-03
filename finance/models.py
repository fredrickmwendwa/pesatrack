from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Category(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
  name = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['user', 'name'], name='unique_category_per_user')
    ]
    ordering = ['name']

    def __str__(self):
      return f"{self.name} ({self.user.username})"
    

class Transaction(models.Model):
  INCOME = 'income'
  EXPENSE = 'expense'
  TRANSACTION_TYPE_CHOICES = [
    (INCOME, 'Income'),
    (EXPENSE, 'Expense'),
  ]

  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
  category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
  date = models.DateField()
  note = models.CharField(max_length=255, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-date', '-created_at']
    indexes = [
      models.Index(fields=['user', 'date']),
      models.Index(fields=['user', 'transaction_type']),
    ]

  def __str__(self):
    return f"{self.get_transaction_type_display()}: {self.amount} ({self.category.name})"
  
  def clean(self):
    if self.category and self.category.user_id != self.user_id:
      raise ValidationError("You can only assign your own categories to your transactions.")

class Budget(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
  monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['user', 'category'], name='unique_budget_per_category')
    ]

  def __str__(self):
    return f"{self.category.name}: {self.monthly_limit}/mo"