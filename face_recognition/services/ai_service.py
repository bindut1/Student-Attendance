import requests
import logging
import base64

logger = logging.getLogger(__name__)


class AIService:
    def send_images(self, account_id, image_files):
        data = {"account_id": account_id}
        files = []

        try:
            for img in image_files:
                img.seek(0)
                files.append(
                    ("images", (img.name, img.read(), img.content_type or "image/jpeg"))
                )

            full_url = "https://70ce-2001-ee0-1b2-193f-b469-84ad-7bfd-1f0f.ngrok-free.app/ai/create-image-features"
            response = requests.post(full_url, data=data, files=files)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"AI server responded with {response.status_code}: {response.text}"
                )
                return {
                    "success": False,
                    "error": f"Server responded with {response.status_code}",
                }

        except requests.RequestException as e:
            logger.error(f"Error connecting to AI server: {e}")
            return {"success": False, "error": str(e)}

    def verify_face(self, image_data, account_id):
        try:
            if isinstance(image_data, str) and image_data.startswith("data:image"):
                image_data = image_data.split(",")[1]
            binary_image = base64.b64decode(image_data)
            data = {"account_id": account_id}
            files = {"image": ("image.jpg", binary_image, "image/jpeg")}
            full_url = "https://70ce-2001-ee0-1b2-193f-b469-84ad-7bfd-1f0f.ngrok-free.app/ai/face-recognization"
            response = requests.post(full_url, data=data, files=files)
            print("Response status:", response.status_code)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"AI server responded with {response.status_code}: {response.text}"
                )
                return {
                    "success": False,
                    "error": f"Server responded with {response.status_code}",
                }

        except requests.RequestException as e:
            logger.error(f"Error verifying face with AI server: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error in verify_face: {e}")
            return {"success": False, "error": f"Lỗi xử lý: {str(e)}"}
