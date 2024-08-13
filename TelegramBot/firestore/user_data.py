'''
Title: User records in Google Cloud Firestore
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶
programing languages: Python
Description: The function of the code is to do the CRUD task in the firestore database. Firestore database is required 
to maintain the user perfered language.
Code Version: V1.0
Copyright ©: Open-source
'''

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('service_account.json') #give your service.json file path here
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def check_user_record(user_id):
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return True
    return False

def get_user_record(user_id):
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    return doc.to_dict()

def add_user_record(user_id, langcd,lang, uname):
    doc_ref = db.collection("users").document(user_id)
    doc_ref.set({
        "name": uname,
        "userId": user_id,
        "language": lang,
        "lang": langcd
    })

def update_user_record(user_id, langcd, lang):
    doc_ref = db.collection('users').document(user_id)
    doc_ref.update({
        "lang": langcd,
        "language": lang
    })
