import markdown as md

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.utils.safestring import SafeText, mark_safe

register = template.Library()


def n2br(value):
    if not isinstance(value, SafeText):
        value = escape(value)
    value = value.replace("\n", "<br>")
    return mark_safe(value)


register.filter("n2br", n2br)


@register.filter("startswith")
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter
def in_favs(user, playlist_pk):
    return user.liked_playlists.filter(pk=playlist_pk).exists()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=["markdown.extensions.fenced_code"])
