import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import CarMake, CarModel

DEALERSHIPS = [
    {"id": 15, "full_name": "Best Cars Kansas City", "city": "Kansas City", "state": "Kansas",
     "address": "1200 Main Street", "zip": "66101", "st": "KS", "lat": 39.0997, "lng": -94.5786},
    {"id": 16, "full_name": "Best Cars Chicago", "city": "Chicago", "state": "Illinois",
     "address": "200 Michigan Avenue", "zip": "60601", "st": "IL", "lat": 41.8781, "lng": -87.6298},
]
REVIEWS = {
    15: [{"id": 1, "name": "Alex Morgan", "review": "Fantastic services and a smooth purchase."}],
    16: [{"id": 2, "name": "Jordan Lee", "review": "Helpful staff and a great selection."}],
}


def _json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    data = _json_body(request)
    username = data.get("username", data.get("userName", ""))
    user = authenticate(request, username=username, password=data.get("password", ""))
    if user is None:
        return JsonResponse({"userName": "", "status": "Invalid credentials"}, status=401)
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated"})


@require_http_methods(["GET", "POST"])
def logout_request(request):
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({"userName": username if request.method == "POST" else ""})


@csrf_exempt
@require_http_methods(["POST"])
def registration(request):
    data = _json_body(request)
    required = ("username", "first_name", "last_name", "email", "password")
    if any(not data.get(field) for field in required):
        return JsonResponse({"error": "All registration fields are required."}, status=400)
    if User.objects.filter(username=data["username"]).exists():
        return JsonResponse({"error": "Username already exists."}, status=409)
    if User.objects.filter(email=data["email"]).exists():
        return JsonResponse({"error": "Email already exists."}, status=409)
    user = User.objects.create_user(
        username=data["username"], first_name=data["first_name"],
        last_name=data["last_name"], email=data["email"], password=data["password"]
    )
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated"}, status=201)


def get_cars(request):
    cars = [{
        "CarMake": make.name,
        "CarMakeDescription": make.description,
        "CarModels": [
            {"CarModel": model.name, "CarModelType": model.type, "CarModelYear": model.year}
            for model in make.models.all()
        ],
    } for make in CarMake.objects.prefetch_related("models").all()]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state=None):
    dealers = DEALERSHIPS if not state else [
        dealer for dealer in DEALERSHIPS if dealer["state"].lower() == state.lower()
    ]
    return JsonResponse({"dealerships": dealers})


def get_dealer_details(request, dealer_id):
    dealer = next((item for item in DEALERSHIPS if item["id"] == dealer_id), None)
    if dealer is None:
        return JsonResponse({"error": "Dealership not found."}, status=404)
    return JsonResponse(dealer)


def _sentiment(review):
    positive = ("fantastic", "great", "excellent", "helpful", "smooth", "good")
    negative = ("bad", "poor", "terrible", "awful", "disappointing")
    text = review.lower()
    if any(word in text for word in positive):
        return "positive"
    if any(word in text for word in negative):
        return "negative"
    return "neutral"


def analyze_review(request, review):
    return JsonResponse({"sentiment": _sentiment(review.replace("%20", " "))})


def get_dealer_reviews(request, dealer_id):
    reviews = REVIEWS.get(dealer_id)
    if reviews is None:
        return JsonResponse({"error": "Dealership not found."}, status=404)
    return JsonResponse({"reviews": [
        dict(review, sentiment=_sentiment(review["review"])) for review in reviews
    ]})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def add_review(request):
    data = _json_body(request)
    dealer_id = int(data.get("dealer_id", 0))
    review_text = str(data.get("review", "")).strip()
    if dealer_id not in REVIEWS or not review_text:
        return JsonResponse({"error": "A valid dealer and review are required."}, status=400)
    review = {"id": len(REVIEWS[dealer_id]) + 1, "name": request.user.get_full_name() or request.user.username,
              "review": review_text}
    REVIEWS[dealer_id].append(review)
    return JsonResponse(dict(review, sentiment=_sentiment(review_text)), status=201)
