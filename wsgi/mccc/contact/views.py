from django.core import mail
from django.views.generic.edit import FormView
from .forms import ContactForm
from django.views.generic import TemplateView
from oauthemail.utils import get_user_auth_backend
from django.utils.html import escape
from django.http import (Http404, HttpResponse,)
from django.shortcuts import get_object_or_404
from .tokens import access_token_generator
from .models import UpdateInvite
from .utils import get_email_content
from family.models import (Family,Person,)
from django.conf import settings

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
        initial.update(update_invite.__dict__)
    
        return initial
    
    def form_valid(self, form):
            # This method is called when valid form data has been POSTed.
            # It should return an HttpResponse.
            token=self.kwargs.get("token")
            update_invite = get_object_or_404(UpdateInvite, access_token=token)
            changed=False
            f=Family.objects.get(id=update_invite.family.id)
            changed=False
            changed_value={}
            if f.address != form.cleaned_data['address']:
                changed=True
                f.address= form.cleaned_data['address']
                changed_value["address"]=form.cleaned_data['address']
            if f.city != form.cleaned_data['city']:
                changed=True
                f.city= form.cleaned_data['city']
                changed_value["city"]=f.city
            if f.state != form.cleaned_data['state']: 
                changed=True
                f.state= form.cleaned_data['state']
                changed_value["state"]=f.state
            if f.zip != form.cleaned_data['zip']:
                changed=True
                f.zip= form.cleaned_data['zip']
                changed_value["zip"]=f.zip
            if f.home1 != form.cleaned_data['home_phone']: 
                changed=True
                f.home1= form.cleaned_data['home_phone']
                changed_value["home_phone"]=f.home1
            if changed:    
                f.save()
                
            if update_invite.person1:    
                p1=Person.objects.get(id=update_invite.person1.id)
                if p1 and p1.cphone != form.cleaned_data['cell_phone1']:
                        p1.cphone = form.cleaned_data['cell_phone1']
                        changed_value["cell_phone1"]=p1.cphone
                        p1.save()
                
            if update_invite.person2:    
                p2=Person.objects.get(id=update_invite.person2.id)
                if p2 and p2.cphone != form.cleaned_data['cell_phone2']:
                        p2.cphone = form.cleaned_data['cell_phone2']
                        changed_value["cell_phone2"]=p2.cphone
                        p2.save()
            
            update_invite.comment=repr({"changed":changed_value, "cleaned_data":form.cleaned_data})       
            update_invite.invite_state=UpdateInvite.SUBMITTED
            update_invite.save()

            return HttpResponse("Updated successfully.")    

    def get_context_data(self, **kwargs):
            context = super(PublicContactView, self).get_context_data(**kwargs)
            token=self.kwargs.get("token")
            """check token expiration date"""
            if not access_token_generator.check_token(token):
                raise Http404()    
            update_invite = get_object_or_404(UpdateInvite, access_token=token)
            if update_invite.invite_state!= UpdateInvite.SENT:
                raise Http404()    
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
            if ui.invite_state==UpdateInvite.ACTIVE:
                email_content=get_email_content(ui,request)
                to_email= request.user.email if settings.DEBUG else ui.invite_email
                mail.EmailMessage('Church Directroy', email_content, to=[to_email], connection=connection).send()
                ui.invite_state=UpdateInvite.SENT
                ui.save()
        return HttpResponse("{0} email sent.".format(len(ids)))
    # return render(request, self.template_name)        
    