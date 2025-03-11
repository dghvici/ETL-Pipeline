
# NC-DataEng-ETL-Project

Northcoders Data Engineering Bootcamp group project

## Lullymore-West ETL Project

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [License](#license)
- [Acknowledgemnts](#acknowledgements)
- [Review](#review)

## Overview

Following an intensive 10 week "Data Engineering in Python" training course with Northcoders, this project is the group's first attempt at setting up an ETL (extract, transform and load) pipeline. As part of the project, alongside developing technical skills, we got to grips with agile working practices, including utilising a kanban board.

### Project Summary

A project brief was supplied by Northcoders to create a minimum viable product (MVP) of an ETL pipeline for a fictional company 'Totesys', in order for them to gain commerical insights. The pipeline should extract data from an operational database, archive it in a data lake and make it available in a remodelled data warehouse. The databases and lambda functions are hosted in the cloud, using Amazon Web Services (AWS).

To deliever this brief, we used Terraform to create the AWS infrastructure as code. We created an ETL pipeline that is trigged by Eventbridge and
uses AWS Lambda functions to perform the data ingestion into an S3 bucket, transformation of data and loading of data into the warehouse.

### Key challenges

Although we made good progress on the project, we didn't quite complete the brief within the given time of two weeks. The majority of the AWS infrasture can be succesfully deployed with data ingested successfully, however the load function is not fully complete and thus full automation of the MVP is not complete.

Some of the key challenges included:

1. Deploying the project successfully as a whole with the many components.
2. Learning and adopting good engineering practices, such as creating and merging git branches, satisfying PEP8 standards, achieving 90% testing coverage and GitHub Actions workflow.
3. How to update the data every 30 minutes without duplication or corruption.
4. Setting up suitable development, testing and production environments and deploying this in the pipeline.
5. Testing functions that interact with operational databases.


### Repo structure

- src: lambda ingest, transform and load python function.
- terraform: policies for S3 bucket, main, Lambda functions, Cloudwatch, Secrets Manager and Evenbridge.
- test: unit tests for the lambda functions.
- test_utils: tests for the utility functions.
- util_func: Utiliy functions for the lambda functions.

N.B. folder ultil_func is in a layer: filepath:
[NC-DataEng-ETL-Project/tree/main/util_func/python](https://github.com/LucyMilligan/NC-DataEng-ETL-Project/tree/main/util_func/python)

## Installation

To install and explore our project please follow this step-by-step guide.

### Prerequisites

- Python 3.12.7 and follow the installation below to install the required packages and modules stored in the requirements.txt file.
- AWS account with necessary permissions
- AWS CLI configured with your credentials
- Virtual environment (optional, but recommeded)
- VS Code or equivalent

### Clone the project repository

```bash
git clone https://github.com/LucyMilligan/NC-DataEng-ETL-Project/tree/main/util_func/python
```

### Create a virtual environment in VS Code

```bash
python -m venv venv
```

### Install requirements

```bash
make requirements
```

### Run tests and checks

```bash
make run-security
make run-checks
```

### Deploy to AWS

On a git push or a pull request, the project is deployed via GitHub Actions workflow (as defined in the .github/workflow/deploy.yml file).

To deploy locally, follow these steps:

```bash
terraform init
terraform plan
terraform apply
```

To tear down the AWS insfrastructure:

```bash
terraform destroy
```

## License

MIT Licence.

## Acknowledgements

Northcoders for curating and delivering the course.

Project group: Iris Araneta, Callum Bain, Dani Ghinchevici, Ollie Lawn, Lucy Milligan and Joshua Sessions.

## Review

### What did we learn and take from this project?

We learnt about good data engineering practices and got to grips with git branching, creating pull requests and communicating between the team. We also put into practice the technical knowledge we'd learnt throughout the bootcamp, delving deeper into some topics bringing it together for a single purpose.

We also learnt that things often take longer than expected - if we anticipate a job will take about half an hour, realitisly that will quickly turn into three hours!

A big take away was that it is often easier to start simply and build complexity, rather than start adding complexity straight away.

### As a group, how do we rate the poject success?

It's a shame we didn't finish, but we are proud of what we've learnt and how we worked together.

### What do we want to learn more about?

Getting all the moving parts successfully working together.
