from flask import Flask, request, jsonify, render_template
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import os
import pandas as pd
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
os.environ["GOOGLE_API_KEY"] = "Replace with actual API key"  # AIzaSyDsOZDBtTqgMZu6j6u3WjMRkgYGyOfwwJ4 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")  # Use "gemini-2.0-pro" if required

# Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["medical_chatbot"]
disease_collection = db["diseases"]

# Fetch dataset from MongoDB
disease_data = list(disease_collection.find({}, {"_id": 0}))

# Ensure fetched data is valid
required_columns = {"Symptoms", "Disease", "Treatments"}
if not all(col in disease_data[0] for col in required_columns):
    raise ValueError("MongoDB data is missing required fields: Symptoms, Disease, or Treatment")

df = pd.DataFrame(disease_data)

embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Small and fast

def get_embeddings(texts):
    return embedder.encode(texts)

# Compute embeddings
all_symptoms = df['Symptoms'].tolist()
all_diseases = df['Disease'].tolist()
all_treatments = df['Treatments'].tolist()
all_embeddings = get_embeddings(all_symptoms)

def find_similar_disease(user_symptoms):
    user_embedding = get_embeddings([user_symptoms])
    similarities = cosine_similarity(user_embedding, all_embeddings)[0]

    top_match_idx = np.argmax(similarities)
    predicted_disease = all_diseases[top_match_idx]
    predicted_treatment = all_treatments[top_match_idx]
    confidence_score = float(similarities[top_match_idx])  # confidence between 0 and 1

    return predicted_disease, predicted_treatment, confidence_score


@app.route('/')
def home():
    return render_template('index3.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_symptoms = data.get("symptoms", "")
    
    if not user_symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    disease, treatment, confidence = find_similar_disease(user_symptoms)
    
    response = model.generate_content(
        f"A patient described their symptoms as: {user_symptoms}. "
        f"The most probable disease is: {disease}. "
        f"Suggested treatment: {treatment}. "
        f"Ask one follow-up question to refine the diagnosis."
    )

    follow_up_question = response.text if response else "Could you describe your symptoms in more detail?"

    return jsonify({
        "disease": disease,
        "treatment": treatment,
        "confidence": confidence,
        "follow_up_question": follow_up_question
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    conversation_history = data.get("history", [])
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
        
    # Generate response using Gemini
    prompt = "The following is a conversation between a doctor and a patient discussing medical symptoms:\n\n"
    for message in conversation_history:
        prompt += f"{'Doctor' if message['sender'] == 'bot' else 'Patient'}: {message['text']}\n"
    prompt += f"Patient: {user_message}\nDoctor:"

    try:
        response = model.generate_content(prompt)
        bot_response = response.text if response else "I'm sorry, I couldn't process your request. Please try again."
    except Exception as e:
        bot_response = "I'm sorry, I couldn't process your request. Please try again."

    return jsonify({
        "response": bot_response
    })

if __name__ == '__main__':
    app.run(debug=True)
