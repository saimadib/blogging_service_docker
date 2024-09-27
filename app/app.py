# app.py
from flask import Flask, request, jsonify
import json
from celery import Celery
import time
from elasticsearch import Elasticsearch, ConnectionError

# Flask app setup
app = Flask(__name__)

# Celery setup for RabbitMQ
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='rpc://',
        broker='amqp://user:password@rabbitmq//'
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

# Elasticsearch client creation
def create_es_client():
    while True:
        try:
            es = Elasticsearch(hosts=["http://elasticsearch:9200"], timeout=30)  # Increase timeout
            if es.ping():
                print("Connected to Elasticsearch")
                return es
            else:
                print("Elasticsearch not ready yet, retrying...")
        except ConnectionError:
            print("Connection error, retrying...")
        time.sleep(5)

es = create_es_client()

# Create index if it doesn't exist
def create_index_if_not_exists(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"Index '{index_name}' created.")

# Call the index creation on startup
create_index_if_not_exists('blogs')

# Blog submission endpoint (POST)
@app.route('/submit_blog', methods=['POST'])
def submit_blog():
    data = request.json
    # Asynchronously queue the blog submission
    process_blog_submission.delay(data)
    return jsonify({"message": "Blog post submitted successfully!"}), 200

# Celery task for processing blog submissions
@celery.task(name='app.process_blog_submission')  # Specify the task name
def process_blog_submission(blog_data):
    es.index(index='blogs', body={
        "blog-title": blog_data['blog-title'],
        "blog-text": blog_data['blog-text'],
        "user-id": blog_data['user-id']
    })
    print(f"Processed blog: {blog_data['blog-title']}")

@app.route('/search_blog', methods=['GET'])
def search_blog():
    search_term = request.args.get('q')
    if not search_term:
        return jsonify({"error": "No search term provided"}), 400

    print(f"Search Term: {search_term}")  # Debugging line

    # Construct the search query
    search_query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "blog-title": search_term
                        }
                    },
                    {
                        "match": {
                            "blog-text": search_term
                        }
                    }
                ]
            }
        }
    }

    try:
        search_result = es.search(index='blogs', body=search_query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    print(f"Search Result: {search_result}")  # Debugging line

    hits = search_result.get('hits', {}).get('hits', [])
    if not hits:
        return jsonify({"message": "No blogs found"}), 404

    blogs = [
        {
            "title": hit['_source']['blog-title'],
            "content": hit['_source']['blog-text'],
            "user_id": hit['_source'].get('user-id', 'Unknown')
        } 
        for hit in hits
    ]
    
    return jsonify(blogs), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
