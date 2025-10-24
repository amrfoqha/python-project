import requests
import json

import requests
import json

# key="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"
key="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"
# key="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"


response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {key}"},
    json={
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [
            {
                "role": "user",
                "content": "what is 5 plus 5 ?"
            }
        ]
    }
)

if response.status_code == 200:
    data = response.json()
    print("Success:", json.dumps(data, indent=2))
else:
    print(f"Error {response.status_code}: {response.text}")

