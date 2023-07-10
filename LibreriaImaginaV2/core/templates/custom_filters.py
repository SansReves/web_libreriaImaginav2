from django import template

register = template.Library()

@register.filter
def get_from_session(session, key):
    return session.get(key)
