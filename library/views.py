from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Book, Author, Category, Member, Borrowing
from .forms import BookForm, AuthorForm, CategoryForm, MemberForm, BorrowingForm
from .exceptions import BookAvailabilityError, DueDateViolationError

# Create your views here.

class HomeView(ListView):
    template_name = 'library/home.html'
    context_object_name = 'books'
    model = Book
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['stats'] = Book.get_book_statistics()
        return context

class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.filter(is_active=True)
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query) |
                Q(isbn__icontains=query)
            )
        if category:
            queryset = queryset.filter(category__name=category)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_available'] = self.object.available_quantity > 0
        return context

class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

class AuthorListView(ListView):
    model = Author
    template_name = 'library/author_list.html'
    context_object_name = 'authors'

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'library/author_detail.html'
    context_object_name = 'author'

class AuthorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('author_list')

    def test_func(self):
        return self.request.user.is_staff

class AuthorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('author_list')

    def test_func(self):
        return self.request.user.is_staff

class AuthorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Author
    template_name = 'library/author_confirm_delete.html'
    success_url = reverse_lazy('author_list')

    def test_func(self):
        return self.request.user.is_staff

class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = 'library/member_list.html'
    context_object_name = 'members'

class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'library/member_detail.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrowings'] = self.object.borrowings.filter(is_returned=False)
        context['history'] = self.object.borrowings.filter(is_returned=True)
        context['today'] = timezone.now().date()
        return context

class MemberCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'library/member_form.html'
    success_url = reverse_lazy('library:member_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Successfully created member: {self.object.first_name} {self.object.last_name}")
        return response

class BorrowingCreateView(LoginRequiredMixin, CreateView):
    model = Borrowing
    form_class = BorrowingForm
    template_name = 'library/borrowing_form.html'
    success_url = reverse_lazy('library:borrowing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        book_id = self.request.GET.get('book')
        if book_id:
            try:
                book = Book.objects.get(pk=book_id)
                form.fields['item'].initial = book
            except Book.DoesNotExist:
                pass
        return form

    def form_valid(self, form):
        item = form.cleaned_data['item']
        if item.available_quantity <= 0:
            raise BookAvailabilityError(f"{item.title} is not available for borrowing")
        response = super().form_valid(form)
        item.available_quantity -= 1
        item.save()
        messages.success(self.request, f"Successfully borrowed {item.title}")
        return response

class BorrowingListView(LoginRequiredMixin, ListView):
    model = Borrowing
    template_name = 'library/borrowing_list.html'
    context_object_name = 'borrowings'

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        status = self.request.GET.get('status')
        
        if status == 'active':
            queryset = queryset.filter(is_returned=False)
        elif status == 'returned':
            queryset = queryset.filter(is_returned=True)
        elif status == 'overdue':
            queryset = queryset.filter(is_returned=False, due_date__lt=timezone.now().date())
            
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context

def return_item(request, pk):
    if request.method == 'POST':
        borrowing = get_object_or_404(Borrowing, pk=pk)
        if not borrowing.is_returned:
            borrowing.is_returned = True
            borrowing.return_date = timezone.now()
            borrowing.save()
            
            item = borrowing.item
            item.available_quantity += 1
            item.save()
            
            messages.success(request, f"Successfully returned {item.title}")
        else:
            messages.warning(request, "This item has already been returned")
            
        return redirect('borrowing_list')
