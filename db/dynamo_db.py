class DroneDb(object):

    def __init__(self, resource):
        self.resource = resource

    def create_table(self, table_name):
        table = self.resource.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'Flight_Id',
                    'KeyType': 'HASH'  # Partition Key
                },
                {
                    'AttributeName': 'Flight_Validation',
                    'KeyType': 'RANGE'  # Sort Key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Flight_Id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Flight_Validation',
                    'AttributeType': 'S'
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
                'Flight_Time(s)': flight_time,
                'Name': name,
                'Email_Address': email,
                'Department': department
            }
        )

        status_code = response['ResponseMetadata']['HTTPStatusCode']

        return 'responded with status Code: {}'.format(status_code)
