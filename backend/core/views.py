from django.shortcuts import render
from .ml.predict import predict_category
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Transaction, Budget
from .serializers import TransactionSerializer, BudgetSerializer,RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from collections import defaultdict

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_transaction(request):
    data = request.data
    user = request.user

    title = data['title']
    amount = data['amount']

 
    predicted_category, confidence = predict_category(title)

    if confidence < 0.5:
        predicted_category = "Miscellaneous"


    transaction = Transaction.objects.create(
        user=user,
        title=title,
        amount=amount,
        category=predicted_category,
        is_auto_categorized=True
    )


    try:
        budget = Budget.objects.get(user=user)
        budget.current_spent += float(amount)
        budget.save()
    except Budget.DoesNotExist:
        pass

    return Response({
        "message": "Transaction added",
        "category": predicted_category,
        "confidence": confidence
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_budget(request):
    user = request.user
    amount = request.data['monthly_limit']

    budget, created = Budget.objects.get_or_create(user=user)
    budget.monthly_limit = amount
    budget.current_spent = 0
    budget.save()

    return Response({"message": "Budget set successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_budget(request):
    user = request.user

    try:
        budget = Budget.objects.get(user=user)
        remaining = budget.monthly_limit - budget.current_spent

        return Response({
            "monthly_limit": budget.monthly_limit,
            "spent": budget.current_spent,
            "remaining": remaining
        })
    except Budget.DoesNotExist:
        return Response({"error": "No budget found"})
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"})
    
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def login(request):
    username = request.data['username']
    password = request.data['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
    return Response({"error": "Invalid credentials"})





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_insights(request):
    user = request.user

  
    transactions = Transaction.objects.filter(user=user)

    try:
        budget = Budget.objects.get(user=user)
    except Budget.DoesNotExist:
        return Response({"error": "No budget set"})

   
    total_spent = sum(t.amount for t in transactions)
    remaining = budget.monthly_limit - total_spent

    # Category-wise spending
    category_data = defaultdict(float)
    for t in transactions:
        category_data[t.category] += t.amount

    category_breakdown = [
        {"category": k, "amount": v}
        for k, v in category_data.items()
    ]

    percent_used = (
        (total_spent / budget.monthly_limit) * 100
        if budget.monthly_limit > 0 else 0
    )

    top_category = max(category_data, key=category_data.get) if category_data else None


    alert = None

    if percent_used >= 90:
        alert = "🚨 Critical: You have used 90% of your budget!"
    elif percent_used >= 70:
        alert = "⚠️ Warning: You have used 70% of your budget."

    suggestion = None

    if top_category == "Food":
        suggestion = "You are spending a lot on food. Try reducing outside orders."
    elif top_category == "Travel":
        suggestion = "Travel expenses are high. Consider optimizing routes."
    elif top_category == "Household":
        suggestion = "Household expenses are high. Review recurring costs."
    elif top_category == "Investment":
        suggestion = "Good job investing. Keep monitoring returns and risks."
    elif top_category == "Personal":
        suggestion = "Personal expenses are rising. Track non-essential spending."
    elif top_category == "Miscellaneous":
        suggestion = "Miscellaneous spending is high. Check for unnecessary expenses."


    return Response({
        "total_spent": total_spent,
        "remaining": remaining,
        "budget": budget.monthly_limit,
        "percent_used": round(percent_used, 2),
        "category_breakdown": category_breakdown,
        "top_category": top_category,
        "alert": alert,
        "suggestion": suggestion
    })