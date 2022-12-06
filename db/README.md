# DynamoDB Implementation

The dynamoDB implementation used in this project was using the **boto3** sdk from aws, which gives you access to manipulate services available in aws, originaly the aws account used for this project was a federated account which means it has access to certain resources in aws and restrictive access to most actions in aws services. For those reasons I created a aws account as a root user and created an IAM user to access the dynamodb resource programatically and used this to implement dynamodb on this project.

> Implementation

We have a class in [dynamodb_py](https://github.com/JeanCarlosVal/Tello_Drone/blob/main/db/dynamo_db.py) file, this class has a constructor that takes in a resource object and initializes the resource object, then this resource is used to make accions on dynamoDB. We have two functions in this class:

- **create_table**, which takes in a name in form of a string and creates a table with read and write capacities of 5, a partition key of Email and a partition key of flight_id  
- **insert_item**, which takes in name of user, email, department, flight_id and flight_time. flight_validation is F by default because we are modifing wether the flight was succesfull or not on the dynamoDb console

Then we have [test](https://github.com/JeanCarlosVal/Tello_Drone/blob/main/db/test.py) file which imports the class and uses it to create a table and insert some sample data to the dynamo table, in this case we have the table already created, so all its doing is inserting data into the table 
