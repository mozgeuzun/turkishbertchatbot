# Simple Chatbot with Flask, Elasticsearch and BERT-based NLP Pipeline

This is a simple chatbot project built using HTML, Flask, Elasticsearch  and the BERT-based NLP pipeline provided by the savasy/bert-base-turkish-squad model.  <br>
The chatbot asks the user "nasıl yardımcı olabilirim?" (How can I help you?), waits for the user's input, sends the input to the Flask backend, which then processes it using the NLP pipeline to generate an answer, and sends the answer back to the user.
 <br>
## Requirements <br>
-Python 3.6+ <br>
-Flask <br>
-Transformers <br>
-Hugging Face Transformers <br>
-Elasticsearch <br>
## How to Run the Project 
-Clone this repository to your local machine. <br>
-Install the required dependencies using pip: pip install -r requirements.txt. <br>
-Open elasticsearch batch file. (Do not forget to get your Elasticsearch password to connect. It should be in the second parameter: http_auth=('elastic', 'fIs*jD*3To+IpzLP3D+B'))
-Run the Flask app: python app.py. <br>
-Open your web browser and go to http://localhost:5000. <br>
-Start chatting with the chatbot! <br>
## Dataset
The dataset used for training the NLP pipeline is a collection of frequently asked questions for the internship program at Çankaya Üniversitesi.
