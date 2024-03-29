# POC Machine Learning Platform

## About

This is a poc of a machine learning platform built on top of FastAPI utilzing PyTorch and deployed onto AWS resources.


The goal was to allow users to via RESTful APIs to:

1. ingest their training data into the system
2. define a PyTorch model that could be trained 
3. run a training job with the model and training data at hand
4. save the model
5. run an inference job with real data to get a prediction with a given model classifier

## Example Workflow

1. Create the model defintion resembling the type of PyTorch layers to be built.

```shell
curl --location 'http://localhost:80/training-models' \
--header 'Content-Type: application/json' \
--data '{
    "name": "diabetes_model",
    "training_data_location": "s3://location",
    "t_dep_column": "diabetes",
    "layers": [
        {
            "training_type": "Linear",
            "in_layers": 13,
            "out_layers": 50
        },
        {
            "training_type": "Linear",
            "in_layers": 50,
            "out_layers": 25
        },
        {
            "training_type": "Linear",
            "in_layers": 25,
            "out_layers": 1
        }
    ]
}'
```

2. Store a training set

```shell
curl --location 'http://localhost:80/training-set/' \
--form 'file=@"/Users/nardoarevalo/Desktop/Diabetes ANN/normalized_diabetes_data_set.csv"'
```

3. Train and store a model with a stored training set

```shell
curl --location 'http://localhost:80/job/training' \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "diabetes_model",
    "data_set_name": "normalized_diabetes_data_set.csv"
}'
```

4. Given a stored trained model, run inference with a given data set

```shell
curl --location 'http://localhost:80/job/training' \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "diabetes_model",
    "data_set_name": "test_set.csv"
}'
```

## Setup

1. Set env variables for s3 connection and mysql database.
```shell
export MYSQL_DB=test;
export MYSQL_HOST=localhost;
export MYSQL_PASS=my-secret-pw;
export MYSQL_USER=root;
export S3_BUCKET_TRAINING_SETS=nardosbucket14;
export STORE_IN_S3=1
```

2. Install dependencies

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

3. Run alembic migrations

```shell
alembic upgrade head
```

4. Run Application
```shell
uvicorn app.main:app --reload
```

5. Optional - Cloudformation Deployment to AWS

After deployed once for Cloudformation, you will need to change the bucket name in the following
files.

`aws/scripts/after-install.sh` -> `line 7`
`.github/workflows/deploy.yml` -> `line 12`

## Swagger Docs

After you run the application you can find the docs located at the following url.
```shell
localhost:80/docs
```

## Architecture Considerations

![Blank diagram - Page 1.png](Blank%20diagram%20-%20Page%201.png)

### Infrastructure as Code (IoC)

Although I've used Terraform in the past, I really like being able to go to the console access Cloudformation and delete a
whole stack with the click of a button. Sometimes deleting resources via Terraform can get unruly and I wanted the ease AWS
provides with Cloudformation so opted for using it as a solution to hasten development.

### RESTful APIs

To make development smooth, FastAPI was chosen as a server to build on top of with Python.
I wanted these apis to be responsive with minimal delays. Between the choices of AWS Lambda, Auto Scaling EC2 groups, and an EKS cluster I opted for 
an autoscaling groups. Although Lambdas have warmers to keep them responsive the size of dependencies for this project with pandas, pytorch, etc was simply too big for the maximum size a lambda could hold.
An EKS cluster had too much overhead cost for a individual developer to maintain so an autoscaling group seemed like the most reasonable route for this project.


### Training Jobs

In practice, I am aware that a training job could take hours if not days to complete through a set of data. Even though
my project isn't handling anything like this type of data, I wanted to build something that could handle that kind of job.
Keeping the jobs on the EC2 instances themselves wouldn't be viable as the apis need to be responsible enough to not go over
1000 ms at max of response time. AWS Batch is a managed service that could handle this work and minimize my costs by not
maintaining infra for the compute resources. Furthermore, you can deploy onto Fargate which further reduces my cost for the actual
compute time that the instances are working.

### Storage
The trained models, and training data need a place to live so AWS S3 is the perfect choice for storage. Although the test 
files I was working with were only a few megabytes in size, I know this solution could scale to store 1000's of GBs if needed.

### MetaData Storage
A MySQL database hosted on AWS RDS was the solution I chose to be able to query jobs easily based off other values. I did not
want to opt in for using a NoSQL database when I do think the relations between entities would matter in the future to build
complex queries.

## CICD

![Blank diagram - Page 2.png](Blank%20diagram%20-%20Page%202.png)

### Continuous Integration
The build and test portions of CICD I left to Github to handle. Github Actions provides an easy way to build docker images, 
build artifacts and ship them off to use within another service to handle the deployment. I left building the docker image
that handles training jobs within AWS Batch, creating the resources on AWS that are used for hosting via Cloudformation, and 
sending the deployment call to AWS Deployment up to Github Actions. It would further be used to create artifacts to ship to
AWS S3 to be picked up by AWS Codedeploy if needed and run any integration and unit tests for every build of a main branch. 

### Continuous Deployment
After a successful build finishes, we need to 
1. deploy the new version of the application to the ec2 instances of the auto-scaling group, 
2. update the database with alembic revisions. 

I left this work up to AWS Code Deploy. Code deploy makes it really easy
to make changes to EC2 instances without needed to handle the SSH work yourself and running a few scripts within the instances to
stop an existing running instance, handle the installation, star the new version of the app, and validate the instance. It seemed  
like the right and easiest choice to handle the deployment.


