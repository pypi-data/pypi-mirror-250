from peerberrypy import API
import os


peerberry_client = API(
    email=os.getenv(key='PEERBERRY_EMAIL'),
    password=os.getenv(key='PEERBERRY_PASSWORD'),
    tfa_secret=os.getenv(key='PEERBERRY_TFA_SECRET'),
)


print(peerberry_client.get_loans(100))
