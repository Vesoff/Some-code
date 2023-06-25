from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        rate_of_posts_by_author = Post.objects.filter(author=self).aggregate(result=Sum('rating')).get('result') * 3
        rate_of_com_by_author = Comment.objects.filter(user=self.user).aggregate(result=Sum('rating')).get('result')
        rate_of_com_posts_author = Comment.objects.filter(user=self.user).aggregate(result=Sum('rating')).get('result')

        self.rating = rate_of_posts_by_author + rate_of_com_by_author + rate_of_com_posts_author
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def subscribe(self):
        pass

    def __str__(self):
        return self.name


class Post (models.Model):
    objects = None
    news = 'NW'
    article = 'AR'

    TYPE = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    post_type = models.CharField(max_length=2,
                                 choices=TYPE,
                                 default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def preview(self):
        return self.text[:124] + '...'


class PostCategory (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment (models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
