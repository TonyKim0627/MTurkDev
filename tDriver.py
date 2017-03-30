#MTurk approving assignments, granting pay
#Tony Kim, JHU c/o 2018
import sys
import boto3
import json
region_name = 'us-east-1'
aws_access_key_id = ''
aws_secret_access_key = ''

#For testing purposes
#endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

client = boto3.client('mturk',
        endpoint_url = endpoint_url,
        region_name = region_name,
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
)


#Obtaining list of hits
#We assume we know that HIT ID
"""
hitDict = client.list_hits()
hitID = str(hitDict['HITs'])
indexS = hitID.find('HITId')
"""

hitID = '3MZ3TAMYTLYFA0GG2LX1HMY6G8XRIK'
hit = client.get_hit(HITId = hitID)
print 'Hit {} status: {}'.format(hitID, hit['HIT']['HITStatus'])
recvResponse = client.list_assignments_for_hit(
                HITId = hitID,
                AssignmentStatuses = ['Submitted']
)

responses = recvResponse['Assignments']
print 'There are total of ' + str(len(responses)) + ' responses waiting for approval.'

for response in responses:
    workerID = response['WorkerId']
    workerInputID = response['AssignmentId']
    workerInput = response['Answer']
    print '' + str(workerID) + 'inputted answer ' + str(workerInput)
    requesterDecision = raw_input('Y/N' + '\n')
    if requesterDecision is 'Y':
        client.approve_assignment(
            AssignmentId = workerInputID
        )
    elif requesterDecision is 'N':
        client.reject_assignment(
            AssignmentId = workerInputID,
            RequesterFeedback = 'Sorry'
        )
