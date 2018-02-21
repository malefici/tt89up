# Test task

There are two applications based on Django and Tornado. I decided to choose tornado for sending notifications into 
browser via WebSockets. I do not want to use something like 
[Django Channels](https://channels.readthedocs.io/en/latest/) in aspect of WSGI protocol stateless. This project does 
not contain tests. 


## How to start

This demo project does not require any server in front of applications or database configuration. For testing you will 
need three terminals and virtual environment with installed dependencies. All URLs between Django and Tornado applications 
are hardcoded.

In first terminal, please, run:

```bash
./manage.py migrate
./manage.py runserver
``` 

And in second terminal we will start application based on Tornado server: 

```bash
python websockets_server.py
```

Now we can start to get data from [petitions site](https://petition.parliament.uk/) by URL 
[127.0.0.1:8000](http://127.0.0.1:8000).

After creating tasks for data aggregation, use third terminal with:

```bash
./manage.py execute_tasks
```

With this command we imitate jobs queue and processing tasks manually.


## Some words about

Long polling is a alternative for WebSockets. You can test it with stopped Tornado server.
I did not understand task variant with diagrams. I hope that it is what you want.
