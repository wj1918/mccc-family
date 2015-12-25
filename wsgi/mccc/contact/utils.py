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

logger = logging.getLogger("django")
#printout()

def random_string():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))    

def create_update_invite(queryset):
    logger.info("in create_update_invite.")
    
    count=0    
    for o in queryset:
        m=UpdateInvite()
        m.update_family=Family.objects.get(id=o.family_id)
        m.address=o.address
        m.home_phone=o.home_phone
        m.last_nm1=o.last_nm
        m.first_nm1=o.first_nm
        m.chinese_nm1=o.chinese_nm
        m.worship=o.worship
        m.first_nm2=o.wf_first
        m.chinese_nm2=o.wf_chinese_nm
    
        p1=None
        if(o.first_nm and o.last_nm):
            p1=Person.objects.get(family__id=o.family_id, first=o.first_nm, last=o.last_nm)
        else:
            if(o.chinese_nm):
                p1=Person.objects.get(family__id=o.family_id, chinese=o.chinese_nm)

        if(p1 and p1.email):
            m.invite_person=p1
            m.invite_email=p1.email
            m.email1=p1.email
            m.cell_phone1=p1.cphone
            token = access_token_generator.make_token() 
            m.access_token=token
            m.expiration_date=datetime.date.today()+ datetime.timedelta(days=settings.ACCESS_TOKEN_EXPIRATION_DAYS)
            m.save()
            count+=1
            
        p2=None    
        if(o.wf_first):
            p2=Person.objects.get(family__id=o.family_id, first=o.wf_first)
        else:
            if(o.wf_chinese_nm):
                p2=Person.objects.get(family__id=o.family_id, chinese=o.wf_chinese_nm)

        if(p2 and p2.email):
            m.invite_person=p2
            m.invite_email=p2.email
            m.email2=p2.email
            m.cell_phone2=p2.cphone
            token = access_token_generator.make_token() 
            m.access_token=token
            m.expiration_date=datetime.date.today()+ datetime.timedelta(days=settings.ACCESS_TOKEN_EXPIRATION_DAYS)
            m.pk=None
            m.save()
            count+=1

    return count
