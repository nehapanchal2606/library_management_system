from django.urls import path, include
from app import views
from rest_framework.routers import DefaultRouter




router = DefaultRouter()
router.register(r'book', views.BookView, basename='book')
urlpatterns = [
    path('register/', views.Registerview.as_view(), name='register'),
    
    path('', include(router.urls)),
    
    path('authors/', views.AuthorListAndCreateView.as_view(), name='authors'),
    path('genres/', views.GenericLisrView.as_view(), name='genres'),
    path('borrow/' , views.BorrowRequestCreateView.as_view(), name='borrow'),
    path('borrow/list/', views.UserBorrowRequestLsitView.as_view(), name='borrow-list'),
    path('borrow/<int:pk>/approve/', views.approve_borrow, name='aprrow_borrow'),
    path('borrow/<int:pk>/reject/', views.reject_borrow, name='reject_borrow'), 
    path('borrow/<int:pk>/return/', views.return_borrow, name='return_borrow'),
    path('book/<int:pk>/reviews/', views.BookReviewCreateView.as_view(), name='bookreview'),
    path('book/<int:pk>/reviews/list/', views.BookReviewListView.as_view(), name='bookreviewlist')
]
