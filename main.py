from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime  # Import datetime module for date and time

# Flask setup
app = Flask(_name_)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Google Generative AI setup
api_key = "your_api_key_here"
genai.configure(api_key=api_key)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """
    Process the user's text input, send it to AI, and return the response.
    """
    try:
        # Get the text input from the request body
        user_input = request.json.get('text', '')
        if not user_input:
            return jsonify({"error": "No input received"}), 400

        # Check if the user is asking for the date or time
        if "date" in user_input.lower() or "time" in user_input.lower():
            # Get the current date and time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify({"response": f"The current date and time is: {current_datetime}"})
        
        # Check if the user is asking for their location
        if "location" in user_input.lower() or "where am i" in user_input.lower() or "my location" in user_input.lower():
            # This is a placeholder response, you can adjust to provide real GPS location if necessary
            return jsonify({"response": "I am unable to retrieve your exact location. Please enable location services on your device."})
        
        # Generate AI response if not asking for date/time or location
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 100,
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        return jsonify({"response": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)