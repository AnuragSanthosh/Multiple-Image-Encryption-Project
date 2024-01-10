import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("C:/Users/ANURAG/Downloads/test-92060-firebase-adminsdk-x5mxe-38e493219a.json")
firebase_admin.initialize_app(cred)

bucket = storage.bucket(name='test-92060.appspot.com')

def upload_file_to_storage(local_file_path, destination_file_name):
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(local_file_path)
    print(f"File uploaded to Firebase Storage as {destination_file_name}")

local_file_path = "parameters.json"  
destination_file_name = "parameters.json"  

upload_file_to_storage(local_file_path, destination_file_name)
