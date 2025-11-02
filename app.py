from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Sample Kubernetes quiz questions with options and correct answers, plus facts for wrong answers
questions = [
    {
        "question": "What is a Pod in Kubernetes?",
        "options": ["A container runtime", "The smallest deployable unit", "A networking service", "A storage volume"],
        "correct": 1,
        "fact": "A Pod is the smallest and simplest Kubernetes object. It represents a single instance of a running process in your cluster and can contain one or more containers."
    },
    {
        "question": "What does a Service in Kubernetes provide?",
        "options": ["Persistent storage", "Load balancing and service discovery", "Configuration management", "Job scheduling"],
        "correct": 1,
        "fact": "A Service is an abstraction that defines a logical set of Pods and a policy by which to access them. It provides load balancing and service discovery."
    },
    {
        "question": "What is a Deployment in Kubernetes?",
        "options": ["A way to store secrets", "A controller for managing stateless applications", "A networking plugin", "A monitoring tool"],
        "correct": 1,
        "fact": "A Deployment provides declarative updates for Pods and ReplicaSets. It allows you to describe the desired state of your application."
    },
    {
        "question": "What is kubectl?",
        "options": ["A container runtime", "The Kubernetes command-line tool", "A GUI dashboard", "A package manager"],
        "correct": 1,
        "fact": "kubectl is the command-line interface for running commands against Kubernetes clusters. It's your primary way to interact with the Kubernetes API."
    },
    {
        "question": "What is a Namespace in Kubernetes?",
        "options": ["A way to isolate resources", "A type of Pod", "A storage class", "A networking policy"],
        "correct": 0,
        "fact": "Namespaces are a way to divide cluster resources between multiple users or teams. They provide scope for names and can be used for resource quotas."
    }
]

@app.route('/')
def home():
    return render_template('quiz.html', questions=questions)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    question_index = data['question_index']
    selected_option = data['selected_option']
    question = questions[question_index]
    is_correct = selected_option == question['correct']
    fact = question['fact'] if not is_correct else None
    return jsonify({'is_correct': is_correct, 'fact': fact})

@app.route('/results')
def results():
    # In a real app, you'd track answers in session or database
    # For simplicity, just show a placeholder
    return render_template('results.html', score=0, total=len(questions), facts=[])

if __name__ == '__main__':
    app.run(debug=True)
