from django.views.generic.edit import FormView
from .forms import ContactForm
from django.views.generic import TemplateView
from oauthemail.utils import get_user_auth_backend
from django.utils.html import escape

class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        return super(ContactView, self).form_valid(form)

class EmailPreviewView(TemplateView):
    template_name = "contact/preview.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EmailPreviewView, self).get_context_data(**kwargs)
        context['ids'] = self.request.session.get("ids",[])
        backend=get_user_auth_backend(self.request)
        # context['backend'] = escape(repr(b))
        context['backend'] = backend
        context['user'] = self.request.user
        return context    
    