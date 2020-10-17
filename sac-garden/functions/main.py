import json
import logging
import os

# from flask import escape
# from google.cloud import firestore
# from google.cloud import logging as cloudLoggin
# from google.cloud import pubsub_v1

# log_client = cloudLoggin.Client()
# log_handler = log_client.get_default_handler()
# cloud_logger = logging.getLogger("cloudLogger")
# cloud_logger.setLevel(logging.INFO)
# cloud_logger.addHandler(log_handler)


# Attivazione manualmente tramite invio di un messaggio contenente informazioni
# sulla durata dell’irrigazione (espressa in secondi) su un topic specifico

# Attivazione automatica tramite analisi dell’umidità del terreno, attivando l’irrigazione quando l’umidità
# scende sotto il 30%. Il valore di umidità viene letto su un topic diverso dal precedente.
def irrigatore(event, context):
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keys.json'
    if 'attributes' in event:
        if 'duration' in event['attributes']:
            duration = event['attributes']['duration']
            print('acceso manuale')
        elif 'humidity' in event['attributes']:
            humidity = event['attributes']['humidity']
            if float(humidity) < 0.3:
                print("acceso automatico")
            else:
                print("spento")
        else:
            print("spento")
    else:
        print("spento")
