from django.conf.urls import url, include
from rest_framework import routers

from myproject import views


router = routers.DefaultRouter()
router.register(r'letter_digits', views.LetterDigitViewSet)
router.register(r'user_birthdays', views.UserBirthdayViewSet)

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^user_birthdays/average/?$', views.AverageAge.as_view()),
    url(r'^', include(router.urls)),
]
