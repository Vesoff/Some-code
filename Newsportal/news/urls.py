from django.urls import path
from .views import PList, PostDetail, PSearchList, PostCreate, PostUpdate, ArticleCreate, PostDelete, PostCategory, subscribe_category

urlpatterns = [
    path('news/', PList.as_view(), name='news_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('news/search/', PSearchList.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('articles/create/', ArticleCreate.as_view(), name='create_art'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('category/<int:pk>/', PostCategory.as_view(), name='category'),
    path('subscribe/<int:pk>/', subscribe_category, name='subscribe'),
   #path('unsubscribe/<int:pk>/', unsubscribe_category, name='unsubscribe'),
]
