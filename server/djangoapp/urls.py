from django.urls import path

from .views import (
    add_review, analyze_review, get_cars, get_dealer_details, get_dealer_reviews, get_dealerships,
    login_user, logout_request, registration,
)

urlpatterns = [
    path("register", registration, name="register"),
    path("login", login_user, name="login"),
    path("logout", logout_request, name="logout"),
    path("get_cars", get_cars, name="get_cars"),
    path("get_dealers", get_dealerships, name="get_dealers"),
    path("get_dealers/<str:state>", get_dealerships, name="get_dealers_by_state"),
    path("dealer/<int:dealer_id>", get_dealer_details, name="dealer"),
    path("reviews/dealer/<int:dealer_id>", get_dealer_reviews, name="reviews"),
    path("add_review", add_review, name="add_review"),
    path("analyze/<path:review>", analyze_review, name="analyze_review"),
    path("fetchDealers", get_dealerships, name="fetch_dealers"),
    path("fetchDealers/<str:state>", get_dealerships, name="fetch_dealers_by_state"),
    path("fetchDealer/<int:dealer_id>", get_dealer_details, name="fetch_dealer"),
    path("fetchReviews/dealer/<int:dealer_id>", get_dealer_reviews, name="fetch_reviews"),
]
