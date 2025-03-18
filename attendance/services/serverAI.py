import requests

def send_images_to_serverAI(account_id, image_files):
    url = 'https://3f48-2402-800-629c-32b9-d9a2-3c9f-431e-df1d.ngrok-free.app/ai/'
    data = {'account_id': account_id}
    files = []

    for img in image_files:
        img.seek(0)  # QUAN TRỌNG: đảm bảo đọc từ đầu
        files.append(('images', (img.name, img.read(), img.content_type or 'image/jpeg')))

    response = requests.post(url, data=data, files=files)
    return response
