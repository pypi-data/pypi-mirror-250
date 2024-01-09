# Forager clients and services

A python wrapper for the Hunter.io v2 api as a client.
Email validation service.

## Installation

### Requirements

    - Python 3.10
    - httpx

### To install

   pip install forager_forward==0.1.1

## Usage

Service supports next method from Hunter.io v2 api

    - domain_search (with async adomain_search)
    - email_finder (with async aemail_finder)
    - verify_email (with async averify_email)
    - email_count (with async aemail_count)
    
Additionally, service supports crud methods for locally storing data

## How to use service

### Import service and instantiate it once

    from forager_forward.client_initializer import ClientInitializer

    initializer = ClientInitializer()

    initializer.initialize_client("api_key_got_from_hunter")


    client = initializer.client


### Once initialized somewhere in the code you can get instances in different places without additional initialization

    client = ClientInitializer().client


### Search addresses for a given domain

    client.domain_search("www.brillion.com.ua")

### Or pass company name

    client.domain_search(company="Brillion", limit=20, seniority="junior")

### Find email address

    client.email_finder(compayny="pmr", full_name="Sergiy Petrov", raw=True)

### Check email deliverabelity

    client.email_verifier("a@a.com")

### All data can be stored in Storage class instance. It has its own crud methods, and it is Singleton.

    from forager_forward.common.storage import Storage

    storage = Storage()

    storage.create(some_key, some_value)

    storage.update(some_key, some_value)

    some_variable = storage.read(some_key)

    storage.delete(some_key)

### To validate emails and store validation result use email_validation_service.

    from forager_forward.app_services.email_validation_service import EmailValidationService

    email_validator = EmailValidationService()

    email_validator.create_email_record("some_email@company.com")

    email_validator.read("another@company.com")

## Tests

    To run test firstly you need to install test dependency, then run

        pytest -cov
