from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Books
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    
    # Magazines
    path('magazines/', views.MagazineListView.as_view(), name='magazine_list'),
    path('magazines/<int:pk>/', views.MagazineDetailView.as_view(), name='magazine_detail'),
    
    # Members
    path('members/', views.MemberListView.as_view(), name='member_list'),
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    
    # Borrowings
    path('borrowings/', views.BorrowingListView.as_view(), name='borrowing_list'),
    path('borrowings/create/', views.BorrowingCreateView.as_view(), name='borrowing_create'),
    path('borrowings/<int:pk>/return/', views.return_item, name='return_item'),
] 