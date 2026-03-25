from deep_translator import GoogleTranslator

def test_translate():
    text = "Hello world. This is a longer paragraph. I want to see if it translates correctly into Malayalam. We should see Malayalam script here."
    target_lang = "ml" # Code for Malayalam
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        print(f"Original: {text}")
        print(f"Translated: {translated}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_translate()
