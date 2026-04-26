from predict import predict_category

tests = [
    "zomato pizza",
    "uber ride",
    "monthly house rent",
    "amazon shopping",
    "mutual fund investment",
    "doctor appointment",
    "grocery store",
    "electricity bill",
    "movie tickets",
    "flight booking"
]

print("\n--- MODEL TEST RESULTS ---\n")

for t in tests:
    category, confidence = predict_category(t)
    print(f"{t} → {category} ({confidence:.2f})")