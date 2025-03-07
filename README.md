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
(Acknowledgemnts)

## Overview 
Following a successful training course with Northcoders, this project is the group's first attempt at setting up an ETL (extract, load and ) pipeline. 

The intention was to ingest data from an RDS database into an S3 bucket. 
The pipeline is triggered by AWS CloudWatch Events and uses AWS Lambda functions to perform data ingestion, transformation and load. 


## Features
- src: lambda ingest, transform and load python function 
- terraform: policies for S3 bucket, main, cloudwatch and state machine 
- test: tests for the lambda function and 
- test_utils: tests for the utility functions for the lmabda functions
- util_func: Utiliy functions for the lambda functions. 

N.B. folder ultil_func is in a layer: filepath: 
[NC-DataEng-ETL-Project/tree/main/util_func/python](https://github.com/LucyMilligan/NC-DataEng-ETL-Project/tree/main/util_func/python)


## Policies 



## Prerequisites 
- Python 3.12.7 and follow the installation below to install the required packages and modules stored in the requirements.txt file. 
- AWS account with necessary permissions
- AWS CLI configured with your credentials 
- Virtual environment (optional, but reccomneded)
- VS Code or equivalent  

## Installation 

# Clone the repository 
git clone [NC-DataEng-ETL-Project/tree/main/util_func/python](https://github.com/LucyMilligan/NC-DataEng-ETL-Project/tree/main/util_func/python)

# Create a virtual environment in VS Code 
python -m venv venv 

# Run make file 
run-make 

## License 

## Acknowledgements
Northcoders for leading the course. 
Project partners: Iris Araneta, Callum Bain, Dani Ghinchevici, Ollie Lawn, Lucy Milligan, Joshua Sessions. 




