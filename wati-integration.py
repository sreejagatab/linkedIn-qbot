"""
Wati API Integration for LinkedIn Profile Bot

This module provides functions to integrate the LinkedIn Profile Query Bot with the Wati API.
"""

import requests
import json
import os
from typing import Dict, Any, Optional, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WatiAPIClient:
    def __init__(self, api_key: str, base_url: str = "https://api.wati.io/api/v1"):
        """
        Initialize the Wati API client.
        
        Args:
            api_key: Wati API key
            base_url: Wati API base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def send_message(self, whatsapp_number: str, message: str) -> Dict[str, Any]:
        """
        Send a message to a WhatsApp number via Wati.
        
        Args:
            whatsapp_number: WhatsApp number to send the message to
            message: Message text
            
        Returns:
            Response from Wati API
        """
        endpoint = f"{self.base_url}/sendSessionMessage/{whatsapp_number}"
        payload = {
            "messageText": message
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message to {whatsapp_number}: {str(e)}")
            return {"error": str(e)}
    
    def send_template_message(
        self, 
        whatsapp_number: str, 
        template_name: str, 
        parameters: List[str]
    ) -> Dict[str, Any]:
        """
        Send a template message to a WhatsApp number via Wati.
        
        Args:
            whatsapp_number: WhatsApp number to send the message to
            template_name: Name of the template to use
            parameters: List of parameter values for the template
            
        Returns:
            Response from Wati API
        """
        endpoint = f"{self.base_url}/sendTemplateMessage"
        payload = {
            "whatsappNumber": whatsapp_number,
            "templateName": template_name,
            "broadcastName": f"linkedin_bot_{template_name}_{whatsapp_number}",
            "parameters": [{"name": f"{{{{1}}}}", "value": param} for param in parameters]
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending template message to {whatsapp_number}: {str(e)}")
            return {"error": str(e)}
    
    def get_conversations(self, page_size: int = 10, page_number: int = 1) -> Dict[str, Any]:
        """
        Get conversations from Wati.
        
        Args:
            page_size: Number of conversations per page
            page_number: Page number
            
        Returns:
            Response from Wati API
        """
        endpoint = f"{self.base_url}/getMessages/{page_size}/{page_number}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting conversations: {str(e)}")
            return {"error": str(e)}
    
    def get_conversation_messages(
        self, 
        whatsapp_number: str, 
        page_size: int = 10, 
        page_number: int = 1
    ) -> Dict[str, Any]:
        """
        Get messages from a specific conversation.
        
        Args:
            whatsapp_number: WhatsApp number of the conversation
            page_size: Number of messages per page
            page_number: Page number
            
        Returns:
            Response from Wati API
        """
        endpoint = f"{self.base_url}/getMessagesWithContact/{whatsapp_number}/{page_size}/{page_number}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting messages for {whatsapp_number}: {str(e)}")
            return {"error": str(e)}
    
    def create_custom_webhook(self, webhook_url: str, events: List[str]) -> Dict[str, Any]:
        """
        Create a custom webhook in Wati.
        
        Args:
            webhook_url: URL to send webhook events to
            events: List of events to subscribe to
            
        Returns:
            Response from Wati API
        """
        endpoint = f"{self.base_url}/createCustomWebhook"
        payload = {
            "webhookUrl": webhook_url,
            "subscriptions": events
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating webhook: {str(e)}")
            return {"error": str(e)}
    
    def delete_webhook(self) -> Dict[str, Any]:
        """
        Delete the webhook in Wati.

        Returns:
            Response from Wati API
        """
        endpoint = f"{self.base_url}/deleteWebhook"
        
        try:
            response = requests.delete(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting webhook: {str(e)}")
            return {"error": str(e)}


class LinkedInBotWatiIntegration:
    def __init__(
        self, 
        wati_api_key: str, 
        bot_api_url: str = "http://localhost:8000",
        wati_api_url: str = "https://api.wati.io/api/v1"
    ):
        """
        Initialize the LinkedIn Bot Wati integration.
        
        Args:
            wati_api_key: Wati API key
            bot_api_url: LinkedIn Bot API URL
            wati_api_url: Wati API URL
        """
        self.wati_client = WatiAPIClient(wati_api_key, wati_api_url)
        self.bot_api_url = bot_api_url
    
    def setup_webhook(self, webhook_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Set up the webhook in Wati.
        
        Args:
            webhook_url: URL to send webhook events to. If None, uses the bot API URL.
            
        Returns:
            Response from Wati API
        """
        if webhook_url is None:
            webhook_url = f"{self.bot_api_url}/wati-webhook"
        
        # Subscribe to message events
        events = ["message"]
        
        return self.wati_client.create_custom_webhook(webhook_url, events)
    
    def process_incoming_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message from Wati.
        
        Args:
            message_data: Message data from Wati webhook
            
        Returns:
            Response from bot API
        """
        try:
            # Extract message text and WhatsApp number
            message_text = message_data.get("payload", {}).get("text", "")
            whatsapp_number = message_data.get("userData", {}).get("waId")
            
            if not message_text or not whatsapp_number:
                logger.warning(f"Missing message text or WhatsApp number: {message_data}")
                return {"error": "Missing message text or WhatsApp number"}
            
            # Send query to bot API
            endpoint = f"{self.bot_api_url}/query"
            payload = {
                "query": message_text,
                "user_id": whatsapp_number,
                "session_id": whatsapp_number
            }
            
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Send response back to user via Wati
            if result.get("success"):
                response_text = result["response"]
            else:
                available_profiles = ", ".join(result.get("available_profiles", []))
                response_text = f"{result['error']}. Available profiles: {available_profiles}"
            
            self.wati_client.send_message(whatsapp_number, response_text)
            
            return {
                "status": "success",
                "whatsapp_number": whatsapp_number,
                "query_result": result
            }
        except Exception as e:
            logger.error(f"Error processing incoming message: {str(e)}")
            return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    # Load configuration
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        
        wati_api_key = config.get("wati_api_key")
        bot_api_url = config.get("bot_api_url", "http://localhost:8000")
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("Config file not found or invalid. Using environment variables.")
        wati_api_key = os.environ.get("WATI_API_KEY")
        bot_api_url = os.environ.get("BOT_API_URL", "http://localhost:8000")
    
    if not wati_api_key:
        logger.error("Wati API key not found in config or environment variables.")
        exit(1)
    
    # Initialize integration
    integration = LinkedInBotWatiIntegration(wati_api_key, bot_api_url)
    
    # Set up webhook
    webhook_result = integration.setup_webhook()
    logger.info(f"Webhook setup result: {webhook_result}")
    
    print("Wati integration initialized. Webhook has been set up.")
    print("The bot will now receive messages from Wati and respond to them.")
    print("Press Ctrl+C to exit.")
    
    # In a real application, you would have a proper server running
    # Here we just keep the script running
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
