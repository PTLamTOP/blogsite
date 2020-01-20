from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique_for_date='date_posted', null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:article-detail', kwargs={'id': self.id, 'slug': self.slug})


class Comment(MPTTModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.author.username}'

