from .forms import SiteUserCreationForm, SiteUserChangeForm
from .models import Vacancy, Popularity, Geography, Skills, SiteUser, ProfSkills
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Класс для настройки отображения пользователей в админке Django
class CustomUserAdmin(UserAdmin):
    # Используемые формы для добавления и изменения пользователя
    add_form = SiteUserCreationForm
    form = SiteUserChangeForm

    # Отображаемые поля в списке пользователей
    list_display = ('username', 'email', 'group', 'is_staff', 'is_active')
    # Фильтры для списка пользователей
    list_filter = ('group', 'is_staff', 'is_active')

    # Группировка полей при редактировании пользователя
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('group', 'is_staff', 'is_active')}),
    )


# Класс для настройки отображения вакансий в админке Django
class VacancyAdmin(admin.ModelAdmin):
    # Связываем класс с моделью Vacancy
    model = Vacancy
    # Отображаемые поля в списке вакансий
    list_display = ('title', 'description', 'skills', 'company', 'salary', 'area_name', 'published_at')
    # Поля, по которым можно производить поиск
    search_fields = ('title', 'skills', 'company', 'salary', 'area_name', 'published_at')


# Классы для настройки отображения различных моделей в админке Django
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


class ProfSkillsAdmin(admin.ModelAdmin):
    model = ProfSkills
    list_display = ('title', 'image', 'table')
    search_fields = ('title',)


# Регистрация моделей в админке с использованием созданных выше классов настроек
admin.site.register(SiteUser, CustomUserAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Popularity, PopularityAdmin)
admin.site.register(Geography, GeographyAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(ProfSkills, ProfSkillsAdmin)