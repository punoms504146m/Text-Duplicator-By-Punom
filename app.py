from flask import Flask, request, jsonify
import pyperclip

app = Flask(__name__)

# Remove pyperclip for web (it doesn't work on server)
# We'll handle clipboard on client side only

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Numbered List Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2rem;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }
        
        input {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            transition: border-color 0.3s;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 16px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
            margin: 10px 0;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        button:disabled {
            background: #cccccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        #output {
            background: #f8f9fa;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            min-height: 200px;
            margin: 20px 0;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
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
            padding: 15px;
            margin: 15px 0;
            border-radius: 10px;
            display: none;
            text-align: center;
            font-weight: 600;
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
        
        .status {
            text-align: right;
            margin-bottom: 10px;
            font-size: 14px;
            color: #666;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔢 Numbered List Generator</h1>
        
        <div id="message" class="message"></div>
        
        <div class="input-group">
            <label for="number">Number of Items:</label>
            <input type="number" id="number" value="5" min="1" max="1000">
        </div>
        
        <div class="input-group">
            <label for="word">Text for Each Item:</label>
            <input type="text" id="word" value="Item" placeholder="Enter text...">
        </div>
        
        <button id="generateBtn" onclick="generateList()">🚀 Generate List</button>
        
        <div class="status">
            Total Items: <span id="itemCount">0</span>
        </div>
        
        <div id="output">Enter values above and click "Generate List"</div>
        
        <div class="button-group">
            <button id="copyBtn" class="copy-btn" onclick="copyToClipboard()" disabled>📋 Copy to Clipboard</button>
            <button id="downloadBtn" class="download-btn" onclick="downloadText()" disabled>⬇️ Download as .txt</button>
        </div>
        
        <div class="footer">
            <p>Generate numbered lists instantly • No registration required</p>
        </div>
    </div>

    <script>
        async function generateList() {
            const number = document.getElementById('number').value;
            const word = document.getElementById('word').value;
            
            // Validation
            if (!number || number < 1) {
                showMessage('Please enter a valid number greater than 0', 'error');
                return;
            }
            
            if (!word.trim()) {
                showMessage('Please enter some text', 'error');
                return;
            }
            
            // Show loading
            const btn = document.getElementById('generateBtn');
            const originalText = btn.textContent;
            btn.textContent = '⏳ Generating...';
            btn.disabled = true;
            
            try {
                // Generate list locally (no server call needed!)
                let output = '';
                for (let i = 0; i < number; i++) {
                    output += `${i + 1}. ${word}\n`;
                }
                
                // Display output
                document.getElementById('output').textContent = output;
                document.getElementById('itemCount').textContent = number;
                
                // Enable buttons
                document.getElementById('copyBtn').disabled = false;
                document.getElementById('downloadBtn').disabled = false;
                
                showMessage(`✅ Generated ${number} items successfully!`, 'success');
                
            } catch (error) {
                showMessage('Error: ' + error.message, 'error');
            } finally {
                btn.textContent = originalText;
                btn.disabled = false;
            }
        }
        
        function showMessage(text, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.textContent = text;
            messageDiv.className = `message ${type}`;
            messageDiv.style.display = 'block';
            
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 3000);
        }
        
        function copyToClipboard() {
            const text = document.getElementById('output').textContent;
            navigator.clipboard.writeText(text).then(() => {
                showMessage('✅ Copied to clipboard!', 'success');
            }).catch(err => {
                showMessage('❌ Failed to copy: ' + err, 'error');
            });
        }
        
        function downloadText() {
            const text = document.getElementById('output').textContent;
            const blob = new Blob([text], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'numbered-list.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showMessage('✅ File downloaded!', 'success');
        }
        
        // Generate on page load
        window.onload = generateList;
        
        // Generate on Enter key press
        document.getElementById('word').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                generateList();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML

if __name__ == '__main__':
    app.run(debug=True)
