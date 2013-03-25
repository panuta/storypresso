# -*- encoding: utf-8 -*-

from django import template
register = template.Library()

from common import utilities


# DATE TIME ############################################################################################################

@register.filter(name='format_datetime')
def format_datetime(datetime):
    return utilities.format_full_datetime(datetime)


@register.filter(name='format_abbr_datetime')
def format_abbr_datetime(datetime):
    return utilities.format_abbr_datetime(datetime)


@register.filter(name='format_date')
def format_date(datetime):
    return utilities.format_full_date(datetime)


@register.filter(name='format_abbr_date')
def format_abbr_date(datetime):
    return utilities.format_abbr_date(datetime)