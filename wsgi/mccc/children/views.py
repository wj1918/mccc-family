
from django.http import HttpResponse
from children.models import CmMaster 
from django.shortcuts import render
import datetime
from django.contrib.auth.decorators import login_required

@login_required
def attendancesheet(request,grade,month,num_weeks):
    firstday=datetime.date(datetime.date.today().year,int(month),1)
    sunday=firstday + datetime.timedelta(days=-firstday.weekday()-1, weeks=1)
    sundays=[]
    for i in range(int(num_weeks)):
        sundays.append("{:%m/%d}".format(sunday))
        sunday=sunday+ datetime.timedelta(weeks=1)
    
    grades=grade.split("+")    
    children_list = CmMaster.objects.filter(ssgrade__in=grades,ssactive='Active').order_by('ssgrade')
    context ={'children_list': children_list, "grade":grade, "sundays":sundays } 
    return render(request, 'children/attendancesheet.html', context)
