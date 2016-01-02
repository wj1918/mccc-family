from django.core import mail
from django.views.generic.edit import FormView
from .forms import ContactForm
from django.views.generic import TemplateView
from oauthemail.utils import get_user_auth_backend
from django.utils.html import escape
from .models import UpdateInvite
from .utils import get_email_content
from django.http import (
    Http404, HttpResponse,
)
from django.shortcuts import get_object_or_404
from .tokens import access_token_generator

class ContactView(FormView):
    template_name = 'contact/update.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        return super(ContactView, self).form_valid(form)

class PublicContactView(FormView):
    template_name = 'contact/update.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        return super(PublicContactView, self).form_valid(form)
        
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(PublicContactView, self).get_initial()
    
        token=self.kwargs.get("token")
        update_invite = get_object_or_404(UpdateInvite, access_token=token)
        initial['address']=update_invite.family.address
        initial['city']=update_invite.family.city
        initial['state']=update_invite.family.state
        initial['zip']=update_invite.family.zip
        initial.update(update_invite.__dict__)
    
        return initial
        
    def get_context_data(self, **kwargs):
            context = super(PublicContactView, self).get_context_data(**kwargs)
            token=self.kwargs.get("token")
            """check token expiration date"""
            if not access_token_generator.check_token(token):
                raise Http404()    
            update_invite = get_object_or_404(UpdateInvite, access_token=token)
            context.update(update_invite.__dict__)
            context.update({"request":self.request})
            return context

class EmailPreviewView(TemplateView):
    template_name = "contact/preview.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EmailPreviewView, self).get_context_data(**kwargs)
        ids=self.request.session.get("ids",[])
        first_id=self.request.session.get("first_id")
        ui=UpdateInvite.objects.get(id=first_id);
        
        backend =get_user_auth_backend(self.request)
        email_content=get_email_content(ui,self.request)
        
        context['ids'] = self.request.session.get("ids",[])
        context['email_list'] = self.request.session.get("email_list",[])
        context['backend'] = backend
        context['user'] = self.request.user
        context['update_invite'] = ui
        context['email_content'] = email_content
        return context    
        
    def post(self, request, *args, **kwargs):
        idsstr=request.POST.get("ids","")
        ids=idsstr.split(",")
        connection= mail.get_connection("oauthemail.smtp.OauthEmailBackend", user=request.user)
        for id in ids:
            ui=UpdateInvite.objects.get(id=id);
            email_content=get_email_content(ui,request)
            mail.EmailMessage('Church Directroy', email_content, to=[ui.invite_email], connection=connection).send()
        return HttpResponse("{0} email sent.".format(len(ids)))
    # return render(request, self.template_name)        
    