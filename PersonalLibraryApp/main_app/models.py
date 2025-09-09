# from django.db import models

# # Create your models here.


from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

READING_STATUS = (
    ('W', 'Want to Read'),
    ('R', 'Currently Reading'), 
    ('F', 'Finished'),
)

class Bookmark(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    material = models.CharField(max_length=30)
    
    def __str__(self):
        return f'A {self.color} {self.material} {self.name}'
    
    def get_absolute_url(self):
        return reverse('bookmarks_detail', kwargs={'pk': self.id})

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    pages = models.IntegerField()
    description = models.TextField(max_length=250)
    bookmarks = models.ManyToManyField(Bookmark)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'book_id': self.id})

class Reading(models.Model):
    date = models.DateField('Reading Date')
    status = models.CharField(
        max_length=1,
        choices=READING_STATUS,
        default=READING_STATUS[0][0]
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.get_status_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']