import requests

class TextGenAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def generate_text(self, prompt, max_length=100):
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "prompt": prompt,
            "max_length": max_length
        }
        response = requests.post(endpoint, json=payload)
        if response.status_code == 200:
            return response.json().get("generated_text")
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

# 示例用法
if __name__ == "__main__":
    api = TextGenAPI(base_url="http://localhost:7860")
    prompt = "Once upon a time"
    generated_text = api.generate_text(prompt)
    print(generated_text)