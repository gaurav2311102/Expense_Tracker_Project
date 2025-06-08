from django.shortcuts import render
from django.db.models import Sum, Avg
from django.db.models.functions import TruncWeek, TruncMonth
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import datetime


from expense.models import Expense
from expense.serializer import ExpenseAnalyticsSerializer, ExpenseSerializer, Userserializer
from utils import custom_response


class CreateUserView(GenericAPIView):
    serializer_class = Userserializer
    permission_classes = []
    
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        return custom_response(data=self.serializer_class(instance).data, status=status.HTTP_200_OK, message="User created")
        
class LoginView(GenericAPIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class ExpenseListCreateView(GenericAPIView):
    serializer_class = ExpenseSerializer
        
    def post(self,request):
        
        request.data.update({"user":request.user.id})
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        return custom_response(data = self.serializer_class(instance).data, message="Expense created", status=status.HTTP_200_OK)
    
    def get(self,request):
        
        expense_queryset = Expense.objects.filter(user__id = request.user.id).order_by("-date")
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        
        if start_date_str and end_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str)
                end_date = datetime.fromisoformat(end_date_str)
                
            except ValueError:
                raise ValidationError("Invalid datetime format for 'start_date' or 'end_date'.")
            
            expense_queryset = expense_queryset.filter(date__gte = start_date, date__lte = end_date)
        
        serializer = self.serializer_class(expense_queryset, many=True)
            
        return custom_response(data=serializer.data, status=status.HTTP_200_OK, message="Expenses List")
    

class ExpenseAnalyticsView(GenericAPIView):
    serializer_class = ExpenseAnalyticsSerializer
    
    def get(self, request):
    
        expenses = Expense.objects.filter(user=request.user)
        
        total_expenses = expenses.aggregate(total=Sum('amount')).get('total') or 0

        category_breakdown = expenses.values('category').annotate(total=Sum('amount')).order_by('-total')

        daily_stats = (
                        expenses.values('date') 
                                .annotate(total=Sum('amount')) 
                                .order_by('date')
                     )
        daily_average = daily_stats.aggregate(daily_average = Avg("total"))["daily_average"]
        
        weekly_stats = (
                        expenses.annotate(week=TruncWeek('date')) 
                                .values('week') 
                                .annotate(total=Sum('amount')) 
                                .order_by('week')
                        )
        
        weekly_average = weekly_stats.aggregate(weekly_average = Avg("total"))["weekly_average"]
        
        monthly_stats = (
                        expenses.annotate(month=TruncMonth('date')) 
                                .values('month') \
                                .annotate(total=Sum('amount')) 
                                .order_by('month')
                        )
        
        monthly_average = monthly_stats.aggregate(monthly_average = Avg("total"))["monthly_average"]
        
        analytics = {
            "total_expenses": total_expenses,
            "category_breakdown": category_breakdown,
            "daily_stats": daily_stats,
            "weekly_stats":weekly_stats,
            "monthly_stats":monthly_stats,
            "daily_average":daily_average,
            "weekly_average":weekly_average,
            "monthly_average":monthly_average
            
        }
        
        serializer = self.serializer_class(analytics)
        
        return custom_response(data=serializer.data, status=status.HTTP_200_OK, message="Anlaytics")