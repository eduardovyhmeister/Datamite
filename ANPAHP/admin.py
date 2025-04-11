from django.contrib import admin
from .models import (BSCFamily,
                     BSCSubfamily,
                     Evaluation, 
                     KPI, 
                     Objective, 
                     Criterion)

# Register your models here.
admin.site.register(BSCFamily)
admin.site.register(BSCSubfamily)
admin.site.register(Evaluation)
admin.site.register(KPI)
admin.site.register(Objective)
admin.site.register(Criterion)
