import os
import boto3
import pymysql.cursors
from dotenv import load_dotenv, find_dotenv
from db.dynamo_db import DroneDb

# finding environment variable
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv("DB_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("DB_SECRET_ACCESS_KEY_ID"),
    region_name='us-east-1'
)

# # DroneDB class object
# db = DroneDb(dynamodb)

# connection to rds
rds = pymysql.connect(host='drone-flights-data.cahojfeljvlq.us-east-1.rds.amazonaws.com',
                      user='admin',
                      password='admin123')
# used to execute commands to rds
cursor = rds.cursor()

# # creating a database to create table
# create_db_sql = '''create database drone_flights'''
# cursor.execute(create_db_sql)

# using database
using_sql = '''use drone_flights'''
cursor.execute(using_sql)

# # creating a table
# sql = '''create table pilot_flights (
# flight_id text not null,
# pilot_name text,
# email_address text,
# department text,
# flight_validation text,
# flight_time int,
# primary key(flight_id(768))
# )
# '''
# cursor.execute(sql)

# showing tables
# cursor.execute('''show tables''')

# show contents of table
cursor.execute('''select * from pilot_flights''')


# used to get data from execution
data = cursor.fetchall()

print(data)


# # Creating Table
# status = db.create_table("drone_flights")
# print(status)

# # Inserting sample Data to table
# status = db.insert_item('2022-12-05.130', 60, 'John Doe', 'John_Doe@Outlook.com', 'Computer Science')
# print(status)
# status = db.insert_item('2022-12-05.233', 40, 'Jonathan haves', 'Jonathan_haves@hotmail.com', 'Economics')
# print(status)
# status = db.insert_item('2022-12-05.277', 9, 'Hing Ming', 'Hing_Ming@hotmail.com', 'Science')
# print(status)
# status = db.insert_item('2022-12-05.456', 10, 'Philip Drew', 'Philip_Drew1231@hotmail.com', 'Business')
# print(status)
# status = db.insert_item('2022-12-05.231', 14, 'Andrii kashliev', 'akashlie@emich.edu', 'Computer Science')
# print(status)
# status = db.insert_item('2022-12-05.123', 10, 'Jean Valenzuela', 'Yanky20081@hotmail.com', 'Computer Science')
# print(status)
# status = db.insert_item('2022-12-05.56', 13, 'Andrea Sanchez', 'Andrea Sanchez@hotmail.com', 'Law')
# print(status)
