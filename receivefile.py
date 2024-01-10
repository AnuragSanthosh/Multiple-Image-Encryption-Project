import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("C:/Users/ANURAG/Downloads/test-92060-firebase-adminsdk-x5mxe-38e493219a.json")
firebase_admin.initialize_app(cred)

bucket = storage.bucket(name='test-92060.appspot.com')

def download_file_from_storage(file_name, destination_path):
    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_path)
    print(f"File downloaded to {destination_path}")

file_name_in_storage = "parameters.json"
destination_local_path = "parameters.json"

download_file_from_storage(file_name_in_storage, destination_local_path)
