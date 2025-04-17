from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from extract_text import extract_text_from_pdf
from search import search_insurance_plans
from recommend import generate_recommendation

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get uploaded file and form data
        file = request.files['file']
        form_data = request.form

        print("✅ File and form received")

        name = form_data.get('name')
        age = form_data.get('age')
        gender = form_data.get('gender')
        conditions = form_data.get('conditions', '')

        # Extract text from uploaded PDF using Azure Form Recognizer
        try:
            extracted_text = extract_text_from_pdf(file)
            print(f"✅ Extracted text length: {len(extracted_text)}")
        except Exception as e:
            print(f"❌ Failed to extract text: {e}")
            return jsonify({'error': 'Failed to extract text from file'}), 500

        # Search relevant insurance plans using Azure Cognitive Search
        try:
            query = f"{conditions} {extracted_text}"
            plans = search_insurance_plans(query)
            print("✅ Retrieved top insurance search results")
        except Exception as e:
            print(f"❌ Failed to search insurance plans: {e}")
            return jsonify({'error': 'Failed to retrieve insurance plans'}), 500

        # Generate personalized insurance plan recommendation using Azure OpenAI
        try:
            recommendation = generate_recommendation(age,conditions, extracted_text, plans)
            return jsonify({'recommendation': recommendation})
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
