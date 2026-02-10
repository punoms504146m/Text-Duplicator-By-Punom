from flask import Flask, render_template_string

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Multiplier by Punom </title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            width: 100%;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px 0;
        }
        button:hover {
            background: #5a67d8;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        #output {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
            min-height: 200px;
            font-family: monospace;
            white-space: pre-wrap;
            margin: 20px 0;
        }
        .button-group {
            display: flex;
            gap: 10px;
        }
        .button-group button {
            flex: 1;
        }
        .copy-btn {
            background: #28a745;
        }
        .download-btn {
            background: #17a2b8;
        }
        .message {
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            display: none;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
    <script src="https://pl27448351.effectivegatecpm.com/a0/c4/ef/a0c4efbdb4a51177f5653938bf3e7d37.js"></script>
</head>
<body>
    <div class="container">
        <h1>Text Multiplier by Punom</h1>
        
        <div id="message" class="message"></div>
        
        <div class="input-group">
            <label for="number">Number of Items:</label>
            <input type="number" id="number" value="5" min="1">
        </div>
        
        <div class="input-group">
            <label for="word">Text for Each Item:</label>
            <input type="text" id="word" value="Item">
        </div>
        
        <button onclick="generateList()">Generate List</button>
        
        <div id="output">Your list will appear here...</div>
        
        <div class="button-group">
            <button class="copy-btn" onclick="copyToClipboard()" id="copyBtn" disabled>Copy</button>
            <button class="download-btn" onclick="downloadText()" id="downloadBtn" disabled>Download</button>
        </div>
    </div>
    <div class="native-banner>
    <script async="async" data-cfasync="false" src="https://pl28687399.effectivegatecpm.com/ea723f805ec00a3c62f8657ef5076b5b/invoke.js"></script>
<div id="container-ea723f805ec00a3c62f8657ef5076b5b"></div>
    </div>

    <script>
        function showMessage(text, type) {
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = 'message ' + type;
            msg.style.display = 'block';
            setTimeout(() => msg.style.display = 'none', 3000);
        }
        
        function generateList() {
            const number = parseInt(document.getElementById('number').value);
            const word = document.getElementById('word').value;
            
            if (!number || number < 1) {
                showMessage('Please enter a valid number', 'error');
                return;
            }
            
            if (!word.trim()) {
                showMessage('Please enter some text', 'error');
                return;
            }
            
            let output = '';
            for (let i = 0; i < number; i++) {
                output += `${i + 1}. ${word}\n`;
            }
            
            document.getElementById('output').textContent = output;
            document.getElementById('copyBtn').disabled = false;
            document.getElementById('downloadBtn').disabled = false;
            
            showMessage('List generated successfully!', 'success');
        }
        
        function copyToClipboard() {
            const text = document.getElementById('output').textContent;
            navigator.clipboard.writeText(text)
                .then(() => showMessage('Copied to clipboard!', 'success'))
                .catch(err => showMessage('Failed to copy', 'error'));
        }
        
        function downloadText() {
            const text = document.getElementById('output').textContent;
            const blob = new Blob([text], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'list.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showMessage('File downloaded!', 'success');
        }
        
        // Generate on page load
        window.onload = generateList;
    </script>
    <script src="https://pl28687305.effectivegatecpm.com/85/ae/57/85ae5719aa3b5fa45f12e80834915e41.js"></script>
</body>
</html>'''

@app.route('/', methods=['GET'])
def home():
    return HTML

if __name__ == '__main__':
    app.run(debug=True)
