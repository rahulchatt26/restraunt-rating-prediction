# Restaurant Rating Prediction
!['image'](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/image.jpg)

### Detailed video on code explanation
```
https://drive.google.com/file/d/1SXSyaaYOz3TzEcHx7spaTbua6rZ2Bpdk/view?usp=share_link
```

### Step 1 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 2 - Run main.py file

```bash
python main.py
```


To download your dataset

```
wget https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data
```


Git commands

If you are starting a project and you want to use git in your project
```
git init
```
Note: This is going to initalize git in your source code.

OR

You can clone exiting github repo
```
git clone <github_url>
```
Note: Clone/ Downlaod github  repo in your system


Add your changes made in file to git stagging are
```
git add file_name
```
Note: You can given file_name to add specific file or use "." to add everything to staging are


Create commits
```
git commit -m "message"
```

```
git push origin main
```
Note: origin--> contains url to your github repo
main--> is your branch name 

To push your changes forcefully.
```
git push origin main -f
```


To pull  changes from github repo
```
git pull origin main
```
Note: origin--> contains url to your github repo
main--> is your branch name

### Deployment link
```
Airflow:
http://https://ec2-3-108-62-248.ap-south-1.compute.amazonaws.com:8080

(Link might have expired)

For singular prediction from local:
python app.py

```
### Problem Statement
Zomato, the online food app, has reached out to us to help them to predict how good or bad a restaurant will turn out in the future. So that, they can take a decision to include the restaurant in their app or remove it.

They have shared the data of 9551 restaurants from all over the world which are currently present in the Zomato App. It contains the details about the restaurants and what rating it achieved finally.

Our task is to create a machine learning model which can predict the Rating of a restaurant based on its characteristics.

### Solution Proposed 
1. Data Ingestion: Collect data from Zomato dataset. The data should include information on restaurant attributes, such as location, cuisine, price range, menu items, and customer ratings. 
2. Data Preprocessing: Clean the data by removing irrelevant or missing values, and performing feature engineering to extract useful features from the data. Also, normalize or scale the data to ensure that all features have equal importance. 
3. Feature Selection: Select the most relevant features that influence the restaurant ratings. This can be done by using statistical methods, such as correlation or feature importance analysis. 
4. Model Training: Train the machine learning model using various algorithms, such as linear regression, decision trees, or random forests. The data should be split into training and testing datasets to evaluate the model's performance. 
5. Model Evaluation: Evaluate the model's performance using metrics such as accuracy, precision, recall, or F1-score. The model should be tested on the testing dataset to ensure its generalization ability. 
6. Model Deployment: Deploy the model for use in real-world scenarios, such as recommending restaurants to customers based on their preferences or assisting restaurant owners in making data-driven decisions. 
Overall, the proposed solution involves collecting and preprocessing data, selecting relevant features, training the machine learning model, evaluating its performance, and deploying the model for real-world applications. The solution can assist restaurant owners in understanding their customers' preferences and making data-driven decisions to enhance customer satisfaction. 

## Tech Stack Used
1. Python 
2. VS Code 
3. Machine learning algorithms
4. Docker
5. MongoDB
6. Flask

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Github Actions
5. Airflow

## How to run?
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

By running the Airflow link you will get this interface

!['image'](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/airflow.png)


For real-time prediction you can use the above Elastic Beanstalk link 

or 

1. Run this project in local by executing the code "python app.py"
2. In browser open "http://127.0.0.1:8080/" link
3. You will get an UI displayed below:
!['Homepage1'](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/homepage1.png)
!['Homepage2'](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/homepage%202.png)
4. Prediction page will displayed below:
!['Prediction'](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/prediction.png)



## Data Collections

![image](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/DATA%20COLLECTIONS.png)

## Project Archietecture
![Architect_Batch_Prediction](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/Project%20Archietecture.jpg)

![image](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/Project%20Archietecture%202.png)


#### Real-time Prediction

![image](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/Real-time%20Prediction.png)


## Deployment Archietecture
![Screenshot_19-overlay](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/Deployment%20Archietecture.png)

![image](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/Deployment%20Archietecture%202.png)

## Pipeline
![image](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/PIPELINE.png)

![image](https://github.com/rahulchatt26/restraunt-rating-prediction/blob/main/images/PIPELINE%202.png)


### Step 1: Clone the repository
```bash
git clone https://github.com/rahulchatt26/restraunt-rating-prediction
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n venv python=3.8 -y
```

```bash
conda activate venv
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable
```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

export MONGODB_URL=<MONGODB_URL>

```

### Step 5 - Run the application server
```bash
python main.py
```


## Run locally

1. Check if the Dockerfile is available in the project directory

2. Build the Docker image
```
docker build --build-arg AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> --build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> --build-arg AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION> --build-arg MONGODB_URL=<MONGODB_URL> . 

```

3. Run the Docker image
```
docker run -d -p 8080:8080 <IMAGE_NAME>
```

then run 
```
python main.py
```

### To download the dataset 
```
wget https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data
```

### To check and reset git log
```
git log
git reset --soft 6afd
6afd -> last 4 digit of log. 
```

### To add and uplod to git
```
git add filename
we can also use . for all file(Current directory)

git commit -m "Message"
git push origin main
```

### To run jupyter-notebook in vscode
```
 pip install ipykernel
```

### **To create a new environment in vscode** 
```
 1. Select the command prompt as a terminal 
conda create -p venv python==3.87 -y
```

### Create a .env It contains details.
```
MONGO_DB_URL=""
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
```
### **To install dockers in aws machine (EC2)**
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

**Secrets**
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
AWS_ECR_LOGIN_URI=
ECR_REPOSITORY_NAME=
BUCKET_NAME=
MONGO_DB_URL=
```
