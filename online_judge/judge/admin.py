from django.contrib import admin
from django.forms import inlineformset_factory

from .models import Problem , Solution, Test


class TestInline(admin.TabularInline):
    model = Test
    extra = 1

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [TestInline]


admin.site.register(Solution)

