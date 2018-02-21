from django.urls import path

from tasks.views import TaskBundleInfoView, CreateTaskBundleView, TaskCSVView, TaskStatusView, TaskDiagramView

urlpatterns = [
    path('bundle/create', CreateTaskBundleView.as_view(), name='bundle_create'),
    path('bundle/<int:pk>/', TaskBundleInfoView.as_view(), name='bundle_detail'),
    path('csv/<int:pk>/', TaskCSVView.as_view(), name='task_csv'),
    path('diagram/<int:pk>/', TaskDiagramView.as_view(), name='task_diagram'),
    path('task-status/<int:pk>/', TaskStatusView.as_view(), name='task_status'),
]
