from django.urls import path
from .views import PList, PostDetail

urlpatterns = [
    path('', PList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
]
