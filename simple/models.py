from django.db import models
from django.utils import timezone

#create 2 models, a books model and user model

#books model should contain:
'''
'book_id', 'goodreads_book_id', 'best_book_id', 'work_id',
       'books_count', 'isbn', 'isbn13', 'authors', 'original_publication_year',
       'original_title', 'title', 'language_code', 'average_rating',
       'ratings_count', 'work_ratings_count', 'work_text_reviews_count',
       'ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5',
       'image_url', 'small_image_url'

'''

'''
class Book(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=250)
    phone = PhoneNumberField()
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
    def __str__(self):
        return self.full_name() 

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=250)
    phone = PhoneNumberField()
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
    def __str__(self):
        return self.full_name()

'''