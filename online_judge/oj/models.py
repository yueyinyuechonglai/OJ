from django.db import models

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
