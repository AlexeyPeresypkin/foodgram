from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


User = get_user_model()


class Ingridient(models.Model):
    title = models.CharField(
        max_length=250, verbose_name='Название'
    )
    dimension = models.CharField(
        max_length=250,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Игридиенты'


class Recipe(models.Model):
    TAGS = (
        ('BR', 'Завтрак'),
        ('LU', 'Обед'),
        ('DN', 'Ужин')
    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='автор',
                               related_name='recipes'
                               )
    title = models.CharField(
        max_length=250, verbose_name='наименование'
    )
    image = models.ImageField(
        upload_to=user_directory_path,
        verbose_name='Изображение'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    ingridients = models.ManyToManyField(
        Ingridient,
        through='RecipeIngredient',
        related_name='ingridients'
    )
    Tag = models.CharField(
        max_length=2, choices=TAGS
    )
    time_cooking = models.SmallIntegerField(
        verbose_name='Время приготовления (мин)'
    )
    slug = models.SlugField(
        db_index=True,
    )
    pub_date = models.DateField(
        auto_now_add=True,
        blank=True,
        verbose_name='Дата публикации',
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingridient',
    )
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        related_name='recipe_ingridient',
    )
    quantity = models.SmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество',
    )


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')  # подписчик
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')  # автор

    def __str__(self):
        return f'Автор: {self.author}, подписчик: {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_follow'
            ),
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(user=models.F('author'))
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
