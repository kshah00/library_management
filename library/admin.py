from django.contrib import admin
from django.utils.html import format_html
from .models import Book, Magazine, Author, Category, Member, Borrowing

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'category', 'available_quantity', 'display_cover')
    list_filter = ('category', 'author', 'is_active')
    search_fields = ('title', 'isbn', 'author__name')
    readonly_fields = ('created_at', 'updated_at')

    def display_cover(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.cover_image.url)
        return "No cover"
    display_cover.short_description = 'Cover'

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ('title', 'issn', 'category', 'available_quantity', 'display_cover')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'issn')
    readonly_fields = ('created_at', 'updated_at')

    def display_cover(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.cover_image.url)
        return "No cover"
    display_cover.short_description = 'Cover'

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'membership_date', 'is_active')
    list_filter = ('is_active', 'membership_date')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('membership_date',)

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('member', 'item', 'borrow_date', 'due_date', 'return_date', 'is_returned')
    list_filter = ('is_returned', 'borrow_date', 'due_date')
    search_fields = ('member__first_name', 'member__last_name', 'item__title')
    readonly_fields = ('borrow_date',)
