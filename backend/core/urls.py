from django.urls import path
from .views import *

urlpatterns = [
    path('add-transaction/', add_transaction),
    path('transactions/', get_transactions),
    path('set-budget/', set_budget),
    path('get-budget/', get_budget),
    path('register/', register),
    path('login/', login),
    path('insights/', get_insights),
]