# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forager_forward',
 'forager_forward.app_clients',
 'forager_forward.app_services',
 'forager_forward.common']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.26.0,<0.27.0']

setup_kwargs = {
    'name': 'forager-forward',
    'version': '0.1.0',
    'description': 'Hunter.io v2 api implementation',
    'long_description': '# Forager clients and services\n\nA python wrapper for the Hunter.io v2 api as a client.\nEmail validation service.\n\n## Installation\n\n### Requirements\n\n    - Python 3.10\n    - httpx\n\n### To install\n\n   pip install forager_forward==0.1.0\n\n## Usage\n\nService supports next method from Hunter.io v2 api\n\n    - domain_search (with async adomain_search)\n    - email_finder (with async aemail_finder)\n    - verify_email (with async averify_email)\n    - email_count (with async aemail_count)\n    \nAdditionally, service supports crud methods for locally storing data\n\n## How to use service\n\n### Import service and instantiate it once\n\n    from forager_forward.client_initializer import ClientInitializer\n\n    initializer = ClientInitializer()\n\n    initializer.initialize_client("api_key_got_from_hunter")\n\n    initializer.initialize_async_client("api_key_got_from_hunter")\n\n    client = initializer.client\n\n    async_client = initializer.async_client\n\n\n### Once initialized somewhere in the code you can get instances in different places without additional initialization\n\n    client = ClientInitializer().client\n\n    async_client = ClientInitializer().async_client\n\n### Search addresses for a given domain\n\n    client.domain_search("www.brillion.com.ua")\n\n### Or pass company name\n\n    client.domain_search(company="Brillion", limit=20, seniority="junior")\n\n### Find email address\n\n    client.email_finder(compayny="pmr", full_name="Sergiy Petrov", raw=True)\n\n### Check email deliverabelity\n\n    client.email_verifier("a@a.com")\n\n### All data can be stored in Storage class instance. It has its own crud methods, and it is Singleton.\n\n    from forager_forward.common.storage import Storage\n\n    storage = Storage()\n\n    storage.create(some_key, some_value)\n\n    storage.update(some_key, some_value)\n\n    some_variable = storage.read(some_key)\n\n    storage.delete(some_key)\n\n### To validate emails and store validation result use email_validation_service.\n\n    from forager_forward.app_services.email_validation_service import EmailValidationService\n\n    email_validator = EmailValidationService()\n\n    email_validator.create_email_record("some_email@company.com")\n\n    email_validator.read("another@company.com")\n\n## Tests\n\n    To run test firstly you need to install test dependency, then run\n\n        pytest -cov\n',
    'author': 'victro-nuzhniy',
    'author_email': 'nuzhniyva@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/victor-nuzhniy/forager.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
