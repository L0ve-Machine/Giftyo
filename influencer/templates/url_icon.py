from django import template
import re

register = template.Library()

@register.simple_tag
def detect_icon(url):
    icons = {
        'youtube': 'youtube',
        'note.com': 'note',
        'facebook': 'facebook',
        'line.me': 'line',
        'linktr.ee': 'linktree',
        'lit.link': 'litlink',
    }

    for key, name in icons.items():
        if re.search(key, url):
            return name
    return 'link'  # デフォルトアイコン
