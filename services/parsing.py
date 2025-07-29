import re
import string
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class TextParser:
    def __init__(self):
        # Option 1: Basic stop words (current approach)
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        # Option 2: Use NLTK stop words (uncomment to use)
        # try:
        #     import nltk
        #     from nltk.corpus import stopwords
        #     nltk.download('stopwords', quiet=True)
        #     self.stop_words = set(stopwords.words('english'))
        # except ImportError:
        #     # Fallback to basic stop words if NLTK not available
        #     self.stop_words = {
        #         'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        #         'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
        #         'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        #     }
        
        # Option 3: Extended manual stop words
        # self.stop_words = {
        #     # Articles
        #     'the', 'a', 'an',
        #     # Conjunctions
        #     'and', 'or', 'but', 'so', 'yet', 'nor',
        #     # Prepositions
        #     'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'about', 
        #     'into', 'through', 'during', 'before', 'after', 'above', 'below', 
        #     'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further',
        #     # Common verbs
        #     'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 
        #     'had', 'having', 'do', 'does', 'did', 'doing', 'will', 'would', 
        #     'could', 'should', 'may', 'might', 'must', 'can',
        #     # Pronouns
        #     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
        #     'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
        #     'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 
        #     'they', 'them', 'their', 'theirs', 'themselves',
        #     # Other common words
        #     'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 
        #     'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
        #     'has', 'had', 'having', 'do', 'does', 'did', 'will', 'would', 
        #     'should', 'could', 'can', 'may', 'might', 'must', 'shall'
        # }
    
    def clean_text(self, raw_text: str) -> str:
        """Clean and normalize raw text input"""
        if not raw_text:
            return ""
        
        # Remove extra whitespace and normalize
        text = ' '.join(raw_text.split())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-\.\,\!\?\:]', ' ', text)
        
        # Fix multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_key_features(self, text: str, max_features: int = 10) -> List[str]:
        """Extract key features from cleaned text"""
        if not text:
            return []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        features = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and len(sentence) < 200:  # Reasonable length
                # Look for feature indicators
                if any(keyword in sentence.lower() for keyword in [
                    'feature', 'include', 'with', 'has', 'contain', 'made', 'design', 'quality'
                ]):
                    features.append(sentence)
        
        # Also extract bullet points if they exist
        bullet_points = re.findall(r'[-•*]\s*(.+)', text)
        features.extend([point.strip() for point in bullet_points if len(point.strip()) > 5])
        
        # Remove duplicates and limit
        unique_features = list(dict.fromkeys(features))
        return unique_features[:max_features]
    
    def filter_stop_words(self, words: List[str]) -> List[str]:
        """Remove stop words from a list of words"""
        return [word for word in words if word.lower() not in self.stop_words]
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract important keywords excluding stop words"""
        if not text:
            return []
        
        # Tokenize and clean
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter stop words and short words
        keywords = [word for word in words if len(word) > 2 and word not in self.stop_words]
        
        # Count frequency
        from collections import Counter
        word_freq = Counter(keywords)
        
        # Return most common keywords
        return [word for word, count in word_freq.most_common(max_keywords)]
    
    def extract_specifications(self, text: str) -> Dict[str, str]:
        """Extract technical specifications from text"""
        specs = {}
        
        # Common specification patterns
        spec_patterns = [
            r'(\w+):\s*([^\n,;]+)',  # "Color: Blue"
            r'(\w+)\s*=\s*([^\n,;]+)',  # "Weight = 5kg"
            r'(\w+)\s*-\s*([^\n,;]+)',  # "Material - Cotton"
        ]
        
        for pattern in spec_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for key, value in matches:
                if len(key) > 1 and len(value) > 1:
                    specs[key.strip().title()] = value.strip()
        
        return specs
    
    def post_process_description(self, description: str) -> str:
        """Clean up generated description"""
        if not description:
            return ""
        
        # Remove extra whitespace
        description = ' '.join(description.split())
        
        # Ensure proper capitalization at sentence starts
        sentences = re.split(r'([.!?]+)', description)
        processed_sentences = []
        
        for i, sentence in enumerate(sentences):
            if i % 2 == 0 and sentence.strip():  # Actual sentence content
                sentence = sentence.strip()
                if sentence:
                    sentence = sentence[0].upper() + sentence[1:]
                processed_sentences.append(sentence)
            else:
                processed_sentences.append(sentence)
        
        result = ''.join(processed_sentences)
        
        # Remove any remaining artifacts from generation
        result = re.sub(r'\n+', '\n\n', result)  # Normalize line breaks
        result = re.sub(r'\s+', ' ', result)     # Normalize spaces
        
        return result.strip()
