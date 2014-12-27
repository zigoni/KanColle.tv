from importlib import import_module
from django import template
from django.template.loader import get_template


register = template.Library()


class KcUserQuickLink(template.Node):
    def render(self, context):
        active = context.get('active', None)
        if active is None or active == 'user':
            return ''

        try:
            app = import_module('kc_%s.lib' % active)
        except ImportError:
            print(context['active'])
            return ''

        if app.check_privilege(context['user']):
            t = get_template('kc_%s/quicklink.html' % active)
            return t.render(context)
        return ''


@register.tag()
def kc_user_quicklink(parser, token):
    return KcUserQuickLink()