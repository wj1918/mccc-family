"""
Wrapper for loading templates from the db.
"""

import io

from django.template.base import TemplateDoesNotExist

from django.template.loaders.base import Loader as BaseLoader

from models import HtmlTemplate
from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader

class Loader(BaseLoader):
    is_usable = True
    def load_template_source(self, template_name, template_dirs=None):
        try:
            key, ext = template_name.split('.')
            attr = {
                'html': 'html_content',
                'txt': 'text_content',
            }[ext]
            tpl = HtmlTemplate.objects.get(key=key)
            return (getattr(tpl, attr), repr(tpl))
        except:
            raise TemplateDoesNotExist