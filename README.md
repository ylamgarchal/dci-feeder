# Distributed CI Feeder

## Installation

### Install RabbitMQ server

```console
[yassine@Bouceka dci-feeder]$ sudo dnf install -y rabbitmq-server.noarch
[yassine@Bouceka dci-feeder]$ sudo systemctl start rabbitmq-server
```

RabbitMQ will listen to "localhost:5672" by default.

### Install Celery
```console
[yassine@Bouceka dci-feeder]$ sudo dnf install -y python2-celery.noarch python3-celery.noarch
```

## Run full workflow

### Run local dev server

```console
[yassine@Bouceka dci-feeder]$ ./bin/runserver.py
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

### Run local worker

```console
[yassine@Bouceka dci-feeder]$ celery -A dcifeeder.celery_app:app worker --loglevel=info

 -------------- celery@Bouceka v4.2.1 (windowlicker)
---- **** ----- 
--- * ***  * -- Linux-4.20.13-200.fc29.x86_64-x86_64-with-fedora-29-Twenty_Nine 2019-10-24 02:51:48
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         dcifeeder:0x7f7288a71c90
- ** ---------- .> transport:   amqp://guest:**@localhost:5672//
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 4 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . dcifeeder.common.tasks.notifications.send_mails
  . dcifeeder.rhel.tasks.sync.sync

[2019-10-24 02:51:48,413: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
[2019-10-24 02:51:48,422: INFO/MainProcess] mingle: searching for neighbors
[2019-10-24 02:51:49,442: INFO/MainProcess] mingle: all alone
[2019-10-24 02:51:49,454: INFO/MainProcess] celery@Bouceka ready.
```

### Test the Feeder API

```console
[yassine@Bouceka dci-feeder]$ http POST http://127.0.0.1:5000/rhel/rhel-8.2
HTTP/1.0 201 CREATED
Content-Length: 76
Content-Type: application/json
Date: Thu, 24 Oct 2019 00:53:47 GMT
Server: Werkzeug/0.14.1 Python/2.7.15

{
    "event": "SYNC_STARTED",
    "task_id": "task_id",
    "topic": "rhel-8.2"
}
```

## Workflow

  1. The client send a REST request to the Feeder API for running a sync.
     - POST /rhel/rhel-8.2 component_name=rhel-8.2231019
  2. The Feeder API receives the request and run asynchronously the sync
     through a Celery worker.
  3. Once the Celery worker finished its task it sends the result back to the Feeder API with an event key.
     - POST /rhel/_events event=SYNC_SUCCESS topic_name=rhel-8.2
  4. The Feeder API receives the event and, according to the event, could run other tasks
     asynchronously like sending notifications for instance.
