from django.shortcuts import render


def main_page(request):
    return render(request, 'index.html')


def popularity(request):
    return render(request, 'index.html')


def geography(request):
    return render(request, 'index.html')


def skills(request):
    return render(request, 'index.html')


def last_vacancies(request):
    return render(request, 'index.html')
