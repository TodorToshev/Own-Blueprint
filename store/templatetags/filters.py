from django import template

register = template.Library()

#returns range in order to work w/ 'for' loop for star rating
@register.filter(name='times') 
def times(number):
    return range(round(number))

#returns the rest of that range for 'fa-star-o empty' class
@register.filter(name='rest')
def rest(number):
    return range(5 - round(number))