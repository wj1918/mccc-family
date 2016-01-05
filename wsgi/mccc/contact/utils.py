import logging
import random
import string
import datetime
from logging_tree import printout
from django.conf import settings
from django.shortcuts import get_object_or_404
from family.models import Family
from family.models import Person
from contact.models import UpdateInvite
from .tokens import access_token_generator
from profile.models import UserProfile
from django.core.mail import send_mail
from htmltemplate.models import HtmlTemplate
from django.template import engines
from django.contrib.auth.models import (User, Group,)
from django.db import connection


def login_exists(person):
    return UserProfile.objects.filter(person__id=person.id,user__is_active=True,user__is_staff=True).exists() or User.objects.filter(email__iexact=person.email).exists()

def random_string():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))    

def create_update_invite(queryset):
    count=0    
    for o in queryset:
        m=UpdateInvite()
        family=Family.objects.get(id=o.family_id)
        m.family=family
        m.full_address=o.address
        m.home_phone=o.home_phone
        m.last_nm1=o.last_nm
        m.first_nm1=o.first_nm
        m.chinese_nm1=o.chinese_nm
        m.worship=o.worship
        m.first_nm2=o.wf_first
        m.chinese_nm2=o.wf_chinese_nm
        m.dir_type=UpdateInvite.COUPLE if ( o.wf_first or o.wf_chinese_nm)  else UpdateInvite.SINGLE
        m.address=family.address
        m.city=family.city
        m.state=family.state
        m.zip=family.zip
        
        p1=None
        if(o.first_nm and o.last_nm):
            p1=Person.objects.get(family__id=o.family_id, first=o.first_nm, last=o.last_nm)
        elif (o.chinese_nm):
            p1=Person.objects.get(family__id=o.family_id, chinese=o.chinese_nm)

        if(p1):
            m.person1=p1
            m.email1="{0} {1} <{2}>".format(p1.first,p1.last,p1.email) if p1.email else None
            m.cell_phone1=p1.cphone
            m.fellowship_nm1=p1.fellowship

        p2=None    
        if(o.wf_first):
            p2=Person.objects.get(family__id=o.family_id, first=o.wf_first)
        elif (o.wf_chinese_nm):
            p2=Person.objects.get(family__id=o.family_id, chinese=o.wf_chinese_nm)

        if(p2):
            m.person2=p2
            m.email2="{0} {1} <{2}>".format(p2.first,p2.last,p2.email) if p2.email else None
            m.cell_phone2=p2.cphone
            m.fellowship_nm2=p2.fellowship

        if(m.email1 or m.email2):
            m.invite_email=';'.join([x for x in (m.email1,m.email2) if x])
            token = access_token_generator.make_token() 
            m.access_token=token
            m.expiration_date=datetime.date.today()+ datetime.timedelta(days=settings.ACCESS_TOKEN_EXPIRATION_DAYS)
            m.save()
            count+=1

    return count


def send_email(queryset):
    for o in queryset:
        send_mail('Your Email subject', 'Your Email message.', settings.EMAIL_HOST_USER, [o.invite_email], fail_silently=False)
        
def get_email_content(update_invite,request):
    ht=HtmlTemplate.objects.get(name="INVITE_EMAIL").content
    django_engine = engines['django']
    template = django_engine.from_string(ht)
    context={}
    context.update(update_invite.__dict__)
    context.update({"request":request})
    return template.render(context)

def parse_email(email):
    lines =email.splitlines(True)
    subject=None
    to=None
    cc=None
    bcc=None
    content=None
    begin_content=False
    for line in lines:
        if not begin_content:
            if line.startswith('SUBJECT:'):
                subject=line[8:].strip()
                begin_content=False
            elif line.startswith('TO:'):
                to=line[3:].strip()
                begin_content=False
            elif line.startswith('CC:'):
                cc=line[3:].strip()
                begin_content=False
            elif line.startswith('BCC:'):
                bcc=line[4:].strip()
                begin_content=False
            elif line.strip()=="":
                begin_content=False
            else:
                begin_content=True
        if begin_content:
            content= content+ line if content else line
    return subject,to,cc,bcc,content

def save_contact(token, form):
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

def create_user_profile(person):
    
    u=User(username="{0}.{1}".format(person.last.lower(),person.first.lower()),
        first_name=person.first,
        last_name=person.last,
        email=person.email,
        is_staff=True,
        is_active=True,)
    u.save()
        
    g = Group.objects.get(name='MCCC Member') 
    g.user_set.add(u)
    g.save()
    
    cursor = connection.cursor()
    cursor.execute("insert into user_profile(person_id,user_id) value (%s,%s)", [person.id,u.id])    

def signup_by_email(update_invite):
    count=0
    if update_invite.person1 and not login_exists(update_invite.person1) and update_invite.person1.email:
        create_user_profile(update_invite.person1)
        count+=1
    if update_invite.person2 and not login_exists(update_invite.person2) and update_invite.person2.email:
        create_user_profile(update_invite.person2)
        count+=1
    return count
    
def create_logins(queryset):
    count=0    
    for update_invite in queryset:
        count+=signup_by_email(update_invite)
    return count
