def api_visits(request):
    from google.cloud import firestore
    from flask import abort, jsonify

    db = firestore.Client(project='sac-pubsub1')
    if request.method == 'GET':
        docs = db.collection(u'visits').stream()
        ret = {d.id: d.to_dict() for d in docs}
        return jsonify(ret)

    if request.method == 'POST':
        content_type = request.headers['content-type']

        if content_type == 'application/json':
            request_json = request.get_json(silent=True)
            if request_json and 'page' in request_json:
                page_name = request_json['page']
            else:
                raise ValueError(
                    "JSON is invalid or missing a 'page' property")
            if request_json and 'visits' in request_json:
                count_val = request_json['visits']
            else:
                raise ValueError(
                    "JSON is invalid or missing a 'visits' property")
    counter_ref = db.collection(u'visits').document(f'{page_name}')
    counter_ref.set({u'counter': count_val})
    return '', 200
