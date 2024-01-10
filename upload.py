import json


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


with open('parameters.json', 'r') as file:
    parameters_data = json.load(file)

with open('encrypted_data.json', 'r') as file:
    encrypted_data = json.load(file)

parameters_data.update(encrypted_data)

with open('parameters.json', 'w') as file:
    json.dump(parameters_data, file, indent=2)

def upload_file_to_storage(local_file_path, destination_file_name):
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(local_file_path)
    print(f"File uploaded to Firebase Storage as {destination_file_name}")

local_file_path = "parameters.json"  
destination_file_name = "parameters.json" 


upload_file_to_storage(local_file_path, destination_file_name)

with open('signal_hide_label.txt', 'w') as signal_file:
    signal_file.write('hide_label')
with open('completed.txt', 'w') as signal_file:
    signal_file.write('completed')