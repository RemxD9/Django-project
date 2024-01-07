from django.db import models


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.TextField()
    company = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    publication_date = models.DateTimeField()

    def __str__(self):
        return self.title
