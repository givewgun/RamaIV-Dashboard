# RamaIV-Dashboard
Traffic dashboard of Rama IV road in Bangkok, Thailand


## Require

1. Python 3
2. Google cloud project

### Setup

1. Create google cloud service account in api&credentials menu. Choose role that can query and access BigQuery and download the .json credentials
2. rename the credentials to gcloud_credential.json and move into /tabs/config
3. Install virtualenv (optional)
4. Install necessary requirements from requirements.txt

### Command

To install virtualenv
```
pip install virtualenv
```

Then, you have to run the following to make and activate the venv
```
virtualenv venv

venv\Scripts\activate.bat

pip install -r requirements.txt (or use only this line if don't want to create virtualenv)

```

### RUN

```
python index.py
```
