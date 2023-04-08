from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

app = Flask(__name__)
# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-squad")
model = AutoModelForQuestionAnswering.from_pretrained("savasy/bert-base-turkish-squad")
nlp = pipeline("question-answering", model=model, tokenizer=tokenizer)
with open("C:/Users/Hpi5-9/Desktop/bertturkishchatbotforinternship/passage.txt", "r", encoding="utf-8") as f:
    text = f.read()

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data['question']
    results = nlp(question=question, context=text, top_k = 5)
    result = max(results, key=lambda x: len(x['answer']))
    return jsonify({'answer': result['answer']}), 200

if __name__ == '__main__':
    app.run()
