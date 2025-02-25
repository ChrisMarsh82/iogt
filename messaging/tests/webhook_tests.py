from base64 import b64encode

from django.core import management
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from home.models import User
from messaging.factories import ThreadFactory
from messaging.models import Message, Attachment


class RapidProWebhookTest(APITestCase):
    @override_settings(RAPIDPRO_BOT_USER_USERNAME='rb1', RAPIDPRO_BOT_USER_PASSWORD='rapidpassword1')
    def setUp(self) -> None:
        management.call_command('sync_rapidpro_bot_user')
        self.bot_user = User.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION="Basic {}".format(
            b64encode(bytes(f"rb1:rapidpassword1", "utf-8")).decode("ascii")
        ))

    @override_settings(
        RAPIDPRO_BOT_USER_USERNAME='rb1',
        RAPIDPRO_BOT_USER_PASSWORD='rapidpassword1',
        RAPIDPRO_BOT_USER_ID=1
    )
    def test_webhook_stitches_messages(self):
        thread = ThreadFactory()

        rapidpro_data_list = [
            {
                "id": "1",
                "text": "Some message with the first part of text. First part ends at the exclamation mark!",
                "to": str(thread.uuid),
                "from": "abcd",
                "channel": "bd3577c6-65b1-4bb7-9611-306c11b1dcc5",
                "quick_replies": [
                    "Baby (0 to 23 months old)", "Young child (2 to 9 years)", "Teenager (10 to 17 years)"
                ]
            },
            {
                "id": "1",
                "text": "The second part starts here",
                "to": str(thread.uuid),
                "from": "abcd",
                "channel": "bd3577c6-65b1-4bb7-9611-306c11b1dcc5",
                "quick_replies": [
                    "Baby (0 to 23 months old)", "Young child (2 to 9 years)", "Teenager (10 to 17 years)"
                ]
            },

        ]

        for data in rapidpro_data_list:
            response = self.client.post(path=reverse('messaging:api:rapidpro_webhook'), data=data, format='json')

        message = Message.objects.first()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.text, 'Some message with the first part of text.'
                                       ' First part ends at the exclamation mark!The second part starts here')
        self.assertEqual(len(message.quick_replies), 3)

    @override_settings(
        RAPIDPRO_BOT_USER_USERNAME='rb1',
        RAPIDPRO_BOT_USER_PASSWORD='rapidpassword1',
        RAPIDPRO_BOT_USER_ID=1
    )
    def test_webhook_parses_attachments(self):
        thread = ThreadFactory()

        rapidpro_data = {
            "id": "1",
            "text": "Some message with attachment.\nhttps://rapidpro.idems.international/media/attachments/43/"
                    "15890/steps/3de4f80a-1eab-42db-8b7e-d7c35edecd06.bin",
            "to": str(thread.uuid),
            "from": "abcd",
            "channel": "bd3577c6-65b1-4bb7-9611-306c11b1dcc5",
            "quick_replies": [
                "Baby (0 to 23 months old)", "Young child (2 to 9 years)", "Teenager (10 to 17 years)"]}

        response = self.client.post(path=reverse('messaging:api:rapidpro_webhook'), data=rapidpro_data, format='json')

        message = thread.get_renderable_messages().first()
        attachment = message.attachments.all()[0]

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.attachments.all().count(), 1)
        self.assertEqual(message.text, 'Some message with attachment.')
        self.assertEqual(attachment.external_link,
                         'https://rapidpro.idems.international/media/attachments/43/15890/steps/'
                         '3de4f80a-1eab-42db-8b7e-d7c35edecd06.bin')
        self.assertIsNotNone(attachment.file)

    @override_settings(
        RAPIDPRO_BOT_USER_USERNAME='rb1',
        RAPIDPRO_BOT_USER_PASSWORD='rapidpassword1',
        RAPIDPRO_BOT_USER_ID=1
    )
    def test_stitched_attachment_parsing(self):
        thread = ThreadFactory()

        rapidpro_data_list = [
            {
                "id": "1",
                "text": "Some message with a stitched url.\nhttp://www.internet.com/12345",
                "to": str(thread.uuid),
                "from": "abcd",
                "channel": "bd3577c6-65b1-4bb7-9611-306c11b1dcc5",
                "quick_replies": [
                    "Baby (0 to 23 months old)", "Young child (2 to 9 years)", "Teenager (10 to 17 years)"
                ]
            },
            {
                "id": "1",
                "text": "678910.jpg",
                "to": str(thread.uuid),
                "from": "abcd",
                "channel": "bd3577c6-65b1-4bb7-9611-306c11b1dcc5",
                "quick_replies": [
                    "Baby (0 to 23 months old)", "Young child (2 to 9 years)", "Teenager (10 to 17 years)"
                ]
            },

        ]

        for data in rapidpro_data_list:
            response = self.client.post(path=reverse('messaging:api:rapidpro_webhook'), data=data, format='json')

        message = thread.get_renderable_messages().first()
        attachment = message.attachments.first()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.text, 'Some message with a stitched url.')
        self.assertEqual(message.attachments.count(), 1)
        self.assertEqual(attachment.external_link, 'http://www.internet.com/12345678910.jpg')
        self.assertEqual(len(message.quick_replies), 3)

    @override_settings(
        RAPIDPRO_BOT_USER_USERNAME='rb1',
        RAPIDPRO_BOT_USER_PASSWORD='rapidpassword1',
        RAPIDPRO_BOT_USER_ID=1
    )
    def test_single_download(self):
        thread = ThreadFactory()

        rapidpro_data_list = [
            {
                "id": "1",
                "text": "Some message with attachment \nhttps://via.placeholder.com/200",
                "to": str(thread.uuid),
                "from": "abcd",
                "channel": "bd3577c6-65b1-4bb7-9611-306c11b1dcc5",
                "quick_replies": [
                    "Baby (0 to 23 months old)", "Young child (2 to 9 years)", "Teenager (10 to 17 years)"
                ]
            },
            {
                "id": "2",
                "text": "Another message with the same attachment \nhttps://via.placeholder.com/200",
                "to": str(thread.uuid),
                "from": "abcd",
                "channel": "bd3577c6-65b1-4bb7-9611-306c11b1dcc5",
                "quick_replies": [
                    "Baby (0 to 23 months old)", "Young child (2 to 9 years)", "Teenager (10 to 17 years)"
                ]
            },

        ]

        for data in rapidpro_data_list:
            response = self.client.post(path=reverse('messaging:api:rapidpro_webhook'), data=data, format='json')

        messages = thread.get_renderable_messages()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].text, 'Another message with the same attachment ')
        self.assertEqual(messages[1].text, 'Some message with attachment ')
        self.assertEqual(Attachment.objects.count(), 1)

        attachment = Attachment.objects.first()
        self.assertEqual('https://via.placeholder.com/200', attachment.external_link)

        self.assertIsNotNone(attachment.image)

