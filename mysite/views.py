from typing import Dict, Any

from django.shortcuts import render
from django.http import Http404
from django.template import loader
from django.http import HttpResponse
from .models import Person, Feedback,MY_UTIL
from .forms import BlogCommentsForm
from django.shortcuts import redirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
import cx_Oracle
import json
def index(request):
    if request.method == "POST":
        form = BlogCommentsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
           # post.id = request.id
           # post.feed = request.feed
            post.save()
            return redirect('index')
    else:
        person_list = Person.objects.order_by('id')#[:5]
        feedback_list = Feedback.objects.order_by('-id')[:1]
        template = loader.get_template('mysite/index.html')
        context = {
            'person_list': person_list,
            'feedback_list': feedback_list,
            'index_page': 'active',
                  }
    return HttpResponse(template.render(context, request))

def about(request):
    context = {"about_page": "active"}  # new info here
    return render(request, 'mysite/about.html', context)

def proc(request, *callback_args, **callback_kwargs):
    with connection.cursor() as cursor:
        cursor.execute("select * from sephiroth.sem_obs where OGAC_YMD >= '20191101'")
        #obs_list = cursor.fetchone()
        #print(obs_list)
        class CursorByName():
            def __init__(self, cursor):
                self._cursor = cursor
            def __iter__(self):
                return self
            def __next__(self):
                row = self._cursor.__next__()
                return {description[0]: row[col] for col, description in enumerate(self._cursor.description)}
        obs_list  = CursorByName(cursor)
        for row in  CursorByName(cursor):
         obs_list.append(row)

         print(obs_list)
    context = {"proc_page": "active",
               "obs_list": obs_list,
               }
    return render(request,'mysite/ProcedureConn.html',context)

@csrf_exempt
def proc1(request):
    if request.is_ajax() or request.method == "POST":
            my_util = MY_UTIL()
            res = my_util.getData()
          #  return HttpResponse(res)
            return HttpResponse(json.dumps({'list_data': res}), content_type="application/json")
    else:
            my_util = MY_UTIL()
            res = my_util.getData()
            context = {
                'data_list': res,
            }
            return render(request, 'mysite/ProcedureConn.html',context)


def feedback_new(request):
    if request.method == "POST":
        form = BlogCommentsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.id = request.id
            post.feed = request.feed
            post.save()
            return redirect('index', pk=post.pk)
    else:
        form = BlogCommentsForm()
    return render(request, 'mysite/index.html', {'form': form})

def ajax_test(request):
    if request.is_ajax():
        message = "Đây là ajax"
    else:
        message = "Không phải ajax"
    return HttpResponse(message)