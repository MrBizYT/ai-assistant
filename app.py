from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Здесь будет твой диспетчер задач (как я писал ранее)
# Этот сервер принимает сообщения от пользователей
# и отправляет их в Colab/GPU ферму

# Хранилище для ответов (в реальности используй Redis)
answers = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    user_id = data.get('user_id', 'anonymous')
    
    # Здесь логика отправки задачи в Colab
    # (пока просто заглушка)
    
    return jsonify({
        'status': 'queued',
        'message': 'Задача принята, ждите ответ'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'alive'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)