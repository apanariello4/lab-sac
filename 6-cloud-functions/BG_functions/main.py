def visit_count(event, context):
    from google.cloud import firestore
    db = firestore.Client()

    if 'attributes' in event:
        if 'page' in event['attributes']:
            page_name = event['attributes']['page']

        counter_ref = db.collection(u'visits').document(f'{page_name}')
        if not counter_ref.get().exists:
            counter_ref.set({u'counter': 1})
        else:
            counter_ref.update({u'counter': firestore.Increment(1)})
        print(f'Incremented {page_name} counter visit')
    else:
        page_name = 'Unknown'
        print('Nothing done')
