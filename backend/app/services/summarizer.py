import os
import httpx
from typing import Tuple
from ..config import settings

# Set tokenizer parallelism environment variable
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class Summarizer:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}

    async def summarize(self, transcript: str) -> Tuple[str, list]:
        """
        Generate a summary and action items from a transcript using Hugging Face Inference API.
        """
        try:
            # Prepare the prompt for summary
            summary_prompt = f"""Summarize the following meeting transcript in a concise way, highlighting the key points discussed:

{transcript}

Summary:"""

            # Generate summary using Hugging Face API
            async with httpx.AsyncClient() as client:
                summary_response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json={"inputs": summary_prompt}
                )
                summary_response.raise_for_status()
                summary = summary_response.json()[0]["summary_text"]

            # Prepare the prompt for action items
            action_items_prompt = f"""Extract action items from the following meeting transcript. List only the specific tasks that need to be done:

{transcript}

Action Items:"""

            # Generate action items using Hugging Face API
            async with httpx.AsyncClient() as client:
                action_items_response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json={"inputs": action_items_prompt}
                )
                action_items_response.raise_for_status()
                action_items_text = action_items_response.json()[0]["summary_text"]

            # Process action items into a list
            action_items = []
            for item in action_items_text.split('\n'):
                item = item.strip()
                if item and not item.lower().startswith('action items:'):
                    # Remove any numbering or bullet points
                    item = item.lstrip('- *1234567890. ')
                    if item:
                        action_items.append(item)

            return summary, action_items

        except Exception as e:
            print(f"Error in summarizer: {str(e)}")
            return "Error generating summary", []

# Create a singleton instance
summarizer = Summarizer() 