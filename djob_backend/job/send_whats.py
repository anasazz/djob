import requests
import os
def upload_pdf_as_media(access_token, phone_number_id, pdf_file_path , doc):
    url = f'https://graph.facebook.com/v18.0/{phone_number_id}/media'

    file_name = os.path.basename(pdf_file_path)


    files = {
        'file': (file_name, open(pdf_file_path, 'rb'), 'application/pdf')
    }

    data = {
        'type': 'document',
        'messaging_product': 'whatsapp'
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, files=files, data=data, headers=headers)

    print('from send_whats', response.text)
    if response.status_code == 200:
        media_id = response.json()["id"]
        return media_id
    else:
        return None


def send_pdf_as_whatsapp_message(access_token, recipient_phone_number, media_id):
    message_data = {
        "messaging_product": "whatsapp",
        "to": recipient_phone_number,
        "type": "document",
        "document": {
            "id": media_id
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        'https://graph.facebook.com/v17.0/109321572275515/messages',  # Replace with recipient's WhatsApp ID
        headers=headers,
        json=message_data
    )

    if response.status_code == 200:
        # Handle success
        return True
    else:
        # Handle failure
        return False
