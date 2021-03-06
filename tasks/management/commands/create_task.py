from django.core.management import BaseCommand

from tasks.models import Task, TaskBundle


class Command(BaseCommand):
    """
    Command for task manual creating.
    """
    help = 'Create task'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str, help='Needed URL')

    def handle(self, *args, **options):
        # here everything easy: one bundle with one task

        bundle = TaskBundle()
        bundle.save()

        task = Task(link=options['link'])
        task.bundle = bundle

        task.save()

        self.stdout.write('Task pk {}, bundle pk {}'.format(str(task.pk), str(bundle.pk)))
