from rest_framework import serializers
from .models import Category, Transaction, Budget

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'name', 'created_at']
    read_only_fields = ['id', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
  category_name = serializers.CharField(source='category.name', read_only=True)

  class Meta:
    model = Transaction
    fields = ['id', 'category', 'category_name', 'amount', 'transaction_type', 'date', 'note', 'created_at']
    read_only_fields = ['id', 'created_at']

    def validate_category(self, category):
      request_user = self.context['request'].user
      if category.user != request_user:
        raise serializers.ValidationError("You can only use your own categories.")
      return category

class BudgetSerializer(serializers.ModelSerializer):
  class Meta:
    model = Budget
    fields = ['id', 'name', 'monthly_limit' 'created_at']
    read_only_fields = ['id', 'created_at']
