import mimetypes
from django import template

register = template.Library()

@register.filter
def is_video(file_url):
    mime_type, _ = mimetypes.guess_type(file_url)
    return mime_type and mime_type.startswith('video/')