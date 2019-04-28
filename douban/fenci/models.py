from django.db import models


# Create your models here.
class MovieName(models.Model):
    # id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=20)

    def __str__(self):              # __unicode__ on Python 2
        return self.full_name.encode('utf-8')


# com_name is_seen com_star(option) comment_time comment-vote short mv_name
class CommentInfo(models.Model):
    com_name = models.CharField(max_length=20)
    com_star = models.CharField(max_length=10)
    # comment_time = models.DateTimeField('2018-12-07')
    short = models.CharField(max_length=350)
    comment_vote = models.IntegerField(default=0)
    # mv = models.ForeignKey(MovieName)
    movie_name = models.CharField(max_length=10)

    def __str__(self):              # __unicode__ on Python 2
        return self.short.encode('utf-8')
