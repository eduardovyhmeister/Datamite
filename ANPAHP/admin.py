from django.contrib import admin
from .models import Evaluation, KPI, Objective, Criterion

# Register your models here.
admin.site.register(Evaluation)
admin.site.register(KPI)
admin.site.register(Objective)
admin.site.register(Criterion)
