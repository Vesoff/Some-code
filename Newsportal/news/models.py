from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        rating_of_posts_by_author = Post.objects.filter(author=self).aggregate(result=Sum('rating')).get('result') * 3
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(result=Sum('rating')).get('result')
        rating_of_comments_under_posts_author = Comment.objects.filter(user=self.user).aggregate(result=Sum('rating')).get('result')

        self.rating = rating_of_posts_by_author + rating_of_comments_by_author + rating_of_comments_under_posts_author
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post (models.Model):
    news = 'NW'
    article = 'AR'

    TYPE = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    post_type = models.CharField(max_length=2,
                                 choices=TYPE,
                                 default=article)
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

    def preview(self, length=124):
        return f"{self.text[:length]}..." if len(self.text) > length else self.text


class PostCategory (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment (models.Model):
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
