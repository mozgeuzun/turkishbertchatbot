from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

app = Flask(__name__)

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-squad")
model = AutoModelForQuestionAnswering.from_pretrained("savasy/bert-base-turkish-squad")
nlp = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Connect to Elasticsearch
es = Elasticsearch(
    hosts=['https://localhost:9200'],
    http_auth=('elastic', 'fIs*jD*3To+IpzLP3D+B'),
    verify_certs=False
)

# Create index mapping
index_name = 'passages'
index_mapping = {
    "mappings": {
        "properties": {
            "passage_id": {"type": "integer"},
            "passage": {"type": "text", "analyzer": "turkish"},
        }
    }
}

# Create the index with the custom mapping if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_mapping)

# Index the passages
def index_passages():
    with open("passage.txt", "r", encoding="utf-8") as f:
        passages = f.readlines()

    bulk_data = []
    for i, passage in enumerate(passages):
        doc = {
            'passage_id': i,
            'passage': passage.strip()
        }
        bulk_data.append({
            "_index": index_name,
            "_id": i,
            "_source": doc
        })

    bulk(es, bulk_data)

# Call the function to index the passages
index_passages()

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data['question']

    # Search for relevant passages using Elasticsearch
    search_results = es.search(index=index_name, body={
        'query': {
            'match': {
                'passage': {
                    'query': question,
                    'analyzer': 'turkish'
                }
            }
        },
        'size': 5  # Return top 5 passages
    })

    passages = '\n'.join([hit['_source']['passage'] for hit in search_results['hits']['hits']])
    results = nlp(question=question, context=passages, top_k=5)

    result = max(results, key=lambda x: len(x['answer']))
    return jsonify({'answer': result['answer']}), 200

if __name__ == '__main__':
    app.run()
