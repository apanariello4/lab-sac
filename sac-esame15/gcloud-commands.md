# Set default project

`gcloud config set project [PROJECT-ID]`

# Get credentials.json

```
gcloud iam service-accounts create [NAME]

gcloud projects add-iam-policy-binding [PROJECT_ID] --member "serviceAccount:[NAME]@[PROJECT_ID].iam.gserviceaccount.com" --role "roles/owner"

gcloud iam service-accounts keys create [FILE_NAME].json --iam-account [NAME]@[PROJECT_ID].iam.gserviceaccount.com
```

# Set the environment variabile
## In terminal

`export GOOGLE_APPLICATION_CREDENTIALS="/home/nello/Desktop/credentials.json"`

## In VSCode

`os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/credentials.json'`

# Deploying app

1. app.yaml
2. remove credentials

`gcloud app deploy`

# Endpoints

0. Modify [PROJECT_ID] in openapi.yaml

1. Create a dedicated endpoint project (no if already deployed webapp)

    `gcloud projects create [YOUR_PROJECT_NAME] --set-as-default`

2. Validate the OpenAPI document

    `gcloud endpoints services deploy [OPENAPI].yaml --validate-only`

3. Deploy the OpenAPI document

    `gcloud endpoints services deploy [OPENAPI].yaml`

    a. Increase timeout

    `gcloud config set app/cloud_build_timeout 1600s`

4. Deploy app

    `gcloud app deploy`

# Pub-Sub

## Topics

`gcloud pubsub topics create TOPIC [TOPIC ...]`
- Topics can be found under `projects/[YOUR_PROJECT_ID]/topics/[TOPIC]`

`gcloud pubsub topics list`

### Publish topic

`gcloud pubsub topics publish TOPIC --attribute=[ATTRIBUTE=VALUE, ...] --message=MESSAGE`

## Subscriptions

`gcloud pubsub subscriptions create SUBSCRIPTION_NAME --topic TOPIC`

`gcloud pubsub subscriptions pull SUBSCRIPTION_NAME`
- No push via CLI

### Webhook

`gcloud pubsub subscriptions create pushSub --topic pushTopic --push-endpoint 'https://sac-vg-market3.appspot.com/pubsub/push?token=sac123' --ack-deadline 10`
# Cloud Functions

`gcloud

## Topic trigger
`gcloud functions deploy [function_name] --runtime python37 --trigger-topic [YOUR_TOPIC_NAME]`

## HTTP trigger

## Firestore trigger
```
gcloud functions deploy FUNCTION_NAME --runtime python37 --trigger-event providers/cloud.firestore/eventTypes/document.update --trigger-resource projects/YOUR_PROJECT_ID/databases/\(default\)/documents/messages/{pushId}
```
