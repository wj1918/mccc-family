import logging
import random
import string
import datetime
from logging_tree import printout
from django.conf import settings
from family.models import Family
from family.models import Person
from contact.models import UpdateInvite
from .tokens import access_token_generator
from profile.models import UserProfile
from django.core.mail import send_mail
from htmltemplate.models import HtmlTemplate
from django.template import engines


logger = logging.getLogger("django")
#printout()

def login_exists(person):
    return UserProfile.objects.filter(person__id=person.id,user__is_active=True,user__is_staff=True).count()>0

def random_string():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))    

def create_update_invite(queryset):
    logger.info("in create_update_invite.")
    
    count=0    
    for o in queryset:
        m=UpdateInvite()
        m.family=Family.objects.get(id=o.family_id)
        m.address=o.address
        m.home_phone=o.home_phone
        m.last_nm1=o.last_nm
        m.first_nm1=o.first_nm
        m.chinese_nm1=o.chinese_nm
        m.worship=o.worship
        m.first_nm2=o.wf_first
        m.chinese_nm2=o.wf_chinese_nm
        m.dir_type=UpdateInvite.COUPLE if ( o.wf_first or o.wf_chinese_nm)  else UpdateInvite.SINGLE

        p1=None
        if(o.first_nm and o.last_nm):
            p1=Person.objects.get(family__id=o.family_id, first=o.first_nm, last=o.last_nm)
        elif (o.chinese_nm):
            p1=Person.objects.get(family__id=o.family_id, chinese=o.chinese_nm)

        if(p1):
            m.person1=p1
            m.email1="{0} {1} <{2}>".format(p1.first,p1.last,p1.email) if p1.email else None
            m.cell_phone1=p1.cphone

        p2=None    
        if(o.wf_first):
            p2=Person.objects.get(family__id=o.family_id, first=o.wf_first)
        elif (o.wf_chinese_nm):
            p2=Person.objects.get(family__id=o.family_id, chinese=o.wf_chinese_nm)

        if(p2):
            m.person2=p2
            m.email2="{0} {1} <{2}>".format(p2.first,p2.last,p2.email) if p2.email else None
            m.cell_phone2=p2.cphone

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
    ht=HtmlTemplate.objects.get(name="INVITE_EMAIL").content;
    django_engine = engines['django']
    template = django_engine.from_string(ht)
    context={}
    context.update(update_invite.__dict__)
    context.update({"request":request})
    return template.render(context)