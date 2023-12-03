import boto3
import json

# define the DynamoDB table that Lambda will connect to
tableName = "Courses"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

def handler(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
                 operation being performed
    '''
    
    # define the functions used to perform the CRUD operations
    def ddb_create(x):
        dynamo.put_item(**x)

    def ddb_read(x):
        response = dynamo.get_item(**x)
        item = response.get('Item', {})
        return item

    def ddb_update(x):
        dynamo.update_item(**x)
        
    def ddb_delete(x):
        dynamo.delete_item(**x)

    def ddb_scan(x):
        # You can pass filters and other parameters inside the scan method if needed
        response = dynamo.scan()
        items = response.get('Items', [])
        return items
    
    def echo(x):
        return x

    operation = event['operation']

    operations = {
        'create': ddb_create,
        'read': ddb_read,
        'update': ddb_update,
        'delete': ddb_delete,
        'scan': ddb_scan,  
        'echo': echo,
    }

    if operation in operations:
        return operations[operation](event.get('payload'))
    else:
        raise ValueError('Unrecognized operation "{}"'.format(operation))



'''
{
  "operation": "create",
  "payload": {
    "Item": {
      "CourseID": 3050,
      "Course_Name": "Test3",
      "Course_Number": 3401,
      "Description": "test",
      "Instructor": "prof",
      "Subject_Area": "cse",
      "S": "prototype"
    }
  }
}
'''

'''
{
    "operation": "update",
    "payload": {
        "Key": {
            "CourseID": 3050
        },
        "UpdateExpression": "set Course_Name = :name, Course_Number = :number, Description = :desc, Instructor = :instr, Subject_Area = :area",
        "ExpressionAttributeValues": {
            ":name": "New Course Name",
            ":number": 3402,
            ":desc": "Updated description",
            ":instr": "New Instructor",
            ":area": "New Subject Area"
        },
        "ReturnValues": "UPDATED_NEW"
    }
}

'''

'''
{
    "operation": "delete",
    "payload": {
        "Key": {
            "CourseID": 3050
        }
    }
}

'''

'''
{
    "operation": "read",
    "payload": {
        "Key": {
            "CourseID": 3050
        }
    }
}

'''

# https://kxxirxcj4g.execute-api.us-east-1.amazonaws.com/test//CourseDB