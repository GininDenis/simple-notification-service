from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from apps.notifications.models import Topic, Subscription
from apps.users.models import User


class SubscriptionViewSetTestCase(TestCase):

    def setUp(self):
        self.user = mommy.make(User, is_active=True)
        self.topic = mommy.make(Topic, owner=self.user)

    def test_permissions(self):

        self.user.is_active = False
        self.user.save()

        url = reverse('api:subscriptions-list')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user.is_active = True
        self.user.save()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_subscription(self):
        create_data = {
            'protocol': 'http',
            'endpoint': 'http://test.com/',
            'topic': self.topic.id
        }
        url = reverse('api:subscriptions-list')
        self.client.force_login(self.user)

        response = self.client.post(url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        subscription_id = response.json()['id']
        subscription = Subscription.objects.get(pk=subscription_id)

        self.assertEqual(subscription.status,
                         Subscription.STATUS_CHOICES.pending)

    def test_confirm_subscription(self):
        url = reverse('api:subscriptions-confirm')
        subscription = mommy.make(Subscription)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'subscription': subscription.pk,
            'token': subscription.token
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscription.refresh_from_db()
        self.assertEqual(subscription.status,
                         Subscription.STATUS_CHOICES.confirmed)

    def test_destroy_subscription(self):
        subscription = mommy.make(Subscription, topic__owner=self.user)
        url = reverse('api:subscriptions-detail',
                      kwargs={'pk': subscription.pk})
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertRaises(Subscription.DoesNotExist,
                          subscription.refresh_from_db)

    def test_list_subscriptions(self):
        user = mommy.make(User, is_active=True)
        mommy.make(
            Subscription,
            topic__owner=user,
            _quantity=5
        )
        mommy.make(
            Subscription,
            _quantity=20
        )
        subscriptions = Subscription.objects.filter(topic__owner_id=user.pk)
        database_count = len(subscriptions)
        url = reverse('api:subscriptions-list')
        self.client.force_login(user)

        response = self.client.get(url)
        response_count = len(response.json())
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(database_count, response_count)

    def test_retrieve_subscription(self):
        subscription = mommy.make(Subscription, topic__owner=self.user)
        url = reverse('api:subscriptions-detail',
                      kwargs={'pk': subscription.pk})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TopicViewSetTestCase(TestCase):

    def setUp(self):
        self.user = mommy.make(User, is_active=True)

    def test_permissions(self):

        self.user.is_active = False
        self.user.save()

        url = reverse('api:topics-list')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user.is_active = True
        self.user.save()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_topic(self):
        create_data = {
            'owner': self.user.id,
            'title': 'test'
        }

        url = reverse('api:topics-list')
        self.client.force_login(self.user)

        response = self.client.post(url, data=create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        topic_id = response.json()['id']
        topic = Topic.objects.get(pk=topic_id)

        self.assertEqual(str(topic), create_data['title'])

    def test_destroy_topic(self):
        topic = mommy.make(Topic, owner=self.user)
        url = reverse('api:topics-detail',
                      kwargs={'pk': topic.pk})
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertRaises(Topic.DoesNotExist,
                          topic.refresh_from_db)

    def test_list_topics(self):
        user = mommy.make(User, is_active=True)
        mommy.make(
            Topic,
            topic__owner=user,
            _quantity=5
        )
        mommy.make(
            Topic,
            _quantity=20
        )
        topics = Topic.objects.filter(owner_id=user.pk)
        database_count = len(topics)
        url = reverse('api:topics-list')
        self.client.force_login(user)

        response = self.client.get(url)
        response_count = len(response.json())
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(database_count, response_count)

    def test_retrieve_topic(self):
        topic = mommy.make(Topic, owner=self.user)
        url = reverse('api:topics-detail',
                      kwargs={'pk': topic.pk})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
