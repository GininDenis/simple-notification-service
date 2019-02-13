# Simple notification service

#### Short description


Event subscription service, similar to Amazon SNS in minimal view.
This will be a service that runs through the REST-API, accepting 
messages and storing them in a queue to be sent using 
a specific protocol.

#### Basic usage

- Create an account by registering and confirming mail

- Confirm account and fill out a profile.
Upon registration, an APIToken will be created,
which will need to be added to the request headers 
to the service API.

- Create Topic, which will be used for subscriptions within 
the framework of the created account, through the admin
web interface. Within one account, you can create multiple topics.
Within each topic, you can create an unlimited number of 
subscriptions (HTTP / HTTPS endpoints). 
Each endpoint created must be confirmed. 
The specified Endpoint must be able to process the 
message formats listed below at the time of subscription creation. In the case of a request with the type ConfirmSubscription, confirm the subscription by applying a non-subscription_url using the POST method, the subscription will be considered confirmed or by sending a token to / api / confirm /.

####Subscription confirmation:
```json
{
  "type": "SubscriptionConfirmation",
  "subscription_url": "str",
  "token": "str",
  "message": "please follow the‘ subscription_url ’link"
 }

```
####Notification:
```json
{
  "type": "Notification",
  "message": "please follow the‘ subscription_url ’link"
}
```


####Requirements:

- python 3.7
- redis
- requirements.txt