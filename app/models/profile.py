from django.db import models


class Profile(models.Model):
    login = models.CharField('Логин', max_length=200)  # noqa WPS432
    commits = models.IntegerField('Количество коммитов', default=0)
    pull_requests = models.IntegerField('Количество pr', default=0)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.login
