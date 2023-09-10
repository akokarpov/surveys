from django.urls import path

from .views import IndexView, ThanksView, DashboardView, take_view
from .views import page_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('<slug:survey_slug>/<int:survey_id>/<int:rater_id>/', take_view, name='take'),
    path('<int:survey_id>/<int:rater_id>/page', page_view, name='page'),
    # path('<slug:survey_slug>/<int:survey_id>/<int:rater_id>/', TakeView.as_view(), name='take'),
]