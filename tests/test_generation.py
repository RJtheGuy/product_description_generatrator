import pytest
from app.services.parsing import TextParser
from app.services.generate import ProductDescriptionGenerator
from unittest.mock import Mock, AsyncMock

class TestTextParser:
    def test_clean_text(self):
        parser = TextParser()
        raw_text = "This   is    a    test!!!   @#$   text."
        cleaned = parser.clean_text(raw_text)
        assert "This is a test text." in cleaned
    
    def test_extract_key_features(self):
        parser = TextParser()
        text = "This product features waterproof design. It includes USB charging. Made with premium materials."
        features = parser.extract_key_features(text)
        assert len(features) > 0
        assert any("waterproof" in feature.lower() for feature in features)

@pytest.mark.asyncio
class TestProductDescriptionGenerator:
    async def test_generate_description_mock(self):
        # Mock the Ollama client
        mock_client = Mock()
        mock_client.generate = AsyncMock(return_value="This is a test product description.")
        
        generator = ProductDescriptionGenerator(mock_client)
        
        result = await generator.generate_description(
            product_name="Test Product",
            raw_text="Raw product information",
            category="Test Category"
        )
        
        assert "test product description" in result.lower()
        mock_client.generate.assert_called_once()
