import os
from transformers import pipeline
from typing import Tuple

# Set tokenizer parallelism environment variable
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class Summarizer:
    def __init__(self):
        # Initialize the summarization pipeline with flan-t5-large
        self.summarizer = pipeline(
            "summarization",
            model="google/flan-t5-large",
            device=-1  # Use CPU
        )

    async def summarize(self, transcript: str) -> Tuple[str, list]:
        """
        Generate a summary and action items from a transcript using flan-t5-large.
        """
        try:
            # Prepare the prompt for summary
            summary_prompt = f"""Summarize the following meeting transcript in a concise way, highlighting the key points discussed:

{transcript}

Summary:"""

            # Generate summary
            summary_result = self.summarizer(
                summary_prompt,
                max_length=150,
                min_length=50,
                do_sample=False
            )
            
            # Extract summary text from the result
            if not summary_result or not isinstance(summary_result, list) or len(summary_result) == 0:
                return "Error: Could not generate summary", []
                
            summary = summary_result[0].get('summary_text', '')
            if not summary:
                return "Error: Empty summary generated", []

            # Prepare the prompt for action items
            action_items_prompt = f"""Extract action items from the following meeting transcript. List only the specific tasks that need to be done:

{transcript}

Action Items:"""

            # Generate action items
            action_items_result = self.summarizer(
                action_items_prompt,
                max_length=200,
                min_length=30,
                do_sample=False
            )
            
            # Process action items into a list
            if not action_items_result or not isinstance(action_items_result, list) or len(action_items_result) == 0:
                return summary, []
                
            action_items_text = action_items_result[0].get('summary_text', '')
            if not action_items_text:
                return summary, []
                
            # Split into individual action items and clean them up
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