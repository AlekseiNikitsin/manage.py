import asyncio

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin.db import Event


# Fetch the service account key JSON file contents
cred = credentials.Certificate('firekay.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    

})
new = ''


def change(e: Event):
    print(e.data)


ref = db.reference('jo')
ref.listen(change)

def fire_get():
    return ref.get()