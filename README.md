# simple-notification-service

Event subscription service, similar to Amazon SNS in minimal view.
This will be a service that runs through the REST-API, accepting 
messages and storing them in a queue to be sent using 
a specific protocol.

####Requirements:

- python 3.7
- redis
- requirements.txt