# TypeAI+ Backend

This is the backend for the TypeAI+ typing improvement application. It uses Flask to serve the API and Groq's LLaMA 3 model to analyze typing samples and provide feedback.

## Setup

1. Clone this repository
2. Install dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`
3. Create a `.env` file with your Groq API key:
   \`\`\`
   GROQ_API_KEY=your_groq_api_key_here
   \`\`\`
4. Run the application:
   \`\`\`
   python app.py
   \`\`\`

## API Endpoints

### POST /analyze

Analyzes the provided text and returns AI feedback.

**Request Body:**
\`\`\`json
{
  "text": "The text to analyze"
}
\`\`\`

**Response:**
\`\`\`json
{
  "feedback": "AI feedback on the typing sample"
}
\`\`\`

## Deployment

This application can be deployed to platforms like Heroku, Vercel, or any other platform that supports Python applications.

For Heroku deployment:
\`\`\`
heroku create
git push heroku main
\`\`\`

Make sure to set the `GROQ_API_KEY` environment variable in your deployment platform.
\`\`\`

Let's also create a simple script to test the Groq API connection:

```python file="test_groq.py"
import os
import groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Initialize Groq client
client = groq.Client(api_key=groq_api_key)

# Test the connection
try:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, can you hear me?"}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    print("Connection successful!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print(f"Error connecting to Groq API: {str(e)}")
