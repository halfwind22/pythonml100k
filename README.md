
# Take2 Interactive Tech Interview Question

The MovieLens 100K Dataset is used for this exercise. It can be downloaded from
https://grouplens.org/datasets/movielens/100k/ for a sample glance.

Dataset is available under 
https://files.grouplens.org/datasets/movielens/ml-100k.zip

### Introduction
 All the 3 questions have been implemented as 3 separate functions in a single main.py file . Execution of the main file leads to generated outputs in the target folder. Unit tests check for data integrity issues.A file based logger
 logs messages to a log file.
 
### Steps to run the project:

##### Method1: Using Docker

- The contents of the zip file must be extracted into any location.
- Docker must be installed and is a pre-requisite.
- Execute the below commands:
        
```sh
    cd Take2Project
    docker build --rm --pull -t "take2projectfeaturedev:latest" .
```
- At this point the Docker image is built and is assigned a random name.
        To verify, run
```sh
    docker images
```

- We should be seeing an image with the name _take2projectfeaturedev_ .Note the
  _IMAGE ID_ of this image.
- To run a container off the image,

```sh
    docker run -it IMAGE ID
```
- This spins up a container that runs the ETL job and print the output files
  onto the terminal.



##### Method2: Using python and cmd (Windows Terminal,but universal with only minor changes needed)

- First, we must create a virtual environment using below command, and also       activate it:

```sh
    python3 -m venv venv
    venv\Scripts\activate
```
- Next, we must install the required dependencies using:
```sh
    pip install -r requirements.txt
```
- Create a directory for storing the output files.
```sh
    mkdir target
```
- Download the ml-100k folder from [https://files.grouplens.org/datasets/movielens/ml-100k.zip].Unzip it
and place the ml -100k folder in the current directory.
 If all good then  the current directory structure so far should look like this:

   Take2Project
    ├───ml-100k
    ├───target
    └───venv


- Run tests
```sh
    python -m unittest test_etl.py -v
```
- Run main script
```sh
    python main_etl.py
```
- The _target_ folder should have 3 files generated corresponding to each question.       
        
