import json
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="####")


model = genai.GenerativeModel("pro_model")

prompt = """
Respond ONLY in valid JSON format.

Question:
List 3 benefits of Python for data science.

Expected JSON format:
{
  "benefits": [
    "benefit 1",
    "benefit 2",
    "benefit 3"
  ]
}
"""

response = model.generate_content(prompt)


try:
    result = json.loads(response.text)
    print("Valid JSON response:")
    print(result)

except json.JSONDecodeError:
    print("Response is not valid JSON")
    print("Raw response:")
    print(response.text)
