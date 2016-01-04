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
        tried = []
        try:
            tpl = HtmlTemplate.objects.get(name=template_name)
            return tpl.content, "db:{0}".format(template_name)
        except HtmlTemplate.DoesNotExist:
            tried.append(template_name)
        if tried:
            error_msg = "Tried %s" % tried
        else:
            error_msg = ("Your template directories configuration is empty. "
                         "Change it to point to at least one template directory.")
        raise TemplateDoesNotExist(error_msg)
    load_template_source.is_usable = True