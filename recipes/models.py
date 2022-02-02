from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.author.id, filename)


def get_full_name(self):
    if self.first_name:
        return f'{self.first_name} {self.last_name}'
    else:
        return self.username


User.add_to_class("__str__", get_full_name)

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
    slug = models.SlugField(
        'Слаг для шаблонов',
        unique=True,
    )

    class Meta:
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
        verbose_name='Теги',
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

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingridient',
        verbose_name='Рецепт'
    )
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        related_name='recipe_ingridient',
        verbose_name='Ингридиент'
    )
    quantity = models.SmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингридиенты рецепта'
        verbose_name_plural = 'Ингридиенты рецептов'


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


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        null=True,
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        null=True,
        verbose_name='Пользователь'
    )

    def __str__(self):
        return f'{self.recipe.title}, {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'user'],
                                    name='unique_favorites')
        ]
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'


class ShopList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shop_list',
        null=True,
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_list',
        null=True,
        verbose_name='Пользователь'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'user'],
                                    name='unique_shop_list')
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
