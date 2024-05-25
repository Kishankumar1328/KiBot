from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# Set your API key
genai.configure(api_key="Your_api_key")

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KI Bot</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .chat-container {
            width: 100%;
            max-width: 800px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .chat-box {
            width: 100%;
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 10px;
            border-radius: 10px;
            background-color: #f0f0f0;
        }
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 10px;
            word-wrap: break-word;
            position: relative;
            max-width: 80%;
            background-color: #f0f0f0;
            color: #333;
        }
        .user-message {
            background-color: #007bff;
            color: #fff;
            align-self: flex-end;
            border-top-right-radius: 0;
        }
        .ki-bot-message {
            background-color: #fff;
            color: #333;
            align-self: flex-start;
            border-top-left-radius: 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .message-box {
            display: flex;
            align-items: center;
            border-top: 1px solid #ccc;
            padding-top: 10px;
            width: 100%;
        }
        .message-box input[type="text"] {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 5px 0 0 5px;
            font-size: 16px;
            outline: none;
            margin-right: 10px;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .message-box button {
            padding: 10px 20px;
            border: none;
            border-radius: 0 5px 5px 0;
            background-color: #007bff;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .message-box button:hover {
            background-color: #0056b3;
        }
        .loader {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #007bff;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 2s linear infinite;
            position: absolute;
            top: 50%;
            right: 10px;
            transform: translateY(-50%);
            display: none;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Responsive styles */
        @media only screen and (max-width: 600px) {
            .chat-container {
                padding: 10px;
            }
            .message-box input[type="text"] {
                font-size: 14px;
            }
            .message-box button {
                padding: 8px 16px;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1 style="text-align: center; color: #007bff;">KI Bot</h1>
        <div id="chat-box" class="chat-box"></div>
        <div class="message-box">
            <input type="text" id="user-input" placeholder="Type your message here..." />
            <button onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
            <div class="loader"></div>
        </div>
    </div>

    <script>
        function addMessage(text, className) {
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.textContent = text;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function sendMessage() {
            const userInput = document.getElementById('user-input').value;
            if (userInput.trim() === '') return;
            addMessage(userInput, 'user-message');
            document.getElementById('user-input').value = '';

            const loader = document.querySelector('.loader');
            loader.style.display = 'block';

            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'message=' + encodeURIComponent(userInput)
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, 'ki-bot-message'); // Change 'bot-message' to 'ki-bot-message'
                loader.style.display = 'none';
            });
        }

        document.getElementById('user-input').focus();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/chat", methods=["POST"])
def chat_response():
    user_message = request.form["message"]
    response = chat.send_message(user_message)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
