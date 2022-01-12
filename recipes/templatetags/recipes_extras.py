from django import template

register = template.Library()


@register.simple_tag()
def declination(qty):
    if 4 < qty % 100 < 20 or qty % 10 in [0, 5, 6, 7, 8, 9]:
        return 'рецептов...'
    if 1 < qty % 10 < 5:
        return 'рецепта...'
    else:
        return 'рецепт...'
