from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView,UpdateView,DeleteView
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import TodoForm
from .models import Todo
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
import json

def get_content_type_for_model(obj):
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)

def log_deletion(obj):
        from django.contrib.admin.models import DELETION, LogEntry
        return LogEntry.objects.log_action(
            user_id=1,
            content_type_id=get_content_type_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=DELETION,
        )

# Create your views here.
def homepage(request):
    #return HttpResponse('<h1>home page</h1>')
    message=""
    form=TodoForm()
    todos=Todo.objects.all().order_by('-Datetime')
    if request.method=="POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            message = 'Saved Successfully'
        form=TodoForm()
        return render(request,'todo/todo_list.html',{'form':form,'todos':todos,'message':message})
    return render(request,'todo/todo_list.html',{'form':form,'todos':todos})

class TodoDetailView(DetailView):
    model=Todo
    template_name='todo/detail.html'

class TodoUpdateView(UpdateView):
    model = Todo
    fields = '__all__'
    template_name='todo/update.html'

class TodoDeleteView(DeleteView):
    model = Todo
    template_name ='todo/delete.html'
    success_url = reverse_lazy('todo-list')

def deleteTodo(request,id):
    obj = Todo.objects.get(id=id)
    print(log_deletion(obj))
    obj.delete()
    return redirect("/")

@login_required(login_url='/admin/login/')
def adminPage(request):
    #return HttpResponse('<h1>home page</h1>')
    message=""
    form=TodoForm()
    todos=Todo.objects.all().order_by('-Datetime')
    if request.method=="POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            message = 'Saved Successfully'
        form=TodoForm()
        return render(request,'admin/admin.html',{'form':form,'todos':todos,'message':message})
    return render(request,'admin/admin.html',{'form':form,'todos':todos})

@csrf_exempt
def todoapi(request):
    if (request.method == "GET"):
        data = serializers.serialize("json", Todo.objects.all())
        return JsonResponse(json.loads(data), safe=False)
@csrf_exempt 
def todoapiid(request,pk):
    if (request.method == "GET"):
        data = serializers.serialize("json", Todo.objects.filter(id=pk))
        return JsonResponse(json.loads(data),safe=False)

from django.http import HttpResponse
import csv

def export_todos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="todos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title','Description', 'Datetime', 'Status', 'CreatedAt', 'ModifiedAt'])

    todos = Todo.objects.all().values_list('Title','Description', 'Datetime', 'Status', 'CreatedAt', 'ModifiedAt')
    for todo in todos:
        writer.writerow(todo)

    return response
