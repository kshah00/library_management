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
    
    # Authors
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    
    # Members
    path('members/', views.MemberListView.as_view(), name='member_list'),
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    path('members/create/', views.MemberCreateView.as_view(), name='member_create'),
    
    # Borrowings
    path('borrowings/', views.BorrowingListView.as_view(), name='borrowing_list'),
    path('borrowings/create/', views.BorrowingCreateView.as_view(), name='borrowing_create'),
    path('borrowings/<int:pk>/return/', views.return_item, name='return_item'),
] 