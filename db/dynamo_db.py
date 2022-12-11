class DroneDb(object):

    def __init__(self, resource):
        self.resource = resource

    def create_table(self, table_name):
        table = self.resource.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'Email_Address',
                    'KeyType': 'HASH'  # Partition Key
                },
                {
                    'AttributeName': 'Flight_Id',
                    'KeyType': 'RANGE'  # Sort Key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Email_Address',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Flight_Id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Flight_Validation',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Flight_Time_s',
                    'AttributeType': 'N'
                }
            ],
            GlobalSecondaryIndexes=[  # Secondary Global Index to query only valid flights
                {
                    'IndexName': 'flights_validation',
                    'KeySchema': [
                        {
                            'AttributeName': 'Flight_Validation',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'Flight_Time_s',
                            'KeyType': 'RANGE'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,  # ReadCapacityUnits set to 10 strongly consistent reads per second
                        'WriteCapacityUnits': 5  # WriteCapacityUnits set to 10 writes per second
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,  # ReadCapacityUnits set to 10 strongly consistent reads per second
                'WriteCapacityUnits': 5  # WriteCapacityUnits set to 10 writes per second
            }
        )

        print("Creating Table....")
        table.wait_until_exists()
        return "Table Successfully Created"

    def insert_item(self, flight_id, flight_time, name, email, department):
        table = self.resource.Table('drone_flights')

        response = table.put_item(
            Item={
                'Flight_Id': flight_id,
                'Flight_Validation': 'F',
                'Flight_Time_s': flight_time,
                'pilot_name': name,
                'Email_Address': email,
                'Department': department
            }
        )

        status_code = response['ResponseMetadata']['HTTPStatusCode']

        return 'responded with status Code: {}'.format(status_code)
