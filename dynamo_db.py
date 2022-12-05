import boto3

__TableName__ = "Drone_Flights"

client = boto3.client('dynamodb')

DB = boto3.resource('dynamodb')

table = DB.Table(__TableName__)


class db_functions(object):

    def insert_item(self, Name, Email, Department, FLight_Time, Flight_id):
        table.put_item