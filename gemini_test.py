import google.generativeai as genai

# Set your API key here
genai.configure(api_key="YOUR_API_KEY")

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate text
response = model.generate_content("Hello, how are you?")
print(response.text)
