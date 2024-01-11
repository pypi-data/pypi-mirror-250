# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_airflow2_integration', 'odd_airflow2_integration.dir']

package_data = \
{'': ['*']}

install_requires = \
['odd-models>=2.0.12,<3.0.0']

entry_points = \
{'airflow.plugins': ['OddPlugin = odd_airflow2_integration.plugin:OddPlugin']}

setup_kwargs = {
    'name': 'odd-airflow2-integration',
    'version': '0.0.8',
    'description': 'ODD integration with Airflow',
    'long_description': '[![PyPI version](https://badge.fury.io/py/odd-airflow2-integration.svg)](https://badge.fury.io/py/odd-airflow2-integration)\n\n# Open Data Discovery Airflow 2 Integrator\n\nAirflow plugin which tracks DAGs, tasks, tasks runs and sends them to the platform since DAG is run via [Airflow Listeners ](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/listeners.html)\n\n## Requirements\n\n* __Python >= 3.9__\n* __Airflow >= 2.5.1__\n* __Presence__  of an HTTP Connection with the name \'__odd__\'. That connection must have a __host__ property with yours\nplatforms host(fill a __port__ property if required) and a __password__ field with platform collectors token.\nThis connection MUST be represented before your scheduler is in run, we recommend using [AWS Param store](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/secrets-backends/aws-ssm-parameter-store.html), \nAzure KV or similar backends.\n\n## Installation\n\nThe package must be installed alongside Airflow\n\n```bash\npoetry add odd-airflow2-integration\n# or\npip install odd-airflow2-integration\n```\n\n## Lineage\nTo build a proper lineage for tasks we need somehow to deliver the information\nabout what are the inputs and outputs for each task. So we decided to follow the\nold Airflow concepts for lineage creation and use the `inlets` and `outlets`\nattributes.\n\nSo `inlets`/`outlets` attributes are being used to list Datasets\' ODDRNs that\nare considered to be the inputs/outputs for the task.\n\nExample of defining `inlets` and `outlets` using TaskFlow:\n```python\n@task(\n    task_id="task_2",\n    inlets=["//airflow/internal_host/dags/test_dag/tasks/task_1", ],\n    outlets=["//airflow/internal_host/dags/test_dag/tasks/task_3", ]\n)\ndef transform(data_dict: dict):\n    pass\n\ntask_2 = transform()\n```\nExample using Operators:\n```python\ntask_2 = PythonOperator(\n    task_id="task_2",\n    python_callable=transform,\n    inlets=["//airflow/internal_host/dags/test_dag/tasks/task_1", ],\n    outlets=["//airflow/internal_host/dags/test_dag/tasks/task_3", ]\n)\n```\n\nAlso it is worth to mention that neither `inlets` nor `outlets` can not be\ntemplated using the `template_fields` of Operators that have this option.\nMore information about this topic is presented in the comment section for\nthe following [issue](https://github.com/opendatadiscovery/odd-airflow-2/issues/8#issuecomment-1884554977).',
    'author': 'Open Data Discovery',
    'author_email': 'pypi@opendatadiscovery.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/opendatadiscovery/odd-airflow-2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
