from django.contrib import admin
from .models import Problem
from .models import Submission
# Register your models here.

admin.site.register(Problem)
admin.site.register(Submission)