import json
from urllib import error
from urllib import request, parse

from django.core.management.base import BaseCommand
from lxml import html

from tasks.models import Task


class TaskExecutionException(Exception):
    pass


def execute_task(task):
    task.status = Task.STATUS_IN_PROGRESS
    task.save()

    # //*[@id="content"]/h1\

    try:
        handler = request.urlopen(task.link)
        res_html = handler.read()

        # https://petition.parliament.uk/petitions/200292
        handler = request.urlopen(task.link + '.json')
        res_json = handler.read()

        # let's parse JSON
        parsed_json = json.loads(res_json.decode("utf-8"))
    except Exception as e:

        task.status = Task.STATUS_FAILED
        task.status_notes = '{}, {}'.format(type(e), e)

        raise TaskExecutionException
    else:

        task.result = parsed_json['data']['attributes']['signatures_by_constituency']
        task.result_signature_count = parsed_json['data']['attributes']['signature_count']

        # here can be exceptions too, it's can be covered with different handling scenarios
        tree = html.fromstring(res_html.decode("utf-8"))
        task.result_title = tree.xpath('/html/head/title')[0].text[:-12]

        task.status = Task.STATUS_DONE
    finally:
        task.save()


class Command(BaseCommand):
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

        if options['list']:
            for task in tasks:
                self.stdout.write('Task "%s"' % task.pk)
            return

        for task in tasks:
            try:
                execute_task(task)
            except TaskExecutionException:
                self.stdout.write(self.style.ERROR('Task "%s" failed' % task.pk))
            else:
                self.stdout.write('Task "%s" completed' % task.pk)

            try:
                post_data = parse.urlencode({'task_id': task.pk, 'data': json.dumps({'status': task.status})}).encode()
                handler = request.urlopen('http://127.0.0.1:8078/notifications/notify', data=post_data)
                handler.read()
            except error.URLError or error.HTTPError:
                self.stdout.write(self.style.NOTICE('Failed to notice about task execution'))
