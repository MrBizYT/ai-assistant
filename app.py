from flask import Flask, request, jsonify, render_template_string
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

# Константы (потом заменишь на переменные окружения)
HF_TOKEN = os.environ.get('HF_TOKEN', '')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')

# ============================================
# ГЛАВНАЯ СТРАНИЦА
# ============================================
@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Free AI Assistant</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            h1 {
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 30px;
            }
            .status {
                background: rgba(255,255,255,0.2);
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .endpoints {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 30px;
            }
            .endpoint {
                background: rgba(255,255,255,0.15);
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #ffd700;
            }
            .endpoint h3 {
                margin: 0 0 10px 0;
                color: #ffd700;
            }
            .endpoint code {
                background: rgba(0,0,0,0.3);
                padding: 5px 10px;
                border-radius: 5px;
                display: inline-block;
                margin: 5px 0;
            }
            .btn {
                background: #ffd700;
                color: #333;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                text-decoration: none;
                display: inline-block;
                margin-top: 10px;
            }
            .btn:hover {
                background: #ffed4a;
            }
            footer {
                text-align: center;
                margin-top: 40px;
                color: rgba(255,255,255,0.7);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Free AI Assistant</h1>
            
<div class="status">
    <h2>✅ Сервер работает!</h2>
    <p>Время: {{ time }}</p>
    <p>Статус: <span style="color: #90EE90;">Live</span></p>
    <p>Модель: 🤖 Dolphin (без цензуры)</p>
</div>

<!-- ЧАТ БЛОК - добавляем сюда -->
<div style="background: rgba(255,255,255,0.15); border-radius: 10px; padding: 20px; margin: 20px 0;">
    <h3>💬 Напиши сообщение:</h3>
    <input type="text" id="messageInput" 
           style="width: 100%; padding: 15px; font-size: 16px; border: none; border-radius: 5px; margin-bottom: 10px; box-sizing: border-box;" 
           placeholder="Введи сообщение...">
    
    <button onclick="sendMessage()" 
            style="background: #ffd700; color: #333; border: none; padding: 12px 25px; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 16px;">
        Отправить ➡️
    </button>
    
    <div id="responseBox" style="margin-top: 20px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; display: none;">
        <strong>Ответ:</strong>
        <pre id="responseText" style="margin: 10px 0 0 0; white-space: pre-wrap; word-wrap: break-word;"></pre>
    </div>
</div>

<script>
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const box = document.getElementById('responseBox');
    const text = document.getElementById('responseText');
    const message = input.value.trim();
    
    if (!message) {
        alert('Введи сообщение!');
        return;
    }
    
    box.style.display = 'block';
    text.textContent = 'Думаю... 🤔';
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        
        const data = await response.json();
        text.textContent = data.response || 'Нет ответа';
    } catch (error) {
        text.textContent = 'Ошибка: ' + error.message;
    }
}

// Отправка по Enter
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
</script>

            <h2>📡 Доступные endpoints:</h2>
            <div class="endpoints">
                <div class="endpoint">
                    <h3>🏠 Главная</h3>
                    <code>GET /</code>
                    <p>Эта страница</p>
                </div>
                
                <div class="endpoint">
                    <h3>❤️ Проверка здоровья</h3>
                    <code>GET /health</code>
                    <p>Проверка работы сервера</p>
                </div>
                
                <div class="endpoint">
                    <h3>💬 Чат API</h3>
                    <code>POST /chat</code>
                    <p>Отправить сообщение</p>
                </div>
                
                <div class="endpoint">
                    <h3>🤖 Telegram Bot</h3>
                    <code>POST /webhook</code>
                    <p>Для Telegram бота</p>
                </div>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <a href="/health" class="btn">Проверить Health</a>
                <button onclick="testChat()" class="btn">Тест Chat API</button>
            </div>

            <div id="result" style="margin-top: 20px; display: none;">
                <h3>Результат:</h3>
                <pre style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 5px; overflow-x: auto;"></pre>
            </div>

            <footer>
                <p>Создано для свободного ИИ • Бесплатно • Без цензуры</p>
            </footer>
        </div>

        <script>
            async function testChat() {
                const result = document.getElementById('result');
                const pre = result.querySelector('pre');
                
                result.style.display = 'block';
                pre.textContent = 'Отправка запроса...';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: 'Привет! Как дела?'})
                    });
                    
                    const data = await response.json();
                    pre.textContent = JSON.stringify(data, null, 2);
                } catch (error) {
                    pre.textContent = 'Ошибка: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# ============================================
# HEALTH CHECK
# ============================================
@app.route('/health')
def health():
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.now().isoformat(),
        'service': 'ai-assistant'
    }), 200

# ============================================
# CHAT API (основной функционал)
# ============================================
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # ЗДЕСЬ БУДЕТ ПОДКЛЮЧЕНИЕ К РЕАЛЬНОЙ МОДЕЛИ
        # Пока просто эхо + небольшая логика
        
        # Простая обработка сообщения
        response_text = generate_response(user_message)
        
        return jsonify({
            'response': response_text,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# ФУНКЦИЯ ГЕНЕРАЦИИ ОТВЕТА (временная)
# ============================================
def generate_response(message):
    """Временная функция-заглушка. Позже заменим на реальную модель."""
    message = message.lower()
    
    # Простые правила для демо
    if 'привет' in message or 'здравствуй' in message:
        return "Привет! Как я могу помочь?"
    elif 'как дела' in message:
        return "У меня всё отлично! Работаю, помогаю людям."
    elif 'who are you' in message or 'кто ты' in message:
        return "Я свободный ИИ-ассистент. Могу говорить на любые темы без цензуры."
    elif 'censorship' in message or 'цензура' in message:
        return "У меня нет цензуры! Можешь спрашивать что угодно."
    else:
        return f"Эхо: {message}\n\n(Скоро здесь будет настоящий ИИ через Hugging Face)"

# ============================================
# ДЛЯ TELEGRAM БОТА (webhook)
# ============================================
@app.route('/webhook', methods=['POST'])
def webhook():
    """Для подключения Telegram бота позже"""
    try:
        data = request.json
        # Здесь будет обработка сообщений от Telegram
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# ИНФОРМАЦИЯ О СЕРВЕРЕ
# ============================================
@app.route('/info')
def info():
    return jsonify({
        'name': 'Free AI Assistant',
        'version': '1.0.0',
        'features': ['chat', 'health', 'webhook'],
        'status': 'active',
        'model': 'coming soon (Hugging Face)'
    })

# ============================================
# ЗАПУСК
# ============================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

