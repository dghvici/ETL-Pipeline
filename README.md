# NC-DataEng-ETL-Project
Northcoders Data Engineering Bootcamp ETL final group project
# Lullymore-West ETL Project 

## Table of Contents
[Overview](#overview)
[Features](#features)
[Installation](#installation)
[Policies](#policies)
[Prerequisites](#prerequisites)
[Installation](#installation)
[License](#license)
[Acknowledgemnts](#acknowledgements)

## Overview 
Following an intensive training course with Northcoders, this project is the group's first attempt at setting up an ETL (extract, transform and load) pipeline. 
As part of the project we got to grips with agile working practises, running a kamban board data practises. 

# Project Summary
A project brief was supplied by northcoders to create an MVP for an 'imaginarey' company wanting to implement data practises to gain commerical insights. 

To deliever this brief, we needed to create a pipeline that is trigged by AWS CloudWatch events, uses AWS Lambda functions to perform data ingestion, transformation and load and step functions as orchetsration. 

# Key chellenges 
1. how to update the data every 30 minutes without duplication or corruption. 
2. How to satify flak8 and PEP8 standards 
3. Deploy the project as a whole with the many componets
4. Achieve 90% testing coverage (we might be a bit short)


# Features
- src: lambda ingest, transform and load python function 
- terraform: policies for S3 bucket, main, cloudwatch and state machine 
- test: unit tests for the lambda functions 
- test_utils: tests for the utility functions for the lmabda functions
- util_func: Utiliy functions for the lambda functions. 

N.B. folder ultil_func is in a layer: filepath: 
[NC-DataEng-ETL-Project/tree/main/util_func/python](https://github.com/LucyMilligan/NC-DataEng-ETL-Project/tree/main/util_func/python)


## Installation 

# Prerequisites 
- Python 3.12.7 and follow the installation below to install the required packages and modules stored in the requirements.txt file. 
- AWS account with necessary permissions
- AWS CLI configured with your credentials 
- Virtual environment (optional, but reccomneded)
- VS Code or equivalent  

# Clone the project repository 

```
git clone [NC-DataEng-ETL-Project/tree/main/util_func/python](https://github.com/LucyMilligan/NC-DataEng-ETL-Project/tree/main/util_func/python) 
```


# Create a virtual environment in VS Code 
```
python -m venv venv 
```

# Run make file 
```
run-make 
```
## License 

## Badges


## Acknowledgements
Northcoders for curating and delivering the course. 
Project partners: Iris Araneta, Callum Bain, Dani Ghinchevici, Ollie Lawn, Lucy Milligan and Joshua Sessions. 


## FAQs

# As a group what did we learn and take from this project? 

# As a group, how do we rate the poject success? 

# Individually, what do we want to build on as we move into actual real world data engineering? 

