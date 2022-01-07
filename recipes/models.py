from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.author.id, filename)


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


class Tags(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Тег',
    )
    checkbox_style = models.CharField(
        max_length=20,
        blank=True
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
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
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Тег',
        related_name='tags'
    )
    time_cooking = models.SmallIntegerField(
        verbose_name='Время приготовления (мин)',
        validators=[MinValueValidator(1)],
    )
    slug = models.SlugField(
        db_index=True,
    )
    pub_date = models.DateField(
        auto_now_add=True,
        blank=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)


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
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower')  # подписчик
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
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


