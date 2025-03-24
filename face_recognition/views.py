from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from face_recognition.services.ai_service import AIService

@login_required
def upload_and_send(request, account_id):
    if request.method == 'POST':
        try:
            image_files = request.FILES.getlist('images')
            if not image_files:
                return JsonResponse({'error': 'Không có ảnh nào được gửi'}, status=400)
            ai_service = AIService()
            response = ai_service.send_images(account_id, image_files)

            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse(
                    {'error': f'Gửi ảnh thất bại - ServerAI trả về {response.status_code}: {response.text}'},
                    status=500)
        except Exception as e:
            return JsonResponse({'error': f'Lỗi khi gửi ảnh: {str(e)}'}, status=500)