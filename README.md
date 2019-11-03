# Distributed CI Feeder

## All in one setup

### Running the dci feeder on Docker compose

Dci-feeder can be run from within Docker with Docker-compose.

```console
[yassine@Bouceka dci-feeder]$ docker-compose  up
```

### Test the feeder API

On the host you can run the following command:

```console
[yassine@Bouceka dci-feeder]$ http POST http://127.0.0.1:5000/rhel/sync topic=rhel-8.2
HTTP/1.0 201 CREATED
Content-Length: 108
Content-Type: application/json
Date: Sat, 26 Oct 2019 16:25:59 GMT
Server: Werkzeug/0.16.0 Python/2.7.5

{
    "event": "SYNC_STARTED",
    "task_id": "task_id",
    "topic": "rhel-8.2"
}
```

### Running the tests

To run the tests you have to first log in to
the "feeder_api" container and run the "tox" command:

```console
[yassine@Bouceka dci-feeder]$ docker exec -it feeder_api bash
[root@73ddc020cd43 dci-feeder]# tox
```

### Workflow

  1. The client send a REST request to the Feeder API for running a sync.
     - POST /rhel/sync topic=rhel-8.2 component_name=rhel-8.2231019
  2. The Feeder API receives the request and run asynchronously the sync
     through a Celery worker.
  3. Once the Celery worker finished its task it sends the result back to the Feeder API with an event key.
     - POST /rhel/_events event=SYNC_SUCCESS topic=rhel-8.2
  4. The Feeder API receives the event and, according to the event, could run other tasks
     asynchronously like sending notifications for instance.
