from django.urls import path
from rest_framework.authtoken import views as token_views
from . import views
from .views import UserProfileView, LogoutView

app_name = "books"

urlpatterns = [
    # Authentication endpoints
    path("token/", token_views.obtain_auth_token, name="token_obtain"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    # Books endpoints
    path("books/", views.BookListCreateView.as_view(), name="book-list-create"),
    path("books/<str:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path(
        "books/stats/year/<int:year>/",
        views.BookYearStatsView.as_view(),
        name="book-year-stats",
    ),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('user/logout/', LogoutView.as_view(), name='logout'),
]
