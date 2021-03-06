from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from time import time



def get_upload_file_name(instance,filename):
    return 'images/%s/%s_%s'% (type(instance).__name__,str(time()).replace('.','_'),filename)


class SiteUser(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username


class Track(models.Model):
    title = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    description = models.TextField()

    def __unicode__(self):
        return self.title



class Question(models.Model):

    type_choices = (
        ('IQ', 'IQ'),
        ('EN', 'English'),
        ('FAQ', 'FAQ'),
        ('SOFT', 'Soft Skills'),
        ('TRACK', 'Track'),
    )

    status_choices = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )



    header = models.CharField(max_length=100)
    user_id = models.ForeignKey(User)
    track_id = models.ManyToManyField(Track, blank=True)

    type = models.CharField(choices=type_choices, max_length=10, default='TRACK')

    status = models.CharField(max_length=10,choices=status_choices, default=status_choices[0][0])


    image = models.ImageField(null=True,blank=True, upload_to=get_upload_file_name)
    voteUpUsers = models.ManyToManyField(User, blank=True,related_name='questionUpVotes')
    voteDownUsers = models.ManyToManyField(User, blank=True,related_name='questionDownVotes')


    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)


    @property
    def votes(self):
        return self.voteUpUsers.count() - self.voteDownUsers.count()


    def userVote(self,user):
        if self.voteUpUsers.filter(pk=user.id).exists():
            return 1
        elif self.voteDownUsers.filter(pk=user.id).exists():
            return -1
        else:
            return 0

    def __unicode__(self):
        return self.header

class Answer(models.Model):

    status_choices = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    body = models.TextField("Answer")
    question_id = models.ForeignKey(Question, related_name='answers')
    user_id = models.ForeignKey(User)


    voteUpUsers = models.ManyToManyField(User, blank=True,related_name='answerUpVotes')
    voteDownUsers = models.ManyToManyField(User, blank=True,related_name='answerDownVotes')


    status = models.CharField(max_length=10,choices=status_choices, default=status_choices[0][0])


    image = models.ImageField(null=True,blank=True, upload_to=get_upload_file_name)

    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    @property
    def votes(self):
        return self.voteUpUsers.count() - self.voteDownUsers.count()


    def userVote(self,user):
        if self.voteUpUsers.filter(pk=user.id).exists():
            return 1
        elif self.voteDownUsers.filter(pk=user.id).exists():
            return -1
        else:
            return 0

    def __unicode__(self):
        return self.body


class Material(models.Model):

    status_choices = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    type_choices = (
        ('IQ', 'IQ'),
        ('EN', 'English'),
        ('SOFT', 'Soft Skills'),
        ('TRACK', 'Track'),
    )

    name = models.CharField(max_length=100)
    link = models.URLField()
    type = models.CharField(choices=type_choices, max_length=10, default='TRACK')

    description = models.TextField(blank=True)
    user_id = models.ForeignKey(User)
    track_id = models.ManyToManyField(Track, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    status = models.CharField(max_length=10,choices=status_choices, default=status_choices[0][0])

    voteUpUsers = models.ManyToManyField(User, blank=True,related_name='materialUpVotes')
    voteDownUsers = models.ManyToManyField(User, blank=True,related_name='materialDownVotes')


    @property
    def votes(self):
        return self.voteUpUsers.count() - self.voteDownUsers.count()


    def userVote(self,user):
        if self.voteUpUsers.filter(pk=user.id).exists():
            return 1
        elif self.voteDownUsers.filter(pk=user.id).exists():
            return -1
        else:
            return 0


    def __unicode__(self):
        return self.name


class Type(models.Model):
    role = (
        ('HR', 'HR'),
        ('Technical', 'Technical'),
        ('Final', 'Final_interview') )
    role_type = models.CharField(max_length=1, choices=role)

    def __unicode__(self):
        return self.role_type


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1200)
    date = models.CharField(max_length=100)
    type_name = models.ForeignKey(Type)

    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.title