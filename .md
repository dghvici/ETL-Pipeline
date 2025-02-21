https://github.com/northcoders/de-project-specification?tab=readme-ov-file -- FULL INSTRUCTIONS


SETUP:
MAKE file
REQUIREMENTS file
.env
git ignore
YAML file (something to consider later on?)



---INGESTION
Extract data:
-> Terraform code:
    1. IAM ROLES (Lambda permission, S3 permission, Cloudwatch permission, Stepfunction role)
    2. Lambda file 
    3. S3 file (creating buckets) min.2 (one for ingested data, one for transformed data)
    4. Cloud watch file
    5. Scheduler 
    6. State machine
    7. Main / provider
    8. Vars folder
    9. Backend bucket (pre-existing s3 bucket)


->A job scheduler or orchestration process to run the ingestion job and subsequent processes. You can do this with AWS Eventbridge or with a combination of Eventbridge and AWS Step Functions.
                            >>> Sprint : 13/02/2024 Currency Exchange/ Orchestration Lecture
-> Schedule to check changes

-> Save files in bucket with CSV or JSON

-> LAMBDA -> Checks for changes in the database tables, Ingests new or updated data, Log to cloud watch

-> Cloudwatch alerts (04/02/2025 Monitoring & Alterting Lecture/ Sprint: Lambda)



---TRANSFORM
LAMBDA -> A Python application to transform data landing in the "ingestion" S3 bucket and place the results in the "processed" S3 bucket. The data should be transformed to conform to the warehouse schema (see above). The job should be triggered by either an S3 event triggered when data lands in the ingestion bucket, or on a schedule.
                -> Log to cloudwatch
                -> Alert set up

-> S3 bucket for transformed data

-> Data type parquet



---LOADING
A Python application that will periodically schedule an update of the data warehouse from the data in S3. Again, status and errors should be logged to Cloudwatch, and an alert triggered if a serious error occurs.

-> Visual presentation (3rd week of project phase)


NB:--------
-> TDD for all code (test coverage should exceed 90%)
-> PEP8 compliant (ruff/black/flake8)
-> PIP audit and bandit packages
->All functions have doc strings
-> Data structure in bucket


You need to create:

A job scheduler or orchestration process to run the ingestion job and subsequent processes. You can do this with AWS Eventbridge or with a combination of Eventbridge and AWS Step Functions. - //Since data has to be visible in the data warehouse within 30 minutes of being written to the database, you need to schedule your job to check for changes frequently.- // 
An S3 bucket that will act as a "landing zone" for ingested data. - //
A Python application to check for changes to the database tables and ingest any new or updated data. It is strongly recommended that you use AWS Lambda as your computing solution. It is possible to use other computing tools, but it will probably be much harder to orchestrate, monitor and deploy. The data should be saved in the "ingestion" S3 bucket in a suitable format. Status and error messages should be logged to Cloudwatch.
A Cloudwatch alert should be generated in the event of a major error - this should be sent to email.
A second S3 bucket for "processed" data.
A Python application to transform data landing in the "ingestion" S3 bucket and place the results in the "processed" S3 bucket. The data should be transformed to conform to the warehouse schema (see above). The job should be triggered by either an S3 event triggered when data lands in the ingestion bucket, or on a schedule. Again, status and errors should be logged to Cloudwatch, and an alert triggered if a serious error occurs.
A Python application that will periodically schedule an update of the data warehouse from the data in S3. Again, status and errors should be logged to Cloudwatch, and an alert triggered if a serious error occurs.
In the final week of the course, you should be asked to create a simple visualisation such as described above. In practice, this will mean creating SQL queries to answer common business questions. Depending on the complexity of your visualisation tool, other coding may be required too.





The project is open-ended and could include any number of features, but at a minimum, you should seek to deliver the following ----MNIMUM VIABLE PORDUCT:

Two S3 buckets (one for ingested data and one for processed data). Both buckets should be structured and well-organised so that data is easy to find. Data should be immutable - i.e. once you have written data to S3, it should not be amended or over-written. You should create new data files containing additions or amendments.
A Python application that continually ingests all tables from the totesys database (details below). The data should be saved in files in the "ingestion" S3 bucket in a suitable format. The application must:
operate automatically on a schedule
log progress to Cloudwatch
trigger email alerts in the event of failures
follow good security practices (for example, preventing SQL injection and maintaining password security)
A Python application that remodels at least some of the data into a predefined schema suitable for a data warehouse and stores the data in Parquet format in the "processed" S3 bucket. The application must:
trigger automatically when it detects the completion of an ingested data job
be adequately logged and monitored
populate the dimension and fact tables of a single "star" schema in the warehouse (see details below)
A Python application that loads the data into a prepared data warehouse at defined intervals. Again the application should be adequately logged and monitored.
A visual presentation that allows users to view useful data in the warehouse (more on this below).


---- HISTORY

Your warehouse should contain a full history of all updates to facts. For example, if a sales order is created in totesys and then later updated (perhaps the units_sold field is changed), you should have two records in the fact_sales_order table. It should be possible to see both the original and changed number of units_sold. It should be possible to query either the current state of the sale, or get a full history of how it has evolved (including deletion if applicable).

It is not necessary to do this for dimensions (which should not change very much anyway). The warehouse should just have the latest version of the dimension values. However, you might want to keep a full record of changes to dimensions in the S3 buckets.


https://github.com/northcoders/de-project-specification?tab=readme-ov-file