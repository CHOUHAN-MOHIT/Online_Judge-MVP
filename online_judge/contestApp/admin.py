from django.contrib import admin
from django.forms import inlineformset_factory

from .models import Contest , ContestProblem , Scorecard


class ProblemInline(admin.TabularInline):
    model = ContestProblem
    extra = 1
    
@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    inlines = [ProblemInline]

admin.site.register(Scorecard)