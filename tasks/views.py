import csv
import json

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import DetailView, FormView

from tasks.forms import CreateTaskBundleForm
from tasks.models import Task, TaskBundle


class TaskBundleInfoView(DetailView):
    """
    Bundle tasks info.
    """
    model = TaskBundle

    def get_context_data(self, **kwargs):
        data = super().get_context_data()

        # This data must be in context. Everything will work if we need to
        # make some refactoring in class Task
        data['status_done'] = Task.STATUS_DONE
        data['status_failed'] = Task.STATUS_FAILED

        return data


class CreateTaskBundleView(FormView):
    """
    Main form for bundle creation.
    """

    form_class = CreateTaskBundleForm
    template_name = 'tasks/taskbundle_create.html'

    def form_valid(self, form):

        bundle = TaskBundle()
        bundle.save()

        for url in form.cleaned_data['urls']:
            task = Task(link=url)
            task.bundle = bundle
            task.save()

        return HttpResponseRedirect(reverse('bundle_detail', args=[bundle.pk]))


class TaskCSVView(DetailView):
    model = Task

    def get(self, request, *args, **kwargs):
        task = self.get_object()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(slugify(task.result_title))

        writer = csv.writer(response)
        writer.writerow(['Constituency Name', 'MP Name', 'Number of Signatures'])

        for row in task.result:
            writer.writerow([row['name'], row['mp'], row['signature_count']])

        return response


class TaskStatusView(DetailView):
    model = Task

    def get(self, request, *args, **kwargs):
        task = self.get_object()

        response = JsonResponse({'status': task.status})

        return response


class TaskDiagramView(DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        task = self.get_object()

        data = [['MP', 'Percentage']]
        for row in task.result:
            signature_count = int(row['signature_count'])
            data.append([row['mp'], signature_count * 100 / task.result_signature_count])

        data_json = json.dumps(data, indent=4)

        context_data = super().get_context_data()
        context_data['data_json'] = data_json
        print(context_data['data_json'])

        return context_data
