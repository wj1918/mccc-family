
from django.http import HttpResponse
from children.models import CmMaster 
from django.shortcuts import render
import datetime

def attendancesheet(request,grade,month,num_weeks):
    firstday=datetime.date(datetime.date.today().year,int(month),1)
    sunday=firstday + datetime.timedelta(days=-firstday.weekday()-1, weeks=1)
    sundays=[]
    for i in range(int(num_weeks)):
        sundays.append("{:%m/%d}".format(sunday))
        sunday=sunday+ datetime.timedelta(weeks=1)
        
    children_list = CmMaster.objects.filter(ssgrade=grade,ssactive='Active')
    context ={'children_list': children_list, "grade":grade, "sundays":sundays } 
    return render(request, 'children/attendancesheet.html', context)
