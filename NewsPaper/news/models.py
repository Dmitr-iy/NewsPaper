from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)


    def update_rating(self):
        ratPosAuth =self.post_set.all().aggregate(RatingPost=Sum('rating'))
        p = 0
        p += ratPosAuth.get('RatingPost')
        ratComm = self.user.comment_set.all().aggregate(RatingComm=Sum('rating'))
        c = 0
        c += ratComm.get('RatingComm')

        self.authorRating = c + p * 3
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    objects = None
    category_name = models.CharField(max_length=128, unique= True)
    subscribers = models.ManyToManyField(User, related_name='categories')
    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    typContent = [('Article', 'Article'), ('News', 'News')]
    newsArticle = models.CharField(choices=typContent, max_length=7, default='News')
    dateTime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0 : 128] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def __str__(self):
        data = 'Post from {}'.format(self.dateTime.strftime('%d.%m.%Y %H:%M'))
        return f'{data}, {self.author}, {self.title}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    userComment = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataTime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.dataTime}, {self.userComment}'