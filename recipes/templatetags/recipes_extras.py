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


@register.filter()
def get_tags(requestget):
    return requestget.getlist('tag')


@register.filter()
def get_tags_link(request, tag):
    request_copy = request.GET.copy()
    if tag.slug in request.GET.getlist('tag'):
        filters = request_copy.getlist('tag')
        filters.remove(tag.slug)
        request_copy.setlist('tag', filters)
    else:
        request_copy.appendlist('tag', tag.slug)
    return request_copy.urlencode()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return query.urlencode()
