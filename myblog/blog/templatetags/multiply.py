from django import template


register = template.Library()

# custom template tag which is used in article_detail.html for calculating
# padding-left value according to comment's level
@register.simple_tag()
def multiply(level, px, *args, **kwargs):
    return level * px