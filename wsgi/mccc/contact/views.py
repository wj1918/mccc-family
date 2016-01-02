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
            if  update_invite.address!=form.cleaned_data['address']:
                update_invite.address=form.cleaned_data['address']
                changed=True
            if  update_invite.city!=form.cleaned_data['city']:
                update_invite.city=form.cleaned_data['city']
                changed=True
            if  update_invite.state!=form.cleaned_data['state']:
                update_invite.state=form.cleaned_data['state']
                changed=True
            if  update_invite.zip!=form.cleaned_data['zip']:
                update_invite.zip=form.cleaned_data['zip']
                changed=True
            if  update_invite.home_phone!=form.cleaned_data['home_phone']:
                update_invite.home_phone=form.cleaned_data['home_phone']
                changed=True
            if  update_invite.last_nm1!=form.cleaned_data['last_nm1']:
                update_invite.last_nm1=form.cleaned_data['last_nm1']
                changed=True
            if  update_invite.first_nm1!=form.cleaned_data['first_nm1']:
                update_invite.first_nm1=form.cleaned_data['first_nm1']
                changed=True
            if  update_invite.chinese_nm1!=form.cleaned_data['chinese_nm1']:
                update_invite.chinese_nm1=form.cleaned_data['chinese_nm1']
                changed=True
            if  update_invite.cell_phone1!=form.cleaned_data['cell_phone1']:
                update_invite.cell_phone1=form.cleaned_data['cell_phone1']
                changed=True
            if  update_invite.first_nm2!=form.cleaned_data['first_nm2']:
                update_invite.first_nm2=form.cleaned_data['first_nm2']
                changed=True
            if  update_invite.chinese_nm2!=form.cleaned_data['chinese_nm2']:
                update_invite.chinese_nm2=form.cleaned_data['chinese_nm2']
                changed=True
            if  update_invite.cell_phone2!=form.cleaned_data['cell_phone2']:
                update_invite.cell_phone2=form.cleaned_data['cell_phone2']
                changed=True
            
            update_invite.invite_state=UpdateInvite.SUBMITTED
            update_invite.save()
                
                
            f=Family.objects.get(id=update_invite.family.id)
            changed=False
            if f.address != update_invite.address:
                changed=True
                f.address= update_invite.address
            if f.city != update_invite.city: 
                changed=True
                f.city= update_invite.city
            if f.state != update_invite.state: 
                changed=True
                f.state= update_invite.state
            if f.zip != update_invite.zip:
                changed=True
                f.zip= update_invite.zip
            if f.home1 != update_invite.home_phone: 
                changed=True
                f.home1= update_invite.home_phone
            if changed:    
                f.save()
                
            if update_invite.person1:    
                p1=Person.objects.get(id=update_invite.person1.id)
                if p1 and p1.cphone != update_invite.cell_phone1:
                        p1.cphone = update_invite.cell_phone1
                        p1.save()
                
            if update_invite.person2:    
                p2=Person.objects.get(id=update_invite.person2.id)
                if p2 and p2.cphone != update_invite.cell_phone2:
                        p2.cphone = update_invite.cell_phone2
                        p2.save()
                
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
    