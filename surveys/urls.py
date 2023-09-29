from django.urls import path

from .views import IndexView, ThanksView, SurveysView, LoginView, LogoutView
from .views import page_view, take_view, raters_view, survey_dashboard_view, download_raters_view, search_raters_view
from .views import navbar_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('navbar/', navbar_view, name='navbar'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('surveys/', SurveysView.as_view(), name='surveys'),
    path('survey/raters-dashboard/<str:survey_id>/<str:rater_id>/', raters_view, name='raters-dashboard'),
    path('survey/take/<str:survey_id>/<str:rater_id>/', take_view, name='take'),
    path('survey/page/<str:survey_id>/<str:rater_id>/', page_view, name='page'),
    path('survey/dashboard/<str:survey_id>/', survey_dashboard_view, name='survey_dashboard'),
    path('survey/raters/upload/<str:survey_id>/', survey_dashboard_view, name='upload_raters'),
    path('survey/raters/download/<str:survey_id>/', download_raters_view, name='download_raters'),
    path('survey/raters/search/<str:survey_id>/', search_raters_view, name='search_raters'),
]