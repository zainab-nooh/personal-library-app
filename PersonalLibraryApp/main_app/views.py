# from django.shortcuts import render

# # Create your views here.

# def home(request):
#     return HttpResponse("Hello from the main app!")


from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Bookmark
from .forms import ReadingForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def books_index(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'books/index.html', {
        'books': books
    })

@login_required
def books_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    id_list = book.bookmarks.all().values_list('id')
    bookmarks_book_doesnt_have = Bookmark.objects.exclude(id__in=id_list)
    reading_form = ReadingForm()
    return render(request, 'books/detail.html', {
        'book': book,
        'reading_form': reading_form,
        'bookmarks': bookmarks_book_doesnt_have
    })

@login_required
def add_reading(request, book_id):
    form = ReadingForm(request.POST)
    if form.is_valid():
        new_reading = form.save(commit=False)
        new_reading.book_id = book_id
        new_reading.save()
    return redirect('detail', book_id=book_id)

@login_required
def assoc_bookmark(request, book_id, bookmark_id):
    Book.objects.get(id=book_id).bookmarks.add(bookmark_id)
    return redirect('detail', book_id=book_id)

@login_required
def unassoc_bookmark(request, book_id, bookmark_id):
    Book.objects.get(id=book_id).bookmarks.remove(bookmark_id)
    return redirect('detail', book_id=book_id)

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'genre', 'pages', 'description']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['genre', 'pages', 'description']

class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = '/books'

class BookmarkList(LoginRequiredMixin, ListView):
    model = Bookmark

class BookmarkDetail(LoginRequiredMixin, DetailView):
    model = Bookmark

class BookmarkCreate(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = '__all__'

class BookmarkUpdate(LoginRequiredMixin, UpdateView):
    model = Bookmark
    fields = '__all__'

class BookmarkDelete(LoginRequiredMixin, DeleteView):
    model = Bookmark
    success_url = '/bookmarks'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)