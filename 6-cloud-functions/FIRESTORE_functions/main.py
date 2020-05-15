def firestore_trigger(data, context):
    """ Triggered by a change to a Firestore document.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    import json
    from google.cloud import pubsub_v1

    PROJECT_ID = 'sac-pubsub1'

    pub = pubsub_v1.PublisherClient()
    topic = f'projects/{PROJECT_ID}/topics/visits'

    trigger_resource = context.resource

    print('Function triggered by change to: %s' % trigger_resource)

    print('\nOld value:')
    print(json.dumps(data["oldValue"]))

    print('\nNew value:')
    print(json.dumps(data["value"]))

    pub.publish(topic, b'Number of visits', visits='100')
