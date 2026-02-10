from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔢 Numbered List Generator</title>
    <meta name="description" content="Free online tool to generate numbered lists quickly">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🔢</text></svg>">
    <style>
        :root {
            --primary: #4361ee;
            --secondary: #3a0ca3;
            --success: #4cc9f0;
            --dark: #2b2d42;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 2.8rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.1rem;
        }
        
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            border: 1px solid #e9ecef;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--dark);
            font-size: 0.95rem;
        }
        
        input {
            width: 100%;
            padding: 16px;
            font-size: 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            transition: all 0.3s;
            background: #f8fafc;
        }
        
        input:focus {
            outline: none;
            border-color: var(--primary);
            background: white;
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            padding: 18px 32px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s;
            margin-top: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(67, 97, 238, 0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .output-container {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 25px;
            margin: 25px 0;
        }
        
        #output {
            font-family: 'Fira Code', 'Courier New', monospace;
            white-space: pre-wrap;
            min-height: 200px;
            font-size: 15px;
            line-height: 1.6;
            color: #2d3748;
        }
        
        .stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }
        
        .stat {
            background: #edf2f7;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
        }
        
        .action-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 25px;
        }
        
        .action-btn {
            padding: 15px;
            border-radius: 12px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .copy-btn {
            background: #10b981;
            color: white;
        }
        
        .download-btn {
            background: #3b82f6;
            color: white;
        }
        
        .toast {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #10b981;
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s;
            z-index: 1000;
            max-width: 350px;
        }
        
        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }
        
        .toast.error {
            background: #ef4444;
        }
        
        footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 25px;
            border-top: 1px solid #e9ecef;
            color: #6b7280;
            font-size: 0.9rem;
        }
        
        @media (max-width: 640px) {
            .container {
                padding: 25px;
                margin: 10px;
            }
            
            h1 {
                font-size: 2.2rem;
            }
            
            .action-buttons {
                grid-template-columns: 1fr;
            }
            
            .toast {
                left: 20px;
                right: 20px;
                bottom: 20px;
                max-width: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔢 Numbered List Generator</h1>
            <p class="subtitle">Create perfect numbered lists instantly • No signup required</p>
        </header>
        
        <div class="card">
            <div class="form-group">
                <label for="numberInput">How many items?</label>
                <input type="number" id="numberInput" value="10" min="1" max="10000" placeholder="Enter a number">
            </div>
            
            <div class="form-group">
                <label for="textInput">Text for each item</label>
                <input type="text" id="textInput" value="Task" placeholder="What should each item say?">
            </div>
            
            <button class="btn" onclick="generateList()">
                <span>🚀 Generate List Now</span>
            </button>
        </div>
        
        <div class="stats">
            <div class="stat" id="itemCount">0 items</div>
            <div class="stat" id="charCount">0 characters</div>
        </div>
        
        <div class="output-container">
            <pre id="output">Your list will appear here...</pre>
        </div>
        
        <div class="action-buttons">
            <button class="action-btn copy-btn" onclick="copyToClipboard()" id="copyBtn" disabled>
                <span>📋 Copy List</span>
            </button>
            <button class="action-btn download-btn" onclick="downloadText()" id="downloadBtn" disabled>
                <span>⬇️ Download .txt</span>
            </button>
        </div>
        
        <footer>
            <p>✨ Works entirely in your browser • No data sent to servers • 100% Free</p>
            <p style="margin-top: 10px; font-size: 0.8rem;">Bookmark this page for quick access!</p>
        </footer>
    </div>
    
    <div class="toast" id="toast"></div>
    
    <script>
        function generateList() {
            const number = parseInt(document.getElementById('numberInput').value);
            const text = document.getElementById('textInput').value.trim();
            
            // Validation
            if (isNaN(number) || number < 1) {
                showToast('❌ Please enter a valid number greater than 0', true);
                return;
            }
            
            if (!text) {
                showToast('❌ Please enter some text for the items', true);
                return;
            }
            
            if (number > 10000) {
                showToast('❌ Maximum limit is 10,000 items', true);
                return;
            }
            
            // Generate the list
            let output = '';
            for (let i = 0; i < number; i++) {
                output += `${i + 1}. ${text}\n`;
            }
            
            // Update the display
            document.getElementById('output').textContent = output;
            document.getElementById('itemCount').textContent = `${number} item${number !== 1 ? 's' : ''}`;
            document.getElementById('charCount').textContent = `${output.length} characters`;
            
            // Enable action buttons
            document.getElementById('copyBtn').disabled = false;
            document.getElementById('downloadBtn').disabled = false;
            
            showToast(`✅ Generated ${number} items successfully!`);
            
            // Auto-scroll to output
            document.getElementById('output').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
        
        function copyToClipboard() {
            const text = document.getElementById('output').textContent;
            navigator.clipboard.writeText(text)
                .then(() => showToast('✅ Copied to clipboard!'))
                .catch(err => showToast('❌ Failed to copy: ' + err, true));
        }
        
        function downloadText() {
            const text = document.getElementById('output').textContent;
            const date = new Date().toISOString().slice(0, 10);
            const filename = `numbered-list-${date}.txt`;
            
            const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showToast(`✅ Downloaded "${filename}"`);
        }
        
        function showToast(message, isError = false) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = 'toast' + (isError ? ' error' : '');
            toast.classList.add('show');
            
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }
        
        // Enter key support
        document.getElementById('textInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                generateList();
            }
        });
        
        // Generate initial list on load
        window.addEventListener('DOMContentLoaded', generateList);
        
        // Add keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                generateList();
            }
            if (e.ctrlKey && e.key === 'c' && !document.getElementById('copyBtn').disabled) {
                copyToClipboard();
            }
            if (e.ctrlKey && e.key === 's' && !document.getElementById('downloadBtn').disabled) {
                e.preventDefault();
                downloadText();
            }
        });
        
        // Auto-save to localStorage
        setInterval(() => {
            const number = document.getElementById('numberInput').value;
            const text = document.getElementById('textInput').value;
            localStorage.setItem('listGenerator_number', number);
            localStorage.setItem('listGenerator_text', text);
        }, 2000);
        
        // Load from localStorage
        window.addEventListener('DOMContentLoaded', () => {
            const savedNumber = localStorage.getItem('listGenerator_number');
            const savedText = localStorage.getItem('listGenerator_text');
            
            if (savedNumber) {
                document.getElementById('numberInput').value = savedNumber;
            }
            if (savedText) {
                document.getElementById('textInput').value = savedText;
            }
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML)

@app.route('/api/generate', methods=['POST'])
def generate_api():
    # This endpoint is available but not used in the frontend
    # The frontend generates lists locally
    return {"message": "API available"}

# For Vercel serverless
if __name__ == '__main__':
    app.run(debug=True)
