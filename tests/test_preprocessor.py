from backend.nlp.preprocessor import clean_text

def test_clean_text_lowercase():
    assert clean_text("HELLO WORLD") == "hello world"

def test_clean_text_url():
    result = clean_text("Visit https://example.com now")
    assert "URL" not in result
    assert "url" in result

def test_clean_text_email():
    result = clean_text("Contact test@example.com")
    assert "email" in result
