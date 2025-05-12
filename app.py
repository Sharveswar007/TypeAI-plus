# Import necessary modules
from flask import Flask, request, jsonify  # Flask framework for web app
from flask_cors import CORS  # Enable Cross-Origin Resource Sharing
import os  # For environment variable access and file operations
import groq  # For interacting with the Groq API
import time  # For time-related operations (if needed)
from dotenv import load_dotenv  # For loading environment variables from a .env file
import shutil  # For file operations (used later in the script)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Groq client
groq_api_key = "Enter your own Groq API key"  # Replace with your actual API key

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set")

print(f"GROQ_API_KEY: {groq_api_key}")

# Pass the API key directly during initialization
groq_client = groq.Client(api_key=groq_api_key)

@app.route('/analyze', methods=['POST'])
def analyze_typing():
    try:
        # Get the text from the request
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        user_text = data['text']
        
        # Prepare the prompt for the LLaMA 3 model
        prompt = f"""
        You are a typing coach analyzing a user's typing sample. Provide helpful feedback on:
        
        1. Typing accuracy (common mistakes, patterns of errors)
        2. Typing efficiency (suggestions for improvement)
        3. Overall assessment and specific tips for improvement
        
        Be constructive, specific, and encouraging. Format your response in clear paragraphs.
        
        Here is the user's typing sample:
        
        "{user_text}"
        """
        
        # Call the Groq API with LLaMA 3 model
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",  # Using LLaMA 3 8B model
            messages=[
                {"role": "system", "content": "You are a helpful typing coach that provides constructive feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        # Extract the feedback from the response
        feedback = response.choices[0].message.content
        
        # Return the feedback
        return jsonify({"feedback": feedback})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Serve static files from the 'static' directory
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    # Create static folder if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Copy the index.html to static folder if it exists in the current directory
    if os.path.exists('index.html') and not os.path.exists('static/index.html'):
        shutil.copy('index.html', 'static/index.html')
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
