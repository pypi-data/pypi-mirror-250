# Overview

This `cli` folder contains code for our linea-cli.
Users of this software will `pip install linea-cli` and use this client from their laptop locally

## How to use

The user need to get access token from linea UI (e.g. dev.linea.ai) first and configure linea-cli to use the credential

### Init

```
# linea init
Your Linea API address (e.g. dev.linea.ai) :: localhost
Your API token: < type in the token here>
```

This will create a linea.config file under `LINEA_HOME`, by default it is `HOME/.linea`

### Get pipeline details

```
# linea list-pipelines
-----
results like this ==>
[
  {
        'name': 'fraud_detection_stream_data',
        'author': '',
        'maintainer': '',
        'last_execution': '',
        'next_execution': '2023-12-18T05:34:07.143493+00:00',
        'health': '',
        'orchestrator': 'default-airflow',
        'orchestrator_url': 'http://localhost/airflow',
        'description': '',
        'frequency': 'an hour',
        'code_link': '/tmp/airflow/dags',
        'last_updated': '2023-12-13T22:32:43.460913',
        'remote_url': ''
    },
    {
        'name': 'fraud_detection_stream_fraud',
        'author': '',
        'maintainer': '',
        'last_execution': '',
        'next_execution': '2023-12-18T05:34:06.736915+00:00',
        'health': '',
        'orchestrator': 'default-airflow',
        'orchestrator_url': 'http://localhost/airflow',
        'description': '',
        'frequency': 'a day',
        'code_link': '/tmp/airflow/dags',
        'last_updated': '2023-12-13T22:32:44.514551',
        'remote_url': ''
    }
]

```

### Get task details

```
# linea list-executions fraud_detection_dashboard
-----
results like this ==>
[
    {
        'name': 'scheduled__2023-12-17T03:24:42.253908+00:00',
        'started': '2023-12-18T03:28:30.856181+00:00',
        'ended': '2023-12-18T03:28:34.825636+00:00',
        'status': 'failed',
        'code_link': ''
    },
    {
        'name': 'scheduled__2023-12-16T03:24:42.253908+00:00',
        'started': '2023-12-17T03:30:16.865230+00:00',
        'ended': '2023-12-17T03:30:20.814001+00:00',
        'status': 'failed',
        'code_link': ''
    }
]
```

### Create LE (TBD)
