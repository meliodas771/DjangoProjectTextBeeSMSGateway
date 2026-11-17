import os
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from requests.exceptions import RequestException, HTTPError
from .models import SmsHistory

class SmsAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.send_sms_url = reverse('send_sms')

    def test_page_loads_successfully(self):
        """Verify the SMS composition page renders with 200 status."""
        response = self.client.get(self.send_sms_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_app/index.html')
        self.assertContains(response, 'Recipient Phone Number')
        self.assertContains(response, 'Message')

    def test_empty_phone_validation(self):
        """Empty phone number must be rejected."""
        response = self.client.post(self.send_sms_url, {
            'phone_number': '',
            'message': 'Hello world test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Validation Error: Both phone number and message are required.")
        self.assertEqual(SmsHistory.objects.count(), 0)

    def test_empty_message_validation(self):
        """Empty message body must be rejected."""
        response = self.client.post(self.send_sms_url, {
            'phone_number': '9123456789',
            'message': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Validation Error: Both phone number and message are required.")
        self.assertEqual(SmsHistory.objects.count(), 0)

    def test_invalid_phone_number_format(self):
        """Phone numbers with invalid formats must be rejected."""
        response = self.client.post(self.send_sms_url, {
            'phone_number': '123',
            'message': 'Testing invalid number'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Validation Error: Invalid phone number format.")
        self.assertEqual(SmsHistory.objects.count(), 0)

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_credentials(self):
        """Missing API credentials in environment variables must show configuration error."""
        response = self.client.post(self.send_sms_url, {
            'phone_number': '9123456789',
            'message': 'Test without credentials'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Configuration Error: Missing API credentials.")
        self.assertEqual(SmsHistory.objects.count(), 0)

    @patch('sms_app.views.requests.post')
    @patch.dict(os.environ, {'TEXTBEE_API_KEY': 'fake_test_key'})
    def test_successful_sms_submission(self, mock_post):
        """Successful API response creates history and redirects with success message."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        response = self.client.post(self.send_sms_url, {
            'phone_number': '9123456789',
            'message': 'Test successful delivery'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Message successfully sent to gateway!")
        self.assertEqual(SmsHistory.objects.count(), 1)
        history_item = SmsHistory.objects.first()
        self.assertEqual(history_item.phone_number, '+639123456789')
        self.assertEqual(history_item.status, 'Success')

    @patch('sms_app.views.requests.post')
    @patch.dict(os.environ, {'TEXTBEE_API_KEY': 'fake_test_key'})
    def test_gateway_rejection_error_handling(self, mock_post):
        """Provider rejection must log Failed (Rejected) and show error."""
        mock_response = MagicMock()
        mock_response.text = '{"error": "Unauthorized"}'
        mock_post.side_effect = HTTPError(response=mock_response)

        response = self.client.post(self.send_sms_url, {
            'phone_number': '9123456789',
            'message': 'Test rejection'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gateway Error: Provider rejected the message.")
        self.assertEqual(SmsHistory.objects.count(), 1)
        self.assertEqual(SmsHistory.objects.first().status, 'Failed (Rejected)')

    @patch('sms_app.views.requests.post')
    @patch.dict(os.environ, {'TEXTBEE_API_KEY': 'fake_test_key'})
    def test_network_connection_error_handling(self, mock_post):
        """Network error must log Failed (Network) and notify user."""
        mock_post.side_effect = RequestException("Connection timed out")

        response = self.client.post(self.send_sms_url, {
            'phone_number': '9123456789',
            'message': 'Test connection failure'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connection Error: Could not reach the Textbee SMS gateway.")
        self.assertEqual(SmsHistory.objects.count(), 1)
        self.assertEqual(SmsHistory.objects.first().status, 'Failed (Network)')
