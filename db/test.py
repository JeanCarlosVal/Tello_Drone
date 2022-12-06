import os
import boto3
from db.dynamo_db import DroneDb

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('DB_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('DB_SECRET_ACCESS_KEY_ID'),
    region_name='us-east-1'
)

db = DroneDb(dynamodb)

status = db.insert_item('2022-12-05.130', 60, 'John Doe', 'John_Doe@Outlook.com', 'Computer Science')
print(status)
status = db.insert_item('2022-12-05.233', 40, 'Jonathan haves', 'Jonathan_haves@hotmail.com', 'Economics')
print(status)
status = db.insert_item('2022-12-05.277', 9, 'Hing Ming', 'Hing_Ming@hotmail.com', 'Science')
print(status)
status = db.insert_item('2022-12-05.456', 10, 'Philip Drew', 'Philip_Drew1231@hotmail.com', 'Business')
print(status)
status = db.insert_item('2022-12-05.231', 14, 'Andrii kashliev', 'akashlie@emich.edu', 'Computer Science')
print(status)
status = db.insert_item('2022-12-05.123', 10, 'Jean Valenzuela', 'Yanky20081@hotmail.com', 'Computer Science')
print(status)
status = db.insert_item('2022-12-05.56', 13, 'Andrea Sanchez', 'Andrea Sanchez@hotmail.com', 'Law')
print(status)