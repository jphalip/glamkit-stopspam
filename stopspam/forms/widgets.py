from django import forms
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _, get_language
from django.utils.safestring import mark_safe


# RECAPTCHA widgets
class RecaptchaResponse(forms.Widget):

    def render(self, *args, **kwargs):
        from recaptcha.client import captcha as recaptcha
        custom_translations_str = ''
        if self.custom_translations:
            custom_translations_str = 'custom_translations : {\n'
            for key, value in self.custom_translations.items():
                custom_translations_str += '\n%s: "%s",' % (key, force_unicode(value))
            custom_translations_str = custom_translations_str[:-1]  # Remove the last comma
            custom_translations_str += '},'
        recaptcha_options = """
        <script>
            var RecaptchaOptions = {
                theme: '%s',
                lang: '%s',
                %s
                custom_theme_widget: '%s'
            };
        </script>
        """ % (
            self.theme,
            get_language()[0:2],
            custom_translations_str,
            'recaptcha_widget' if self.theme == 'custom' else ''
            )
        return mark_safe(recaptcha_options + recaptcha.displayhtml(self.public_key))


class RecaptchaChallenge(forms.Widget):
    is_hidden = True
    def render(self, *args, **kwargs):
        return ""



# Honeypot widget -- most automated spam posters will check any checkbox
# assuming it's an "I accept terms and conditions" box
class HoneypotWidget(forms.CheckboxInput):
    is_hidden = True
    def render(self, *args, **kwargs):
        wrapper_html = '<div style="display:none"><label for="id_accept_terms">' + _('Are you a robot?') + '</label>%s</div>'
        return mark_safe(wrapper_html % super(HoneypotWidget, self).render(*args, **kwargs))