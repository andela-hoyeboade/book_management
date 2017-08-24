from django.conf.urls import url, include
import views

urlpatterns = [
  url(r'^categories/$', views.CategoryView.as_view(), name='category_api'),
  url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view(), name='category_detail_api'),
  url(r'^categories/(?P<pk>[0-9]+)/books/$', views.CategoryBookView.as_view(), name='category_book_api'),  
  url(r'^books/$', views.BookView.as_view(), name='book_api'),
  url(r'^books/(?P<pk>[0-9]+)/$', views.BookView.as_view(), name='book_detail_api'),
]