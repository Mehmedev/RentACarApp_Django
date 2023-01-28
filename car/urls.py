from django.urls import path

from rest_framework import routers

from .views import CarView, ReservationView, ReservationDetailView

router = routers.DefaultRouter()
router.register('car', CarView)

urlpatterns = [
    path('reservation/', ReservationView.as_view()),
    path('reservation/<int:pk>/', ReservationDetailView.as_view())
]

urlpatterns += router.urls
