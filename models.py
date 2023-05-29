from django.db import models
import os
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify


# https://music.youtube.com/watch?v=GfCy_1xKFdU&feature=share


def iconNameChange(instance, filename):
    ext = filename.split('.')[-1]
    new_name = "%s.%s" % (instance.taskFor, ext)
    return os.path.join('static/images/tasks/', new_name)





class Player(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    position = models.CharField(max_length=255,null=True,blank=True)
    team = models.CharField(max_length=255,null=True,blank=True)
    gamesPlayed = models.IntegerField(null=True,blank=True)
    goals = models.IntegerField(null=True,blank=True)
    assists = models.IntegerField(null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    pob = models.CharField(max_length=255,null=True,blank=True)
    isPreferredFootRight = models.BooleanField(default=1)
    pfp = models.ImageField(upload_to="static/images/players", default="static/images/players/default.jpg")
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} : {self.team}"
    


class MatchResult(models.Model) :


    # hsont,hsofft,hpos,hoff,hfoul,hcatk


    opponent = models.CharField(max_length=255,null=True,blank=True)
    shootsOnTarget_rm = models.IntegerField(null=True,blank=True)
    shootsOnTarget_opp = models.IntegerField(null=True,blank=True)
    shootsOffTarget_rm = models.IntegerField(null=True,blank=True)
    shootsOffTarget_opp = models.IntegerField(null=True,blank=True)
    possession_rm = models.IntegerField(null=True,blank=True)
    possession_opp = models.IntegerField(null=True,blank=True)
    offsides_rm = models.IntegerField(null=True,blank=True)
    offsides_opp = models.IntegerField(null=True,blank=True)
    fouls_rm = models.IntegerField(null=True,blank=True)
    fouls_opp = models.IntegerField(null=True,blank=True)
    counterAttack_rm = models.IntegerField(null=True,blank=True)
    counterAttack_opp = models.IntegerField(null=True,blank=True)
    added = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"Real Madrid vs {self.opponent}"



class Calendar(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        if self is not None:
            return f"{self.month}/{self.year}"



    

class Task(models.Model):
    taskName = models.CharField(max_length=255, null=True,blank=True)

    def __str__(self):
        if self is not None:
            return f"{self.taskName}"

class TaskIconSetter(models.Model):
    taskFor = models.OneToOneField(Task, on_delete= models.CASCADE, null=True, blank=True)
    taskIcon = models.ImageField(upload_to=iconNameChange, default="static/images/tasks/default.svg")

    def __str__(self):
        if self is not None:
            return f"{self.taskFor}"

    
class ClaendarTask(models.Model):
    task = models.ForeignKey(Task, on_delete = models.CASCADE, null=True, blank=True)
    taskIcon = models.ForeignKey(TaskIconSetter, on_delete=models.CASCADE,null=True,blank=True)
    taskDate = models.DateField()
    # calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        if self is not None:
            taskname = str(self.task)
            taskdt = self.taskDate.strftime("%Y-%m-%d")
            return f"{taskname} on {taskdt}"


class Session(models.Model):
    session_name = models.CharField(max_length=500,null=True,blank=True)
    ex1 = models.CharField(max_length=500, null=True,blank=True)
    ex1_time = models.IntegerField()
    ex2 = models.CharField(max_length=500, null=True,blank=True)
    ex2_time = models.IntegerField()
    ex3 = models.CharField(max_length=500, null=True,blank=True)
    ex3_time = models.IntegerField()

    def __str__(self):
        if self is not None:
            return self.session_name
    


class DailySession(models.Model):
    sessionFor = models.ForeignKey(ClaendarTask, on_delete=models.CASCADE, null=True, blank = True)
    session1_start = models.TimeField(null=True,blank=True)
    session2_start = models.TimeField(null=True,blank=True)
    session3_start = models.TimeField(null=True,blank=True)
    session1_end = models.TimeField(null=True,blank=True)
    session2_end = models.TimeField(null=True,blank=True)
    session3_end = models.TimeField(null=True,blank=True)
    session1_name = models.ForeignKey(Session, on_delete=models.CASCADE,related_name='session1',null=True,blank=True)
    session2_name = models.ForeignKey(Session, on_delete=models.CASCADE,related_name='session2',null=True,blank=True)
    session3_name = models.ForeignKey(Session, on_delete=models.CASCADE,related_name='session3',null=True,blank=True)

    def __str__(self):
        return f"{self.sessionFor}"

# @receiver(post_save, sender=ClaendarTask)
# def create_related_model(sender, instance, created, **kwargs):
#     if created:
#         DailySession.objects.create(sessionFor=instance)
    

# class FetchTask(models.Model):
#     taskFetch = models.OneToOneField(ClaendarTask, on_delete=models.CASCADE,null=True,blank=True)
#     dateFetch = models.DateField(null=True,blank=True)

#     def __str__(self):
#         return str(self.dateFetch)
    


# @receiver(post_save, sender=ClaendarTask)
# def create_related_model(sender, instance, created, **kwargs):
#     if created:
#         FetchTask.objects.create(taskFetch=instance, dateFetch=instance.taskDate)


class SuggestedVideo(models.Model):
    whichMatch = models.OneToOneField(MatchResult, on_delete=models.CASCADE, null=True, blank=True)
    vidTitle = models.CharField(max_length=255, null=True, blank=True)
    vidImg = models.CharField(max_length=5000,null=True,blank=True)
    vidLink = models.CharField(max_length=5000,null=True,blank=True)


class APIKey(models.Model):
    key = models.CharField(max_length=1000)

    def __str__(self):
        return self.key    