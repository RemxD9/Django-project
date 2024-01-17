from django.contrib import admin
from .models import Vacancy, Popularity, Geography, Skills


# Register your models here.
class VacancyAdmin(admin.ModelAdmin):
    model = Vacancy
    list_display = ('title', 'description', 'skills', 'company', 'salary', 'area_name', 'published_at')
    search_fields = ('title', 'skills', 'company', 'salary', 'area_name', 'published_at')


class PopularityAdmin(admin.ModelAdmin):
    model = Popularity
    list_display = ('title', 'image', 'table')
    search_fields = ('title',)


class GeographyAdmin(admin.ModelAdmin):
    model = Geography
    list_display = ('title', 'image', 'table')
    search_fields = ('title',)


class SkillsAdmin(admin.ModelAdmin):
    model = Skills
    list_display = ('title', 'image', 'table')
    search_fields = ('title',)


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Popularity, PopularityAdmin)
admin.site.register(Geography, GeographyAdmin)
admin.site.register(Skills, SkillsAdmin)
