# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dubo',
 'dubo.api_client',
 'dubo.api_client.api',
 'dubo.api_client.api.dubo',
 'dubo.api_client.api.enterprise',
 'dubo.api_client.api.sdk',
 'dubo.api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['altair>=5.0.1,<6.0.0',
 'attrs>=21.3.0',
 'httpx>=0.20.0,<0.25.0',
 'pandas>=2.0.0,<3.0.0',
 'pydeck>=0.8.0,<0.9.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'sqlglot>=18.15.0,<19.0.0']

setup_kwargs = {
    'name': 'dubo',
    'version': '0.2.13',
    'description': 'Analytics made simple',
    'long_description': "dubo\n====\n\nThe Dubo SDK lets you interact with databases and data documentation via natural language. Use it with internal tools like Slackbots, within your company's ChatGPT plugin, or in your product directly.\n\nTo get started, check out the [documentation](https://docs.dubo.gg).\n\n## Developing for the Dubo SDK\n\n### Generating the API Client\n\nAn api client can be generated to access the dubo API, it is located in the `/dubo/api_client` folder:\n\n```shell\njust generate-api-client\n```\n\nMore info can be found in the README file inside the `api-client-generator` folder.\n\n### Generating Documentation\n\n```shell\njust generate-doc\n```\n",
    'author': 'Andrew Duberstein',
    'author_email': 'ajduberstein@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
