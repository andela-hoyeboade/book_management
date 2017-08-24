from django.conf.urls import url, include
import views

urlpatterns = [
  url(r'^categories/', views.CategoryView.as_view(), name='api_category'),
  url(r'^books/', views.BookView.as_view(), name='api_book')
]