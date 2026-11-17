import os
import re
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from dotenv import load_dotenv
from .models import SmsHistory

load_dotenv()

def send_sms_view(request):
    # Fetch the last 10 message attempts for the dashboard feature
    recent_messages = SmsHistory.objects.all().order_by('-timestamp')[:10]
    total_count = SmsHistory.objects.count()
    success_count = SmsHistory.objects.filter(status='Success').count()
    failed_count = SmsHistory.objects.exclude(status='Success').count()

    raw_phone = ''
    message_body = ''

    def get_context():
        return {
            'recent_messages': recent_messages,
            'phone_number': raw_phone,
            'message_body': message_body,
            'total_count': total_count,
            'success_count': success_count,
            'failed_count': failed_count,
        }

    if request.method == 'POST':
        raw_phone = request.POST.get('phone_number', '').strip()
        # Automatically prepend the Philippine country code
        phone_number = f"+63{raw_phone}" if raw_phone else ""
        message_body = request.POST.get('message', '').strip()

        # 3. Input Validation: Check for empty inputs
        if not phone_number or not message_body:
            messages.error(request, "Validation Error: Both phone number and message are required.")
            return render(request, 'sms_app/index.html', get_context())

        # 3. Input Validation: Check for valid phone number format (Basic E.164 format)
        phone_pattern = re.compile(r'^\+?[1-9]\d{9,14}$')
        if not phone_pattern.match(phone_number):
            messages.error(request, "Validation Error: Invalid phone number format. Use standard format (e.g., +639123456789).")
            return render(request, 'sms_app/index.html', get_context())

        try:
            # 4. Error Handling: Check for missing API credentials
            api_key = os.getenv('TEXTBEE_API_KEY')
            if not api_key:
                raise ValueError("Missing API credentials. Please check your .env file.")
            
            # 2. SMS Sending Functionality
            response = requests.post(
                "https://api.textbee.dev/api/v1/gateway/send-sms",
                json={
                    "recipients": [phone_number], 
                    "message": message_body
                },
                headers={"x-api-key": api_key},
                timeout=30
            )
            
            response.raise_for_status()
            
            # Save success to database and refresh page
            SmsHistory.objects.create(phone_number=phone_number, message=message_body, status='Success')
            messages.success(request, "Message successfully sent to gateway!")
            return redirect('send_sms')
            
        except requests.exceptions.HTTPError as e:
            # 4. Error Handling: Rejected messages
            SmsHistory.objects.create(phone_number=phone_number, message=message_body, status='Failed (Rejected)')
            messages.error(request, f"Gateway Error: Provider rejected the message. Details: {e.response.text}")
        except requests.exceptions.RequestException as e:
            # 4. Error Handling: Network connections
            SmsHistory.objects.create(phone_number=phone_number, message=message_body, status='Failed (Network)')
            messages.error(request, "Connection Error: Could not reach the Textbee SMS gateway.")
        except ValueError as e:
            # 4. Error Handling: Configuration
            messages.error(request, f"Configuration Error: {str(e)}")
        except Exception as e:
            messages.error(request, "An unexpected application error occurred.")

    return render(request, 'sms_app/index.html', get_context())
