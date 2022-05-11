from django.urls import path
from todo import views


urlpatterns =[
    path("",views.homepage,name="todo-list"),
    path('padmin/',views.adminPage,name='admin-page'),
    path('detail/<pk>/', views.TodoDetailView.as_view(),name='todo-detail'),
    path('update/<pk>/', views.TodoUpdateView.as_view(),name='todo-update'),
    path('delete/<id>/', views.deleteTodo,name='todo-delete'),
    path('api/', views.todoapi,name='api'),
    path('api/<int:pk>/', views.todoapiid),
    path('exportcsv/',views.export_todos_csv)
]
