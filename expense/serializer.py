from rest_framework import serializers

from expense.models import Expense, User

class Userserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "country_code", "full_name", "date_joined", "password"]
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        return user
        
class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Expense
        fields = "__all__"
        
class ExpenseAnalyticsSerializer(serializers.Serializer):
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_breakdown = serializers.ListField(child = serializers.DictField())
    daily_stats = serializers.ListField(child = serializers.DictField())
    weekly_stats = serializers.ListField(child = serializers.DictField())
    monthly_stats = serializers.ListField(child = serializers.DictField())
    daily_average = serializers.DecimalField(max_digits=10, decimal_places=2)
    weekly_average = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_average = serializers.DecimalField(max_digits=10, decimal_places=2)   