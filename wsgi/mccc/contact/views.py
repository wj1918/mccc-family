from django.core import mail
from django.views.generic.edit import FormView
from .forms import ContactForm
from django.views.generic import TemplateView
from oauthemail.utils import get_user_auth_backend
from django.utils.html import escape
from django.http import (Http404, HttpResponse, HttpResponseRedirect,)
from django.shortcuts import get_object_or_404
from .tokens import access_token_generator
from .models import UpdateInvite
from .utils import get_email_content
from .utils import save_contact
from .utils import signup_by_email
from family.models import (Family,Person,)
from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from django.core.urlresolvers import reverse

class ContactUpdateView(FormView):
    template_name = 'DIRECTORY_UPDATE_FORM'
    form_class = ContactForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        return super(ContactUpdateView, self).form_valid(form)
        
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(ContactUpdateView, self).get_initial()
    
        token=self.kwargs.get("token")
        update_invite = get_object_or_404(UpdateInvite, access_token=token)
        initial.update(update_invite.__dict__)
    
        return initial
    
    def form_valid(self, form):
            # This method is called when valid form data has been POSTed.
            # It should return an HttpResponse.
            token=self.kwargs.get("token")
            self.validate_token(token)
            save_contact(token,form)
            return HttpResponse("Updated successfully.")    

    def get_context_data(self, **kwargs):
            context = super(ContactUpdateView, self).get_context_data(**kwargs)
            token=self.kwargs.get("token")
            """check token expiration date"""
            update_invite=self.validate_token(token)
            context.update(update_invite.__dict__)
            context.update({"request":self.request})
            return context

    def validate_token(self,token):
            if not access_token_generator.check_token(token):
                raise Http404()    
            update_invite = get_object_or_404(UpdateInvite, access_token=token)
            if update_invite.invite_state!= UpdateInvite.SENT:
                raise Http404()  
                
            return update_invite

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
            if ui.invite_state==UpdateInvite.ACTIVE:
                email_content=get_email_content(ui,request)
                to_email= request.user.email if settings.DEBUG else ui.invite_email
                mail.EmailMessage('Church Directroy', email_content, to=[to_email], connection=connection).send()
                ui.invite_state=UpdateInvite.SENT
                ui.save()
        return HttpResponse("{0} email sent.".format(len(ids)))

class SignupConfirmView(View):
    def get(self, request, *args, **kwargs):
        token=self.kwargs.get("token")
        update_invite=self.validate_token(token)
        context={"num_email":update_invite.invite_email.count(";")+1}
        context.update(update_invite.__dict__)
        return render(request, 'SIGNUP_PAGE',context)

    def post(self, request, *args, **kwargs):
        token=self.kwargs.get("token")
        update_invite=self.validate_token(token)
        signup_by_email(update_invite)
        url="/member/member/mcccdir/"
        return HttpResponseRedirect(url)

    def validate_token(self,token):
            if not access_token_generator.check_token(token):
                raise Http404()    
            update_invite = get_object_or_404(UpdateInvite, access_token=token)
            if not(update_invite.invite_state== UpdateInvite.SUBMITTED or  update_invite.invite_state== UpdateInvite.SENT):
                raise Http404()  
            return update_invite
