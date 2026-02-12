from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from functools import wraps
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'  # Change this in production

# Mock database (in production, use real database)
TEMPLATES_FILE = 'templates.json'
ADMIN_CODE = 'PUNOM2024'  # Admin approval code

# Initialize templates database
def load_templates():
    if os.path.exists(TEMPLATES_FILE):
        with open(TEMPLATES_FILE, 'r') as f:
            return json.load(f)
    return {
        'pending': [],
        'approved': [],
        'rejected': []
    }

def save_templates(data):
    with open(TEMPLATES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Initial template data
initial_templates = load_templates()
if not initial_templates['approved'] and not initial_templates['pending']:
    initial_templates['approved'] = [
        {
            'id': 1,
            'name': 'Dragon',
            'category': 'ascii',
            'content': '''────────▓▓▓▓▓▓▓────────────▒▒▒▒▒▒
──────▓▓▒▒▒▒▒▒▒▓▓────────▒▒░░░░░░▒▒
────▓▓▒▒▒▒▒▒▒▒▒▒▒▓▓────▒▒░░░░░░░░░▒▒▒
───▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒░░░░░░░░░░░░░░▒
──▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░▒
──▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░▒
─▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░▒
▓▓▒▒▒▒▒▒░░░░░░░░░░░▒▒░░▒▒▒▒▒▒▒▒▒▒▒░░░░░░▒
▓▓▒▒▒▒▒▒▀▀▀▀▀███▄▄▒▒▒░░░▄▄▄██▀▀▀▀▀░░░░░░▒
▓▓▒▒▒▒▒▒▒▄▀████▀███▄▒░▄████▀████▄░░░░░░░▒
▓▓▒▒▒▒▒▒█──▀█████▀─▌▒░▐──▀█████▀─█░░░░░░▒
▓▓▒▒▒▒▒▒▒▀▄▄▄▄▄▄▄▄▀▒▒░░▀▄▄▄▄▄▄▄▄▀░░░░░░░▒
─▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░▒
──▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░▒
───▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▀▀░░░░░░░░░░░░░░▒
────▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒
─────▓▓▒▒▒▒▒▒▒▒▒▒▄▄▄▄▄▄▄▄▄░░░░░░░░▒▒
──────▓▓▒▒▒▒▒▒▒▄▀▀▀▀▀▀▀▀▀▀▀▄░░░░░▒▒
───────▓▓▒▒▒▒▒▀▒▒▒▒▒▒░░░░░░░▀░░░▒▒
────────▓▓▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░▒▒
──────────▓▓▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒
───────────▓▓▒▒▒▒▒▒▒▒░░░░░░░▒▒
─────────────▓▓▒▒▒▒▒▒░░░░░▒▒
───────────────▓▓▒▒▒▒░░░░▒▒
────────────────▓▓▒▒▒░░░▒▒
──────────────────▓▓▒░▒▒
───────────────────▓▒░▒
────────────────────▓▒''',
            'description': 'Epic dragon ASCII art',
            'author': 'System',
            'date_added': '2024-01-01'
        },
        {
            'id': 2,
            'name': 'Heart & Stars',
            'category': 'ascii',
            'content': '''____________________██████
_________▓▓▓▓____█████████
__ Ƹ̵̡Ӝ̵̨̄Ʒ▓▓▓▓▓=▓____▓=▓▓▓▓▓
__ ▓▓▓_▓▓▓▓░●____●░░▓▓▓▓
_▓▓▓▓_▓▓▓▓▓░░__░░░░▓▓▓▓
_ ▓▓▓▓_▓▓▓▓░░♥__♥░░░▓▓▓
__ ▓▓▓___▓▓░░_____░░░▓▓
▓▓▓▓▓____▓░░_____░░▓
_ ▓▓____ ▒▓▒▓▒___ ████
_______ ▒▓▒▓▒▓▒_ ██████
_______▒▓▒▓▒▓▒ ████████
_____ ▒▓▒▓▒▓▒_██████ ███
_ ___▒▓▒▓▒▓▒__██████ _███
_▓▓X▓▓▓▓▓▓▓__██████_ ███
▓▓_██████▓▓__██████_ ███
▓_███████▓▓__██████_ ███
_████████▓▓__██████ _███
_████████▓▓__▓▓▓▓▓▓_▒▒
_████████▓▓__▓▓▓▓▓▓
_████████▓▓__▓▓▓▓▓▓
__████████▓___▓▓▓▓▓▓
_______▒▒▒▒▒____▓▓▓▓▓▓
_______▒▒▒▒▒ _____▓▓▓▓▓
_______▒▒▒▒▒_____ ▓▓▓▓▓
_______▒▒▒▒▒ _____▓▓▓▓▓
________▒▒▒▒______▓▓▓▓▓
________█████____█████''',
            'description': 'Beautiful heart and stars design',
            'author': 'System',
            'date_added': '2024-01-01'
        },
        {
            'id': 3,
            'name': 'Ninja',
            'category': 'ascii',
            'content': '''_'▀█║────────────▄▄───────────​─▄──▄_
──█║───────▄─▄─█▄▄█║──────▄▄──​█║─█║
──█║───▄▄──█║█║█║─▄║▄──▄║█║─█║​█║▄█║
──█║──█║─█║█║█║─▀▀──█║─█║█║─█║​─▀─▀
──█║▄║█║─█║─▀───────█║▄█║─▀▀
──▀▀▀──▀▀────────────▀─█║
───────▄▄─▄▄▀▀▄▀▀▄──▀▄▄▀
──────███████───▄▀
──────▀█████▀▀▄▀
────────▀█▀''',
            'description': 'Cool ninja warrior',
            'author': 'System',
            'date_added': '2024-01-01'
        }
    ]
    save_templates(initial_templates)

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Multiplier by Punom - Template Manager</title>
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
        }
        
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        
        h1, h2, h3 {
            color: #333;
            margin-bottom: 20px;
        }
        
        h1 {
            text-align: center;
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
        
        input, select, textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        textarea {
            font-family: monospace;
            resize: vertical;
            min-height: 150px;
        }
        
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #5a67d8;
        }
        
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .button-group button {
            flex: 1;
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
        
        .mode-group {
            margin-bottom: 20px;
            display: flex;
            gap: 20px;
            align-items: center;
        }
        
        .mode-option {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .mode-option label {
            display: inline;
            font-weight: normal;
            margin-bottom: 0;
        }
        
        .mode-option input[type="radio"] {
            width: auto;
            margin: 0;
        }
        
        /* Template Gallery */
        .template-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .template-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
        }
        
        .template-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .template-preview {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            line-height: 1.4;
            max-height: 150px;
            overflow: hidden;
            position: relative;
            margin-bottom: 10px;
        }
        
        .template-preview::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 50px;
            background: linear-gradient(transparent, #f8f9fa);
            pointer-events: none;
        }
        
        .template-info {
            margin-bottom: 10px;
        }
        
        .template-name {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 5px;
        }
        
        .template-category {
            display: inline-block;
            padding: 3px 8px;
            background: #e2e8f0;
            border-radius: 15px;
            font-size: 12px;
            color: #4a5568;
            margin-right: 5px;
        }
        
        .template-description {
            color: #666;
            font-size: 14px;
            margin-bottom: 5px;
        }
        
        .template-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: #999;
            margin-bottom: 10px;
        }
        
        .template-actions {
            display: flex;
            gap: 10px;
        }
        
        .template-actions button {
            padding: 8px 12px;
            font-size: 14px;
        }
        
        .use-btn {
            background: #667eea;
        }
        
        .preview-btn {
            background: #17a2b8;
        }
        
        .delete-btn {
            background: #dc3545;
        }
        
        .approve-btn {
            background: #28a745;
        }
        
        .reject-btn {
            background: #ffc107;
            color: #333;
        }
        
        .category-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 4px 10px;
            background: #667eea;
            color: white;
            border-radius: 15px;
            font-size: 11px;
            font-weight: 500;
        }
        
        .status-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 15px;
            font-size: 11px;
            font-weight: 500;
            margin-left: 5px;
        }
        
        .status-pending {
            background: #fff3cd;
            color: #856404;
        }
        
        .status-approved {
            background: #d4edda;
            color: #155724;
        }
        
        .status-rejected {
            background: #f8d7da;
            color: #721c24;
        }
        
        /* Admin Panel */
        .admin-panel {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .admin-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .admin-login {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .admin-login input {
            width: auto;
            flex: 1;
        }
        
        .tab-container {
            margin-bottom: 20px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 10px 20px;
            background: none;
            color: #666;
            border: none;
            border-radius: 5px 5px 0 0;
            cursor: pointer;
        }
        
        .tab:hover {
            background: #f0f0f0;
        }
        
        .tab.active {
            background: #667eea;
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        /* Categories */
        .category-filter {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .category-btn {
            background: #f0f0f0;
            color: #333;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
        }
        
        .category-btn.active {
            background: #667eea;
            color: white;
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .modal-close {
            float: right;
            font-size: 24px;
            cursor: pointer;
            color: #999;
        }
        
        .modal-close:hover {
            color: #333;
        }
        
        .full-preview {
            font-family: monospace;
            white-space: pre-wrap;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 14px;
            line-height: 1.5;
        }
        
        @media (max-width: 768px) {
            .template-gallery {
                grid-template-columns: 1fr;
            }
            
            .button-group {
                flex-direction: column;
            }
            
            .mode-group {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Admin Status Bar -->
        <div class="container" id="adminStatus" style="display: none;">
            <div class="admin-header">
                <h3>👑 Admin Panel</h3>
                <button onclick="logoutAdmin()" style="background: #dc3545;">Logout</button>
            </div>
        </div>

        <!-- Admin Login Section (shown when not logged in) -->
        <div class="container" id="adminLoginSection">
            <h3>Admin Access</h3>
            <div class="admin-login">
                <input type="password" id="adminCode" placeholder="Enter admin code">
                <button onclick="loginAdmin()">Login</button>
            </div>
        </div>

        <!-- Main Text Multiplier -->
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

            <div class="mode-group">
                <span style="font-weight: bold; color: #555;">Output Mode:</span>
                <div class="mode-option">
                    <input type="radio" id="modeWithSerial" name="mode" value="withSerial" checked>
                    <label for="modeWithSerial">With Serial Numbers</label>
                </div>
                <div class="mode-option">
                    <input type="radio" id="modeWithoutSerial" name="mode" value="withoutSerial">
                    <label for="modeWithoutSerial">Without Serial Numbers</label>
                </div>
            </div>
            
            <button onclick="generateList()">Generate List</button>
            <div class="button-group">
                <button class="copy-btn" onclick="copyToClipboard()" id="copyBtn" disabled>Copy</button>
                <button class="download-btn" onclick="downloadText()" id="downloadBtn" disabled>Download</button>
            </div>
            
            <div id="output">Your list will appear here...</div>
            
            <!-- Template Button -->
            <button onclick="scrollToTemplates()" style="background: #9f7aea; margin-top: 10px;">
                📚 Browse Templates
            </button>
        </div>

        <!-- Template Upload Section -->
        <div class="container">
            <h2>📤 Upload New Template</h2>
            <p style="color: #666; margin-bottom: 20px;">Submit your ASCII art or text design. Admin approval required.</p>
            
            <div class="input-group">
                <label for="templateName">Template Name:</label>
                <input type="text" id="templateName" placeholder="e.g., Dragon, Heart, Flower...">
            </div>
            
            <div class="input-group">
                <label for="templateCategory">Category:</label>
                <select id="templateCategory">
                    <option value="messenger">Messenger</option>
                    <option value="whatsapp">WhatsApp</option>
                    <option value="instagram">Instagram</option>
                    <option value="tiktok">TikTok</option>
                    <option value="facebook_comments">Facebook Comments</option>
                    <option value="instagram_comments">Instagram Comments</option>
                    <option value="tiktok_comments">TikTok Comments</option>
                    <option value="ascii">ASCII Text Art</option>
                    <option value="other">Other</option>
                </select>
            </div>
            
            <div class="input-group">
                <label for="templateDescription">Description (optional):</label>
                <input type="text" id="templateDescription" placeholder="Brief description of your template">
            </div>
            
            <div class="input-group">
                <label for="templateContent">Template Content:</label>
                <textarea id="templateContent" placeholder="Paste your ASCII art or text design here..."></textarea>
            </div>
            
            <div class="button-group">
                <button onclick="submitTemplate()" style="background: #28a745;">Submit for Approval</button>
                <button onclick="clearUploadForm()" style="background: #6c757d;">Clear</button>
            </div>
        </div>

        <!-- Templates Gallery -->
        <div class="container" id="templatesSection">
            <div class="admin-header">
                <h2>🎨 Template Gallery</h2>
                <div class="admin-login">
                    <select id="categoryFilter" onchange="filterTemplates()" style="width: auto; margin-right: 10px;">
                        <option value="all">All Categories</option>
                        <option value="messenger">Messenger</option>
                        <option value="whatsapp">WhatsApp</option>
                        <option value="instagram">Instagram</option>
                        <option value="tiktok">TikTok</option>
                        <option value="facebook_comments">Facebook Comments</option>
                        <option value="instagram_comments">Instagram Comments</option>
                        <option value="tiktok_comments">TikTok Comments</option>
                        <option value="ascii">ASCII Text Art</option>
                        <option value="other">Other</option>
                    </select>
                    <button onclick="refreshTemplates()">🔄 Refresh</button>
                </div>
            </div>
            
            <div id="templatesLoading" style="display: none; text-align: center; padding: 40px;">
                Loading templates...
            </div>
            
            <div id="templatesContainer" class="template-gallery">
                <!-- Templates will be loaded here -->
            </div>
        </div>
    </div>

    <!-- Preview Modal -->
    <div id="previewModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closePreviewModal()">&times;</span>
            <h3 id="previewTitle">Template Preview</h3>
            <div id="previewContent" class="full-preview"></div>
            <div class="button-group">
                <button onclick="useTemplateFromPreview()" style="background: #667eea;">Use This Template</button>
                <button onclick="closePreviewModal()">Close</button>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let isAdmin = false;
        let currentTemplates = [];
        let currentPreviewTemplate = null;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            checkAdminStatus();
            loadTemplates();
        });
        
        // Message system
        function showMessage(text, type) {
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = 'message ' + type;
            msg.style.display = 'block';
            setTimeout(() => msg.style.display = 'none', 3000);
        }
        
        // Admin functions
        function loginAdmin() {
            const code = document.getElementById('adminCode').value;
            fetch('/admin/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: code})
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    isAdmin = true;
                    document.getElementById('adminLoginSection').style.display = 'none';
                    document.getElementById('adminStatus').style.display = 'block';
                    showMessage('Admin login successful!', 'success');
                    loadTemplates(); // Reload with admin view
                } else {
                    showMessage('Invalid admin code', 'error');
                }
            });
        }
        
        function logoutAdmin() {
            fetch('/admin/logout', {method: 'POST'})
            .then(() => {
                isAdmin = false;
                document.getElementById('adminLoginSection').style.display = 'block';
                document.getElementById('adminStatus').style.display = 'none';
                showMessage('Logged out', 'success');
                loadTemplates(); // Reload without admin view
            });
        }
        
        function checkAdminStatus() {
            fetch('/admin/status')
            .then(res => res.json())
            .then(data => {
                isAdmin = data.isAdmin;
                if (isAdmin) {
                    document.getElementById('adminLoginSection').style.display = 'none';
                    document.getElementById('adminStatus').style.display = 'block';
                }
            });
        }
        
        // Template functions
        function submitTemplate() {
            const name = document.getElementById('templateName').value;
            const category = document.getElementById('templateCategory').value;
            const description = document.getElementById('templateDescription').value;
            const content = document.getElementById('templateContent').value;
            
            if (!name || !content) {
                showMessage('Please enter template name and content', 'error');
                return;
            }
            
            fetch('/templates/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    name: name,
                    category: category,
                    description: description,
                    content: content
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showMessage('Template submitted for approval!', 'success');
                    clearUploadForm();
                    loadTemplates();
                } else {
                    showMessage('Failed to submit template', 'error');
                }
            });
        }
        
        function clearUploadForm() {
            document.getElementById('templateName').value = '';
            document.getElementById('templateCategory').value = 'messenger';
            document.getElementById('templateDescription').value = '';
            document.getElementById('templateContent').value = '';
        }
        
        function loadTemplates() {
            const container = document.getElementById('templatesContainer');
            const loading = document.getElementById('templatesLoading');
            const category = document.getElementById('categoryFilter').value;
            
            loading.style.display = 'block';
            container.innerHTML = '';
            
            let url = '/templates';
            if (category !== 'all') {
                url += '?category=' + category;
            }
            
            fetch(url)
            .then(res => res.json())
            .then(data => {
                currentTemplates = data;
                displayTemplates(data);
                loading.style.display = 'none';
            });
        }
        
        function displayTemplates(templates) {
            const container = document.getElementById('templatesContainer');
            container.innerHTML = '';
            
            if (templates.length === 0) {
                container.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;">No templates found</div>';
                return;
            }
            
            templates.forEach(template => {
                const card = createTemplateCard(template);
                container.appendChild(card);
            });
        }
        
        function createTemplateCard(template) {
            const card = document.createElement('div');
            card.className = 'template-card';
            
            let previewContent = template.content;
            if (previewContent.length > 200) {
                previewContent = previewContent.substring(0, 200) + '...';
            }
            
            let categoryName = template.category.replace('_', ' ').toUpperCase();
            
            let statusHtml = '';
            if (isAdmin && template.status && template.status !== 'approved') {
                statusHtml = `<span class="status-badge status-${template.status}">${template.status}</span>`;
            }
            
            card.innerHTML = `
                <div class="category-badge">${categoryName}</div>
                <div class="template-preview">${previewContent}</div>
                <div class="template-info">
                    <div class="template-name">${template.name} ${statusHtml}</div>
                    <span class="template-category">${template.category}</span>
                    <div class="template-description">${template.description || 'No description'}</div>
                    <div class="template-meta">
                        <span>By: ${template.author || 'Anonymous'}</span>
                        <span>${template.date_added || ''}</span>
                    </div>
                </div>
                <div class="template-actions">
                    <button class="use-btn" onclick="useTemplate(${template.id})">Use</button>
                    <button class="preview-btn" onclick="previewTemplate(${template.id})">Preview</button>
                    ${isAdmin ? `
                        ${template.status === 'pending' ? `
                            <button class="approve-btn" onclick="approveTemplate(${template.id})">Approve</button>
                            <button class="reject-btn" onclick="rejectTemplate(${template.id})">Reject</button>
                        ` : ''}
                        <button class="delete-btn" onclick="deleteTemplate(${template.id})">Delete</button>
                    ` : ''}
                </div>
            `;
            
            return card;
        }
        
        function useTemplate(templateId) {
            const template = currentTemplates.find(t => t.id === templateId);
            if (template) {
                document.getElementById('word').value = template.content;
                generateList();
                showMessage('Template loaded!', 'success');
                window.scrollTo({top: 0, behavior: 'smooth'});
            }
        }
        
        function previewTemplate(templateId) {
            const template = currentTemplates.find(t => t.id === templateId);
            if (template) {
                currentPreviewTemplate = template;
                document.getElementById('previewTitle').textContent = template.name;
                document.getElementById('previewContent').textContent = template.content;
                document.getElementById('previewModal').style.display = 'flex';
            }
        }
        
        function useTemplateFromPreview() {
            if (currentPreviewTemplate) {
                useTemplate(currentPreviewTemplate.id);
                closePreviewModal();
            }
        }
        
        function closePreviewModal() {
            document.getElementById('previewModal').style.display = 'none';
            currentPreviewTemplate = null;
        }
        
        function filterTemplates() {
            loadTemplates();
        }
        
        function refreshTemplates() {
            loadTemplates();
        }
        
        function scrollToTemplates() {
            document.getElementById('templatesSection').scrollIntoView({behavior: 'smooth'});
        }
        
        // Admin template actions
        function approveTemplate(templateId) {
            fetch('/admin/templates/approve/' + templateId, {method: 'POST'})
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showMessage('Template approved!', 'success');
                    loadTemplates();
                }
            });
        }
        
        function rejectTemplate(templateId) {
            fetch('/admin/templates/reject/' + templateId, {method: 'POST'})
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showMessage('Template rejected', 'success');
                    loadTemplates();
                }
            });
        }
        
        function deleteTemplate(templateId) {
            if (confirm('Are you sure you want to delete this template?')) {
                fetch('/admin/templates/delete/' + templateId, {method: 'DELETE'})
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        showMessage('Template deleted', 'success');
                        loadTemplates();
                    }
                });
            }
        }
        
        // Original text multiplier functions
        function generateList() {
            const number = parseInt(document.getElementById('number').value);
            const word = document.getElementById('word').value;
            const mode = document.querySelector('input[name="mode"]:checked').value;
            
            if (!number || number < 1) {
                showMessage('Please enter a valid number', 'error');
                return;
            }
            
            if (!word.trim()) {
                showMessage('Please enter some text', 'error');
                return;
            }
            
            let output = '';
            if (mode === 'withSerial') {
                for (let i = 0; i < number; i++) {
                    output += `${i + 1}. ${word}\n`;
                }
            } else {
                for (let i = 0; i < number; i++) {
                    output += `${word}\n`;
                }
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
        window.onload = function() {
            generateList();
        };
    </script>
</body>
</html>'''

# API Routes
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    if data.get('code') == ADMIN_CODE:
        session['admin_logged_in'] = True
        return jsonify({'success': True})
    return jsonify({'success': False}), 401

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    return jsonify({'success': True})

@app.route('/admin/status')
def admin_status():
    return jsonify({'isAdmin': session.get('admin_logged_in', False)})

@app.route('/templates/submit', methods=['POST'])
def submit_template():
    data = request.json
    templates_db = load_templates()
    
    new_template = {
        'id': max([t['id'] for t in templates_db['approved'] + templates_db['pending'] + templates_db['rejected']] or [0]) + 1,
        'name': data['name'],
        'category': data['category'],
        'description': data.get('description', ''),
        'content': data['content'],
        'author': 'User Submitted',
        'date_added': datetime.now().strftime('%Y-%m-%d'),
        'status': 'pending'
    }
    
    templates_db['pending'].append(new_template)
    save_templates(templates_db)
    return jsonify({'success': True})

@app.route('/templates')
def get_templates():
    category = request.args.get('category')
    templates_db = load_templates()
    
    templates = templates_db['approved'].copy()
    
    # Include pending templates for admin
    if session.get('admin_logged_in'):
        templates.extend(templates_db['pending'])
        templates.extend(templates_db['rejected'])
    
    if category and category != 'all':
        templates = [t for t in templates if t['category'] == category]
    
    return jsonify(templates)

@app.route('/admin/templates/approve/<int:template_id>', methods=['POST'])
@admin_required
def approve_template(template_id):
    templates_db = load_templates()
    
    # Find in pending
    for i, template in enumerate(templates_db['pending']):
        if template['id'] == template_id:
            template['status'] = 'approved'
            templates_db['approved'].append(template)
            templates_db['pending'].pop(i)
            save_templates(templates_db)
            return jsonify({'success': True})
    
    return jsonify({'success': False}), 404

@app.route('/admin/templates/reject/<int:template_id>', methods=['POST'])
@admin_required
def reject_template(template_id):
    templates_db = load_templates()
    
    for i, template in enumerate(templates_db['pending']):
        if template['id'] == template_id:
            template['status'] = 'rejected'
            templates_db['rejected'].append(template)
            templates_db['pending'].pop(i)
            save_templates(templates_db)
            return jsonify({'success': True})
    
    return jsonify({'success': False}), 404

@app.route('/admin/templates/delete/<int:template_id>', methods=['DELETE'])
@admin_required
def delete_template(template_id):
    templates_db = load_templates()
    
    for status in ['approved', 'pending', 'rejected']:
        for i, template in enumerate(templates_db[status]):
            if template['id'] == template_id:
                templates_db[status].pop(i)
                save_templates(templates_db)
                return jsonify({'success': True})
    
    return jsonify({'success': False}), 404

@app.route('/', methods=['GET'])
def home():
    # Initialize templates on startup
    load_templates()
    return HTML

if __name__ == '__main__':
    # Create initial templates if they don't exist
    load_templates()
    app.run(debug=True)
