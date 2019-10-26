# Distributed CI Feeder

## Installation on host

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

### Installation on Docker

Dci-feeder can be run from within Docker with Docker-compose.

```console
[yassine@Bouceka dci-feeder]$ cd docker-compose
[yassine@Bouceka dci-compose]$ docker-compose -f dcifeeder.yml up
```

### Test the Feeder API

```console
[yassine@Bouceka dci-feeder]$ curl -XPOST -i http://127.0.0.1:5000/rhel/rhel-8.2
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 79
Server: Werkzeug/0.16.0 Python/2.7.5
Date: Sat, 26 Oct 2019 16:25:59 GMT

{
  "event": "SYNC_STARTED", 
  "task_id": "task_id", 
  "topic": "rhel-8.2"
}
```

### Running the tests

To run the tests in the docker compose environment, you have to first log in to
the API container and run the "tox" command:

```console
[yassine@Bouceka dci-feeder]$ docker exec -it feeder_api bash
[root@73ddc020cd43 dci-feeder]# tox
```

### Workflow

  1. The client send a REST request to the Feeder API for running a sync.
     - POST /rhel/rhel-8.2 component_name=rhel-8.2231019
  2. The Feeder API receives the request and run asynchronously the sync
     through a Celery worker.
  3. Once the Celery worker finished its task it sends the result back to the Feeder API with an event key.
     - POST /rhel/_events event=SYNC_SUCCESS topic_name=rhel-8.2
  4. The Feeder API receives the event and, according to the event, could run other tasks
     asynchronously like sending notifications for instance.
