from django.db import models

# Create your models here.
from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from django.contrib.auth  import get_user_model

from Accounts.models import Account

# Create your models here.
Account=get_user_model()

# class Tag(models.Model):
#     name = models.CharField(max_length=200)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True,
#                           primary_key=True, editable=False)

#     def __str__(self):
#         return self.name

class Project(models.Model):
    owner=models.ForeignKey(Account,null=True,blank=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)                          #HERE "TAG " is used not Tag only as the other model defined is below it
    vote_total = models.IntegerField(default=0, null=True, blank=True)  
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering=['-vote_ratio','-vote_total','title']

    
    #Making a query set to check that user has already review the project and also user itself cannot review work
    #flatt=true gives this as alist  still confirem
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        print(f'review qery set {queryset}')
        return queryset


    #to update vote_ratio and count 
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        totalVotes = reviews.count()
        upVotes = reviews.filter(value='up').count()
        
        print(f'total no of votes {totalVotes}')

        
        ratio = (upVotes / totalVotes) * 100
        
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        
        print(f'total no of votes 2nd print {totalVotes}')
        print(f'reviews{reviews}')
        print(f' no of up votes {upVotes}')
        # print(f'ratio {ratio}')
        self.save()
    
    
    

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together=[['owner','project']]
    
    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
