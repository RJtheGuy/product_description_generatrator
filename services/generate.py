import asyncio
import logging
from typing import Optional
from app.services.parsing import TextParser
from app.utils.ollama_client import OllamaClient

logger = logging.getLogger(__name__)

class ProductDescriptionGenerator:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        self.text_parser = TextParser()
    
    async def generate_description(
        self,
        product_name: str,
        raw_text: str,
        category: Optional[str] = None,
        target_length: Optional[int] = 150
    ) -> str:
        """
        Generate a product description from raw text
        """
        try:
            # Step 1: Clean and parse the raw text
            cleaned_text = self.text_parser.clean_text(raw_text)
            key_features = self.text_parser.extract_key_features(cleaned_text)
            
            # Step 2: Create prompt
            prompt = self._build_prompt(
                product_name=product_name,
                cleaned_text=cleaned_text,
                key_features=key_features,
                category=category,
                target_length=target_length
            )
            
            # Step 3: Generate description using Ollama
            description = await self.ollama_client.generate(prompt)
            
            # Step 4: Post-process the generated description
            final_description = self.text_parser.post_process_description(description)
            
            return final_description
            
        except Exception as e:
            logger.error(f"Error generating description for {product_name}: {str(e)}")
            raise e
    
    def _build_prompt(
        self,
        product_name: str,
        cleaned_text: str,
        key_features: list,
        category: Optional[str] = None,
        target_length: Optional[int] = 150
    ) -> str:
        """Build the prompt for the language model"""
        
        category_context = f"Category: {category}\n" if category else ""
        features_text = "\n".join([f"- {feature}" for feature in key_features])
        
        prompt = f"""
You are a professional product description writer. Create an engaging, SEO-friendly product description.

Product Name: {product_name}
{category_context}
Raw Information: {cleaned_text}

Key Features:
{features_text}

Instructions:
- Write a compelling product description of approximately {target_length} words
- Focus on benefits, not just features
- Use persuasive, customer-focused language
- Include relevant keywords naturally
- Structure with clear paragraphs
- End with a call-to-action feel

Product Description:
"""
        return prompt.strip()
