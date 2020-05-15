# Set default project

`gcloud config set project [PROJECT-ID]`

# Get credentials.json

`gcloud iam service-accounts create [NAME]`

`gcloud projects add-iam-policy-binding [PROJECT_ID] --member "serviceAccount:[NAME]@[PROJECT_ID].iam.gserviceaccount.com" --role "roles/owner"`

`gcloud iam service-accounts keys create [FILE_NAME].json --iam-account [NAME]@[PROJECT_ID].iam.gserviceaccount.com`

# Set the environment variabile
## In terminal

`export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"`

## In VSCode

`os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'my-path/credentials.json'`

# Deploying app

1. app.yaml
2. remove credentials

`gcloud app deploy`

# Deploying api

0. Modify [PROJECT_ID] in openapi.yaml

1. Create a dedicated endpoint project (no if already deployed webapp).

    ```gcloud projects create [YOUR_PROJECT_NAME] --set-as-default```

2. Validate the OpenAPI document

    `gcloud endpoints services deploy [OPENAPI].yaml --validate-only`

3. Deploy the OpenAPI document

    `gcloud endpoints services deploy [OPENAPI].yaml`

4. Deploy app

    `gcloud deploy app`

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

# Cloud Functions

`gcloud functions deploy [function_name] --runtime python37 --trigger-topic [YOUR_TOPIC_NAME]`
