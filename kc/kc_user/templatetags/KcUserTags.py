from django import template
from django.template.loader import get_template
from kc_user.config import KC_MANAGED_APPS


register = template.Library()


class KcUserManagementLoader(template.Node):
    def render(self, context):
        u = context['user']
        output = ''
        for app_name in KC_MANAGED_APPS:
            if u.privilege(app_name):
                t = get_template('kc_%s/mgt.html' % app_name)
                output += t.render(context)
        return output


@register.tag()
def kc_management_loader(parser, token):
    return KcUserManagementLoader()


class KcUserQuickLink(template.Node):
    def render(self, context):
        app_name = context.get('active', None)
        if app_name is None or app_name == 'user':
            return ''
        u = context['user']
        if u.privilege(app_name):
            t = get_template('kc_%s/quicklink.html' % app_name)
            return t.render(context)
        return ''


@register.tag()
def kc_user_quicklink(parser, token):
    return KcUserQuickLink()