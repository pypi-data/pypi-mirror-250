from django import template
from django.urls import reverse
from django_jinja import library
from furl import furl

register = template.Library()


def add_params(url, filter):
    params = {}
    for field_name in filter.form.fields.keys():
        if field_name in filter.form.data:
            params[field_name] = filter.form[field_name].value()
    f = furl(url)
    f.set(params)
    return f.url


@library.global_function
@register.simple_tag
def tag_url(url_name, filter, tag, taggable_manager_name='tags'):
    f = furl(reverse(url_name))
    f = furl(add_params(f.url, filter))

    if f.args.getlist(taggable_manager_name):
        if str(tag.pk) not in f.args.getlist(taggable_manager_name):
            f.add({taggable_manager_name: tag.pk})
    else:
        f.add({taggable_manager_name: tag.pk})
    return f.url


@library.global_function
@register.simple_tag
def tag_count(queryset, tag, taggable_manager_name='tags'):
    return queryset.filter(**{taggable_manager_name: tag}).count()


@library.global_function
@register.simple_tag
def filter_url(url_name, filter, field_name, value):
    f = furl(reverse(url_name))
    f = furl(add_params(f.url, filter))
    f.args[field_name] = value
    return f.url


@library.global_function
@register.simple_tag
def remove_filter_url(url_name, filter, field_name):
    f = furl(reverse(url_name))
    f = furl(add_params(f.url, filter))
    del f.args[field_name]
    return f.url
