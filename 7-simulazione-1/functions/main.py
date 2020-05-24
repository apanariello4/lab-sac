def price_update(data, context):
    """ Triggered by a change to a Firestore document.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    import json
    from google.cloud import pubsub_v1

    PROJECT_ID = 'sac-vg-market3'

    pub = pubsub_v1.PublisherClient()
    topic = f'projects/{PROJECT_ID}/topics/pushTopic'

    # trigger_resource = context.resource

    old_price = data["oldValue"]["fields"]["price"]["integerValue"]
    new_price = data["value"]["fields"]["price"]["integerValue"]
    game = str(data["value"]["fields"]["title"]["stringValue"])

    # print('\nOld value:')
    # print(json.dumps(data["oldValue"]))

    # print('\nNew value:')
    # print(json.dumps(data["value"]))

    path_parts = context.resource.split('/documents/')[1].split('/')

    game_info = {
        'title': str(data["value"]['fields']['title']['stringValue']),
        'console': str(data["value"]['fields']['console']['stringValue']),
        'user_id': str(path_parts[1]),
        'game_id': str(path_parts[3])
    }

    print(json.dumps(game_info))

    if float(old_price) > 20 and float(new_price) < 20:
        pub.publish(topic, b'a game is below 20', **game_info)
        print("Published message")
    else:
        print("Message not published")
