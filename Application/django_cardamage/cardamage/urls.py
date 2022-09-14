from django.urls import path, include

from cardamage import views

urlpatterns = [
    path('upload/',views.CarCreate.as_view()),
    path('car/<int:id>/',views.CarDetail.as_view()),
    path('engine/<int:id>',views.CarDetail.as_view()),
]

