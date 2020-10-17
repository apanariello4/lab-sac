def update_meme(event, context):
    from google.cloud import firestore
    db = firestore.Client()

    if 'attributes' in event:
        if 'action' in event['attributes'] and 'meme_id' in event['attributes'] and 'tag' in event['attributes']:
            action = event['attributes']['action']
            meme_id = event['attributes']['meme_id']
            tag = event['attributes']['tag']
            if action == "DELETE":
                ref = db.document(f'memes/{meme_id}').get()
                if ref.exists():
                    tags = ref["tags"]
                    if tag in tags:
                        tags.remove(tag)
                        ref.set({"tags":tags})
                    else:
                        print("Tag is not present")
                else:
                    print("Document not found")
            if action == "INSERT":
                ref = db.document(f'memes/{meme_id}').get()
                if ref.exists():
                    tags = ref["tags"]
                    if tag in tags:
                        print("Tag already present")
                    else:
                        tags.append(tag)
                        ref.set({"tags":tags})
                else:
                    print("Document not found")
            else:
                print("Wrong Action")
        else:
            print("Wrong attributes")
