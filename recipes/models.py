from django.db import models
from django.contrib.auth import get_user_model


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


User = get_user_model()


class Ingridient(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    dimension = models.CharField(max_length=250)


class Recipe(models.Model):
    TAGS = (
        ('BR', 'Завтрак'),
        ('LU', 'Обед'),
        ('DN', 'Ужин')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    picture = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(verbose_name='Описание')
    ingridients = models.ManyToManyField(Ingridient, through='Ingridients',
                                         related_name='ingridients')
    Tag = models.CharField(max_length=2, choices=TAGS)
    time_cooking = models.SmallIntegerField(
        verbose_name='Время приготовления (мин)')
    slug = models.SlugField(db_index=True, )


class Ingridients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingridients = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
