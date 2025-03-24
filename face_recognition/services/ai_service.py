import requests
import logging

logger = logging.getLogger(__name__)

class AIService:
    """Service to interact with the AI facial recognition server"""
    
    def __init__(self, api_url=None):
        self.api_url = api_url or 'https://3f48-2402-800-629c-32b9-d9a2-3c9f-431e-df1d.ngrok-free.app/ai/'
    
    def send_images(self, account_id, image_files):
        """Send images to AI server for processing
        
        Args:
            account_id: The ID of the account
            image_files: List of image files (from request.FILES)
            
        Returns:
            dict: The response from the AI server
        """
        data = {'account_id': account_id}
        files = []

        try:
            for img in image_files:
                img.seek(0)
                files.append(('images', (img.name, img.read(), img.content_type or 'image/jpeg')))

            response = requests.post(self.api_url, data=data, files=files)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error connecting to AI server: {e}")
            return {"error": str(e), "success": False}