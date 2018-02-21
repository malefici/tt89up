import json
from urllib import error
from urllib import request, parse

from django.core.management.base import BaseCommand
from lxml import html

from tasks.models import Task


class TaskExecutionException(Exception):
    """
    Custom exception for handling exceptions from our code.
    """
    pass


def execute_task(task):
    """
    Task execution. Requesting and parsing.

    :param task: Task for execution
    :type task: Task
    """

    # mark task as processing
    task.status = Task.STATUS_IN_PROGRESS
    task.save()

    try:
        # get html page with petition description
        handler = request.urlopen(task.link)
        res_html = handler.read()

        # get JSON data for petition
        handler = request.urlopen(task.link + '.json')
        res_json = handler.read()

        # let's parse JSON
        parsed_json = json.loads(res_json.decode("utf-8"))

        # get petition name
        tree = html.fromstring(res_html.decode("utf-8"))
        petition_name = tree.xpath('/html/head/title')[0].text[:-12]
    except Exception as e:
        # Here I handle all exceptions. For more detailed logging or special logic we can except different exceptions
        # with their handling.

        task.status = Task.STATUS_FAILED
        task.status_notes = '{}, {}'.format(type(e), e)

        raise TaskExecutionException
    else:
        # save all parsed data in model

        task.result = parsed_json['data']['attributes']['signatures_by_constituency']
        task.result_signature_count = parsed_json['data']['attributes']['signature_count']

        task.result_title = petition_name

        task.status = Task.STATUS_DONE
    finally:
        task.save()


class Command(BaseCommand):
    """
    Command for processing task. Here we emulate RQ.
    """
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all tasks for ',
        )

    def handle(self, *args, **options):

        tasks = Task.objects.filter(status=Task.STATUS_NEW)

        if not tasks:
            self.stdout.write('There is no tasks for execution')
            return

        # list tasks for processing
        if options['list']:
            for task in tasks:
                self.stdout.write('Task "%s"' % task.pk)
            return

        for task in tasks:
            # task execution with exceptions handling
            try:
                execute_task(task)
            except TaskExecutionException:
                self.stdout.write(self.style.ERROR('Task "%s" failed' % task.pk))
            else:
                self.stdout.write('Task "%s" completed' % task.pk)

            # notify user via WebSockets about task processing
            try:
                post_data = parse.urlencode({'task_id': task.pk, 'data': json.dumps({'status': task.status})}).encode()
                request.urlopen('http://127.0.0.1:8078/notifications/notify', data=post_data)

                # here can be logic for Tornado application response

            except error.URLError or error.HTTPError:
                self.stdout.write(self.style.NOTICE('Failed to notice about task execution'))
