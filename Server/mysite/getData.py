import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate(
    "./newtraingdata-firebase-adminsdk-citr0-2048de1105.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'Data')
data = []
try:
    docs = doc_ref.get()

    for doc in docs:
        data.append(doc.to_dict())

except google.cloud.exceptions.NotFound:
    print(u'Missing data')

print('Leght:', len(data))

print(data)
