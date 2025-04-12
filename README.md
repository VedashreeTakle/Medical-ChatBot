# Medical-ChatBot

# MediDiagnose 🩺💬
AI Medical Assistant using Gemini API, Flask, MongoDB



🧠 _Overview_

MediDiagnose is a smart, AI-powered medical assistant designed to help users identify possible illnesses based on symptoms and receive treatment suggestions. It combines the power of Google's Gemini API, a symptom similarity algorithm, and natural conversation flows to deliver accurate and personalized healthcare assistance.



💡 _Features_

🔍 Symptom Checker: Users can enter their symptoms to get a list of possible diseases and treatments.

🧬 Gemini-Powered Insights: Provides follow-up questions, advice, and friendly chat-like responses via the Gemini API.

📊 Confidence Scores: Each disease prediction comes with a confidence level.

🧠 Smart Matching: Uses cosine similarity to compare user symptoms against a database of known conditions.

💾 MongoDB Integration: Stores user queries and AI responses for future use or learning.

🌐 Web Interface (Flask): Simple and intuitive UI for interacting with the AI.



🏗️ _Tech Stack_
Layer	Tools/Tech Used:
Frontend	HTML, CSS, JavaScript (basic)

Backend	Flask (Python):
AI/ML	Gemini API, Cosine Similarity

Database	MongoDB:
⚙️ How It Works




User Inputs Symptoms 🗣️

→ Symptoms are submitted via a web form.


Symptom Similarity Matching 🧮

→ Cosine similarity is used to match input with known conditions from the dataset.


Prediction and Treatment Suggestion 💊

→ Returns a list of likely diseases with confidence levels and treatment options.


Follow-up via Gemini API 🧠

→ Gemini API takes over to answer questions, provide explanations, and continue the conversation.


Data Storage 📁

→ Interactions are stored in MongoDB for record-keeping and analysis.



🧪 Sample Query

User: "I have a sore throat and mild fever."

MediDiagnose: "It might be Pharyngitis or Common Cold.

Suggested Treatment: Rest, warm fluids, throat lozenges...

Would you like to know how to prevent this in the future?"



🧰 Installation & Setup: 

git clone https://github.com/yourusername/MediDiagnose.git

cd MediDiagnose

pip install -r requirements.txt

python app.py

Make sure to set your Gemini API Key and MongoDB URI in .env or config.




🛣️ Roadmap

 Improve UI using React or Bootstrap

 Add voice-to-text symptom input

 Enable symptom history tracking per user

 Deploy using Docker & Render

 

🤝 Contributing

Pull requests are welcome! If you’d like to add features or fix bugs, feel free to fork the repo and open a PR.
