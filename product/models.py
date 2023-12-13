from django.db import models
from django.core.files import File
from django.contrib.auth.models import User

from PIL import Image
from io import BytesIO

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)  # uporzadkowane alfabetycznie
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=999 )
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/', null=True, blank=True)
    
    class Meta:
        ordering = ('-created',)  # uporzadkowane alfabetycznie

    
    def __str__(self):
        return self.name
    
    def get_display_price(self):
        return self.price / 100


    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return "http://placehold.jp/9797a1/ffffff/240x240.jpg"


    def make_thumbnail(self, image, size=(240, 240)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
    

    def get_rating(self):
        reviews_total = 0

        for review in self.reviews.all():
            reviews_total += review.rating

        if reviews_total > 0:
            return reviews_total / self.reviews.count()
    
        return 0 

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)