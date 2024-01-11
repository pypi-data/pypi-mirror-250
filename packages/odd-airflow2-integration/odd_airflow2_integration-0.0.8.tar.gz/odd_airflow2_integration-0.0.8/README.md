[![PyPI version](https://badge.fury.io/py/odd-airflow2-integration.svg)](https://badge.fury.io/py/odd-airflow2-integration)

# Open Data Discovery Airflow 2 Integrator

Airflow plugin which tracks DAGs, tasks, tasks runs and sends them to the platform since DAG is run via [Airflow Listeners ](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/listeners.html)

## Requirements

* __Python >= 3.9__
* __Airflow >= 2.5.1__
* __Presence__  of an HTTP Connection with the name '__odd__'. That connection must have a __host__ property with yours
platforms host(fill a __port__ property if required) and a __password__ field with platform collectors token.
This connection MUST be represented before your scheduler is in run, we recommend using [AWS Param store](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/secrets-backends/aws-ssm-parameter-store.html), 
Azure KV or similar backends.

## Installation

The package must be installed alongside Airflow

```bash
poetry add odd-airflow2-integration
# or
pip install odd-airflow2-integration
```

## Lineage
To build a proper lineage for tasks we need somehow to deliver the information
about what are the inputs and outputs for each task. So we decided to follow the
old Airflow concepts for lineage creation and use the `inlets` and `outlets`
attributes.

So `inlets`/`outlets` attributes are being used to list Datasets' ODDRNs that
are considered to be the inputs/outputs for the task.

Example of defining `inlets` and `outlets` using TaskFlow:
```python
@task(
    task_id="task_2",
    inlets=["//airflow/internal_host/dags/test_dag/tasks/task_1", ],
    outlets=["//airflow/internal_host/dags/test_dag/tasks/task_3", ]
)
def transform(data_dict: dict):
    pass

task_2 = transform()
```
Example using Operators:
```python
task_2 = PythonOperator(
    task_id="task_2",
    python_callable=transform,
    inlets=["//airflow/internal_host/dags/test_dag/tasks/task_1", ],
    outlets=["//airflow/internal_host/dags/test_dag/tasks/task_3", ]
)
```

Also it is worth to mention that neither `inlets` nor `outlets` can not be
templated using the `template_fields` of Operators that have this option.
More information about this topic is presented in the comment section for
the following [issue](https://github.com/opendatadiscovery/odd-airflow-2/issues/8#issuecomment-1884554977).