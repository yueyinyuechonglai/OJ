from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
    prob_id = models.IntegerField(default=0)
    title = models.CharField(max_length=30)
    time_lim = models.IntegerField()
    mem_lim = models.IntegerField()
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    example_inp = models.TextField()
    exmaple_outp = models.TextField()
    data_input = models.FileField()
    data_output = models.FileField()

    def add_problem(self):
        self.save()

class MyUser(User):
    introduction = models.TextField()

class Submission(models.Model):
    submit_count = 0
    subm_id = models.IntegerField(default=0)
    prob_id = models.IntegerField(default=0)
    time = models.DateTimeField('add_time',auto_now_add = True)
    value = models.TextField()
    user = models.CharField(max_length=20)
