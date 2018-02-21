from django.db import models
from jsonfield import JSONField


class TaskBundle(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def get_task_ids_for_status_check(self):
        ids = []
        for task in self.task_set.all():
            if task.status not in [Task.STATUS_DONE, Task.STATUS_FAILED]:
                ids.append(task.id)

        return ids


class Task(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_FAILED = 'failed'

    status = models.CharField(max_length=11, default=STATUS_NEW, db_index=True)
    status_notes = models.TextField(null=True)

    link = models.URLField()
    result = JSONField(default=None)
    result_signature_count = models.PositiveIntegerField(null=True)
    result_title = models.CharField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    bundle = models.ForeignKey(TaskBundle, on_delete=models.CASCADE)

    def is_done(self):
        return self.status == self.STATUS_DONE

    def is_processing(self):
        return self.status not in [Task.STATUS_FAILED, self.STATUS_DONE]

    def is_failed(self):
        return self.status == Task.STATUS_FAILED
