Welcome to The Blue Alliance Wiki! Here are some helpful pages -

## Site Architecture & Design Docs

A guide to understanding how TBA works internally.

 - [[Architecture Overview|Architecture-Overview]]; to learn how the basics work
 - [[The Data Model|Architecture-Data-Model]]; for how the data is laid out in the DB
 - [[Caching Architecture|Architecture-Caching]]; for all the ways data is cached
 - [[Closet Skeletons|Closet-Skeletons]]; for some of the bonkers things we do deep down

## Setup

### [[Setup Guide|Setup-Guide]]

A step-by-step guide for getting The Blue Alliance up and running locally. For new contributors, this should be your first stop.

### [[Repo Setup|Repo-Setup]]

A guide for configuring The Blue Alliance repo locally in order to streamline development. This step is optional as it is not required for working in The Blue Alliance repo, but it will be helpful for contributors that plan to do frequent work in the repo.

### [[WSL Setup|WSL-Guide]]

If you are planning on developing using WSL, there are a few extra steps you'll need to take. This guide was not tested on WSL 1; we recommend updating to WSL version 2.

## Developing

### [[tba_dev_config.json|tba_dev_config]]

Documentation on configuration option for a local development container using the `tba_dev_config.json` file.

### [[Queues and defer|Queues-and-defer]]

Details on using the `defer` method to enqueue tasks to be executed asynchronously, along with notes on task queues in The Blue Alliance codebase.

### [[Redis|Redis]]

Details on how to cache data using `redis`.

### [[Development Runbook|Development-Runbook]]

Helpful commands when developing in The Blue Alliance codebase. This section includes things like how to run tests, how to seed your development environment with production data, and more!

### [[Web Dev Runbook|Web-Dev-Runbook]]

Notes for working effectively and safely in the `web` service.

### [[Py 2 -> Py 3 Migration Notes|Py2ToPy3]]

Running notes on how to migrate code from the Python 2 codebase to the new Python 3 codebase.

## Deployment

### [[Google App Engine + Firebase Setup|GAE-Firebase-Setup]]

Notes on setting up a Google App Engine instance or Firebase project for testing upstream.

### [[CI/CD Setup|CI-CD-Setup]]

Steps for setting up automatic deployment via Github Actions.

### Manual Deployment

TODO

## Maintainers

### [[Maintainers Runbook|Maintainer-Runbook]]

Runbook for maintainer tasks. A catch-all of administration information.

### [[Preparing for a New Season|New-Season]]

The years start coming and they don't stop coming. Here is a collection of notes for preparing/supporting a new season.
