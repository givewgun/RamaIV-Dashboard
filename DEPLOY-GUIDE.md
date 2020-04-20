1. run this to build and push docker imaage
```
gcloud builds submit --tag gcr.io/taxi-272612/ramaivdashboardpred
```

2. run this to deploy (or use ui in google cloud)
```
gcloud run deploy ramaivdashboardpred --image gcr.io/taxi-272612/ramaivdashboardpred --platform managed --allow-unauthenticated
```