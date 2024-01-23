from django.contrib import admin
from django.urls import path
from Analytics import views
from django.conf import settings
from django.conf.urls.static import static

# Список URL-шаблонов, направляющих запросы на соответствующие представления
urlpatterns = [
    path('', views.registration_view, name='registration_view'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('login/', views.login_view, name='login_view'),
    path('home/', views.main_page, name='home'),
    path('popularity/', views.popularity, name='Востребованность'),
    path('geography/', views.geography, name='География'),
    path('skills/', views.skills, name='Навыки'),
    path('lastvacancies/', views.last_vacancies, name='Последние вакансии'),
    path('admin/', admin.site.urls, name='admin'),
]

# Добавление URL-шаблонов для обслуживания медиа-файлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)