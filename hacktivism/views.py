from django.template.loader import get_template
from django.template import Template, Context
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
import datetime
import os
from forms import ContactForm
from forms import Submit_Defacements_Form, Defacements_Form
from defacements.models import Notifier, Defacements

def default(request):
    return render_to_response('index.html')
    #return HttpResponse(fp.read())
    
    

def deface(request):
    #defacements = Defacements.objects.all()[:20]
    now = datetime.datetime.now()
    defacements = Defacements.objects.filter(time__year=now.year, \
                                             time__month=now.month, \
                                             time__day=now.day )

    list_defacements = []
    list_notifier = []
    for item in defacements:
        dict_item = model_to_dict(item)
        dict_item['notifier'] = item.notifier.name
        dict_item['time'] = str(item.time.time())
        #dict_item['time'] = item.time.isoformat()
        list_defacements.append(dict_item)
        #list_notifier.append(item.notifier.name)
    #list_defacements = Defacements.objects.all()[:20].values()
    
    return render_to_response('deface.html',\
                              {"defacements": list_defacements , \
                               "notifier": list_notifier }
                              )

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {"current_date":now})
    #return render_to_response('mypage.html', {'current_section':'current_section', 'title':'title'})
    
def hours_ahead(request, offset, offset1) :
    try :
        offset = int(offset)
    except ValueError :
        raise Http404()
    #assert False
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render_to_response('hour_offset.html', {'hour_offset':dt })

## using a form in a view
def justest(request):
    values = request.META.items()

    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v) )
    return HttpResponse("<table>%s</title>" % html)

def search_form(request):
    return render_to_response("search_form.html")

from defacements.models import Notifier
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        notifier = Notifier.objects.filter(name__icontains=q)
        return render_to_response('search_results.html',
            {'Notifier': notifier, 'query': q})
    else:
        return render_to_response('search_form.html', {'error': True})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('/thanks')
    else:
        form = ContactForm()
    return render_to_response('contact_form.html',{'form':form} )


def submit(request):
    if request.method == 'POST':
        form = Submit_Defacements_Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try :
                n = Notifier.objects.get(name=cd['notifier'])
            except Notifier.DoesNotExist:
                n = Notifier(name=cd['notifier'], e_mail=cd['e_mail'])
                n.save()
            d = Defacements(notifier = n, \
                            notifier_words = cd['notifier_words'], \
                            full_path = cd['full_path'])
            d.save()
            print cd['notifier']
            return HttpResponseRedirect('thanks')
    else:
        form = Submit_Defacements_Form()
    return render_to_response('submit.html', {'form':form})

# 2013-11-30 02:50
#from django.core.mail import send_mail
#from django.http import HttpResponseRedirect
#def contact(request):
    #errors = []
    #if request.method == 'POST':
        #if not request.POST.get('subject', ''):
            #errors.append('Enter a subject.')
        #if not request.POST.get('message', ''):
            #errors.append('Enter a message.')
        #if request.POST.get('email') and '@' not in request.POST['email']:
            #errors.append('Enter a valid e-mail address.')
        #if not errors:
            ##send_mail(
                ##request.POST['subject'],
                ##request.POST['message'],
                ##request.POST.get('email', 'noreply@example.com'), 
                ##['siteowner@example.com'],
            ##)
            #return HttpResponseRedirect('index')
    #return render_to_response('contact_form.html', {
        #'errors':errors,
        #'subject': request.POST.get('subject', ''),
        #'message': request.POST.get('message', ''),
        #'email': request.POST.get('email', ''),
    #})