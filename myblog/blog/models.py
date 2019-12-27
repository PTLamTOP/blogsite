from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=500, null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        # showing Django the correct URL pattern to an article according to our site structure
        return reverse('article-detail', kwargs={'pk': self.pk})

