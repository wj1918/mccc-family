"""
Wrapper for loading templates from the db.
"""

import io
from django.template.base import TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader
from models import HtmlTemplate
from django.template import TemplateDoesNotExist

class Loader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        if template_name!=template_name.upper():
            raise TemplateDoesNotExist(template_name)
        try:
            tpl = HtmlTemplate.objects.get(name=template_name)
            return tpl.content, "db:{0}".format(template_name)
        except HtmlTemplate.DoesNotExist:
            raise TemplateDoesNotExist(template_name)
    load_template_source.is_usable = True