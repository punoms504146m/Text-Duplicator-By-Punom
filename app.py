from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from functools import wraps
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'  # Change in production

# Configuration
ADMIN_CODE = 'PUNOM2024'
TEMPLATES_FILE = 'templates.json'
CONFIG_FILE = 'config.json'

# ---------- Data Layer ----------
def load_templates():
    if os.path.exists(TEMPLATES_FILE):
        with open(TEMPLATES_FILE, 'r') as f:
            return json.load(f)
    # Default templates
    default = {
        'pending': [],
        'approved': [
            {
                'id': 1,
                'name': 'Dragon',
                'category': 'ascii',
                'description': 'Epic dragon ASCII art',
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
                'author': 'System',
                'date_added': '2024-01-01',
                'status': 'approved'
            },
            {
                'id': 2,
                'name': 'Heart & Stars',
                'category': 'ascii',
                'description': 'Beautiful heart and stars design',
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
                'author': 'System',
                'date_added': '2024-01-01',
                'status': 'approved'
            },
            {
                'id': 3,
                'name': 'Ninja',
                'category': 'ascii',
                'description': 'Cool ninja warrior',
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
                'author': 'System',
                'date_added': '2024-01-01',
                'status': 'approved'
            }
        ],
        'rejected': []
    }
    save_templates(default)
    return default

def save_templates(data):
    with open(TEMPLATES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    default = {
        'footer_text': '© 2024 Text Multiplier by Punom. All rights reserved.',
        'footer_links': []
    }
    save_config(default)
    return default

def save_config(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ---------- Admin Decorator ----------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------- Main Page HTML (User Facing) ----------
MAIN_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Multiplier by Punom</title>
    <style>
        /* Copy all styles from previous version, but remove admin panel parts */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .main-container { max-width: 1200px; margin: 0 auto; }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        h1, h2, h3 { color: #333; margin-bottom: 20px; }
        .input-group { margin-bottom: 20px; }
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
        button:hover { background: #5a67d8; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .button-group button { flex: 1; }
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
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
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
        .template-info { margin-bottom: 10px; }
        .template-name { font-weight: bold; font-size: 16px; margin-bottom: 5px; }
        .template-category {
            display: inline-block;
            padding: 3px 8px;
            background: #e2e8f0;
            border-radius: 15px;
            font-size: 12px;
            color: #4a5568;
            margin-right: 5px;
        }
        .template-description { color: #666; font-size: 14px; margin-bottom: 5px; }
        .template-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: #999;
            margin-bottom: 10px;
        }
        .template-actions { display: flex; gap: 10px; }
        .template-actions button { padding: 8px 12px; font-size: 14px; }
        .use-btn { background: #667eea; }
        .preview-btn { background: #17a2b8; }
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
        .modal-close:hover { color: #333; }
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
        /* Footer */
        .footer {
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: #666;
            margin-top: 20px;
        }
        .admin-link {
            display: inline-block;
            margin-top: 10px;
            color: #667eea;
            text-decoration: none;
        }
        .admin-link:hover { text-decoration: underline; }
        @media (max-width: 768px) {
            .template-gallery { grid-template-columns: 1fr; }
            .button-group { flex-direction: column; }
            .mode-group { flex-direction: column; align-items: flex-start; }
        }
    </style>
</head>
<body>
    <div class="main-container">
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
            <button onclick="scrollToTemplates()" style="background: #9f7aea; margin-top: 10px;">📚 Browse Templates</button>
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
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2>🎨 Template Gallery</h2>
                <div>
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
            <div id="templatesLoading" style="display: none; text-align: center; padding: 40px;">Loading templates...</div>
            <div id="templatesContainer" class="template-gallery"></div>
        </div>

        <!-- Footer (dynamic) -->
        <div class="footer">
            <div id="footerContent">{{ footer_text }}</div>
            <a href="/admin" class="admin-link">Admin Panel</a>
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
        let currentTemplates = [];
        let currentPreviewTemplate = null;

        // Message system
        function showMessage(text, type) {
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = 'message ' + type;
            msg.style.display = 'block';
            setTimeout(() => msg.style.display = 'none', 3000);
        }

        // Template upload
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
                body: JSON.stringify({ name, category, description, content })
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
            if (category !== 'all') url += '?category=' + category;
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
            templates.forEach(t => container.appendChild(createTemplateCard(t)));
        }

        function createTemplateCard(template) {
            const card = document.createElement('div');
            card.className = 'template-card';
            let preview = template.content.length > 200 ? template.content.substring(0,200)+'...' : template.content;
            let categoryName = template.category.replace('_',' ').toUpperCase();
            card.innerHTML = `
                <div class="category-badge">${categoryName}</div>
                <div class="template-preview">${preview}</div>
                <div class="template-info">
                    <div class="template-name">${template.name}</div>
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
                </div>
            `;
            return card;
        }

        function useTemplate(id) {
            const t = currentTemplates.find(t => t.id === id);
            if (t) {
                document.getElementById('word').value = t.content;
                generateList();
                showMessage('Template loaded!', 'success');
                window.scrollTo({top:0,behavior:'smooth'});
            }
        }

        function previewTemplate(id) {
            const t = currentTemplates.find(t => t.id === id);
            if (t) {
                currentPreviewTemplate = t;
                document.getElementById('previewTitle').textContent = t.name;
                document.getElementById('previewContent').textContent = t.content;
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

        function filterTemplates() { loadTemplates(); }
        function refreshTemplates() { loadTemplates(); }
        function scrollToTemplates() {
            document.getElementById('templatesSection').scrollIntoView({behavior:'smooth'});
        }

        // Text multiplier functions
        function generateList() {
            const num = parseInt(document.getElementById('number').value);
            const word = document.getElementById('word').value;
            const mode = document.querySelector('input[name="mode"]:checked').value;
            if (!num || num < 1) { showMessage('Please enter a valid number', 'error'); return; }
            if (!word.trim()) { showMessage('Please enter some text', 'error'); return; }
            let out = '';
            for (let i=0; i<num; i++) out += (mode==='withSerial' ? `${i+1}. ${word}` : word) + '\\n';
            document.getElementById('output').textContent = out;
            document.getElementById('copyBtn').disabled = false;
            document.getElementById('downloadBtn').disabled = false;
            showMessage('List generated successfully!', 'success');
        }

        function copyToClipboard() {
            navigator.clipboard.writeText(document.getElementById('output').textContent)
                .then(() => showMessage('Copied to clipboard!','success'))
                .catch(() => showMessage('Failed to copy','error'));
        }

        function downloadText() {
            const text = document.getElementById('output').textContent;
            const blob = new Blob([text], {type:'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = 'list.txt';
            document.body.appendChild(a); a.click(); document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showMessage('File downloaded!','success');
        }

        // Initial load
        window.onload = function() {
            generateList();
            loadTemplates();
        };
    </script>
</body>
</html>'''

# ---------- Admin Panel HTML ----------
ADMIN_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel - Text Multiplier</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a202c;
            padding: 20px;
        }
        .admin-container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1, h2, h3 { color: #2d3748; margin-bottom: 20px; }
        .tabs {
            display: flex;
            gap: 10px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 16px;
            color: #718096;
            border-radius: 5px;
        }
        .tab:hover { background: #edf2f7; }
        .tab.active {
            background: #667eea;
            color: white;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        th { background: #f7fafc; font-weight: 600; }
        tr:hover { background: #f7fafc; }
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin: 2px;
            color: white;
        }
        .btn-sm { padding: 5px 10px; font-size: 12px; }
        .btn-primary { background: #667eea; }
        .btn-success { background: #28a745; }
        .btn-warning { background: #ffc107; color: #333; }
        .btn-danger { background: #dc3545; }
        .btn-info { background: #17a2b8; }
        .status-badge {
            padding: 3px 8px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: 500;
        }
        .status-approved { background: #d4edda; color: #155724; }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-rejected { background: #f8d7da; color: #721c24; }
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 10px;
            max-width: 700px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        .form-group { margin-bottom: 15px; }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #4a5568;
        }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #cbd5e0;
            border-radius: 5px;
        }
        .footer-preview {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <div class="header">
            <h1>🔧 Admin Panel - Text Multiplier</h1>
            <div>
                <span style="margin-right: 15px;">Welcome, Admin</span>
                <a href="/" target="_blank" class="btn btn-info" style="text-decoration: none;">View Site</a>
                <button onclick="logout()" class="btn btn-danger">Logout</button>
            </div>
        </div>

        <!-- Tabs -->
        <div class="card">
            <div class="tabs">
                <button class="tab active" onclick="openTab(event, 'templates-tab')">📋 Templates</button>
                <button class="tab" onclick="openTab(event, 'pending-tab')">⏳ Pending Approval</button>
                <button class="tab" onclick="openTab(event, 'footer-tab')">📝 Footer Settings</button>
            </div>

            <!-- Templates Tab -->
            <div id="templates-tab" class="tab-content active">
                <h2>All Approved Templates</h2>
                <div style="margin-bottom: 15px;">
                    <input type="text" id="searchTemplates" placeholder="Search templates..." style="padding: 8px; width: 300px; border: 1px solid #cbd5e0; border-radius: 5px;">
                    <button onclick="loadTemplates()" class="btn btn-primary">Refresh</button>
                </div>
                <div id="templatesTableContainer">Loading...</div>
            </div>

            <!-- Pending Tab -->
            <div id="pending-tab" class="tab-content">
                <h2>Pending Approval</h2>
                <div id="pendingTableContainer">Loading...</div>
            </div>

            <!-- Footer Tab -->
            <div id="footer-tab" class="tab-content">
                <h2>Footer Settings</h2>
                <div id="footerForm">
                    <div class="form-group">
                        <label for="footerText">Footer Text</label>
                        <input type="text" id="footerText" class="form-control" value="{{ footer_text }}">
                    </div>
                    <button onclick="saveFooter()" class="btn btn-success">Save Footer</button>
                    <div class="footer-preview" id="footerPreview"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Edit Template Modal -->
    <div id="editModal" class="modal">
        <div class="modal-content">
            <h3>Edit Template</h3>
            <div id="editForm"></div>
            <div style="margin-top: 20px; display: flex; gap: 10px;">
                <button onclick="saveTemplateEdit()" class="btn btn-success">Save Changes</button>
                <button onclick="closeEditModal()" class="btn btn-warning">Cancel</button>
            </div>
        </div>
    </div>

    <script>
        let allTemplates = [];
        let editingTemplateId = null;

        // Tab switching
        function openTab(evt, tabName) {
            const tabs = document.getElementsByClassName('tab-content');
            for (let t of tabs) t.classList.remove('active');
            document.getElementById(tabName).classList.add('active');
            const tabBtns = document.getElementsByClassName('tab');
            for (let btn of tabBtns) btn.classList.remove('active');
            evt.currentTarget.classList.add('active');
            
            if (tabName === 'templates-tab') loadTemplates();
            if (tabName === 'pending-tab') loadPending();
            if (tabName === 'footer-tab') loadFooter();
        }

        // Load approved templates
        function loadTemplates() {
            const container = document.getElementById('templatesTableContainer');
            container.innerHTML = 'Loading...';
            fetch('/admin/templates/approved')
                .then(res => res.json())
                .then(data => {
                    allTemplates = data;
                    renderTemplatesTable(data);
                });
        }

        function renderTemplatesTable(templates) {
            const container = document.getElementById('templatesTableContainer');
            if (!templates.length) {
                container.innerHTML = '<p>No templates found.</p>';
                return;
            }
            let html = '<table><tr><th>ID</th><th>Name</th><th>Category</th><th>Description</th><th>Author</th><th>Date</th><th>Actions</th></tr>';
            templates.forEach(t => {
                html += `<tr>
                    <td>${t.id}</td>
                    <td>${t.name}</td>
                    <td>${t.category}</td>
                    <td>${t.description || ''}</td>
                    <td>${t.author || ''}</td>
                    <td>${t.date_added || ''}</td>
                    <td>
                        <button onclick="editTemplate(${t.id})" class="btn btn-primary btn-sm">Edit</button>
                        <button onclick="deleteTemplate(${t.id})" class="btn btn-danger btn-sm">Delete</button>
                    </td>
                </tr>`;
            });
            html += '</table>';
            container.innerHTML = html;
        }

        // Load pending templates
        function loadPending() {
            const container = document.getElementById('pendingTableContainer');
            container.innerHTML = 'Loading...';
            fetch('/admin/templates/pending')
                .then(res => res.json())
                .then(data => {
                    if (!data.length) {
                        container.innerHTML = '<p>No pending templates.</p>';
                        return;
                    }
                    let html = '<table><tr><th>ID</th><th>Name</th><th>Category</th><th>Description</th><th>Content Preview</th><th>Actions</th></tr>';
                    data.forEach(t => {
                        let preview = t.content.length > 50 ? t.content.substring(0,50)+'...' : t.content;
                        html += `<tr>
                            <td>${t.id}</td>
                            <td>${t.name}</td>
                            <td>${t.category}</td>
                            <td>${t.description || ''}</td>
                            <td><pre style="margin:0; font-size:11px;">${preview}</pre></td>
                            <td>
                                <button onclick="approveTemplate(${t.id})" class="btn btn-success btn-sm">Approve</button>
                                <button onclick="rejectTemplate(${t.id})" class="btn btn-warning btn-sm">Reject</button>
                                <button onclick="editTemplate(${t.id})" class="btn btn-primary btn-sm">Edit</button>
                                <button onclick="deleteTemplate(${t.id})" class="btn btn-danger btn-sm">Delete</button>
                            </td>
                        </tr>`;
                    });
                    html += '</table>';
                    container.innerHTML = html;
                });
        }

        // Load footer settings
        function loadFooter() {
            fetch('/admin/footer')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('footerText').value = data.footer_text;
                    document.getElementById('footerPreview').textContent = 'Preview: ' + data.footer_text;
                });
        }

        function saveFooter() {
            const text = document.getElementById('footerText').value;
            fetch('/admin/footer', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({footer_text: text})
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('Footer updated successfully!');
                    loadFooter();
                }
            });
        }

        // Template actions
        function editTemplate(id) {
            fetch(`/admin/templates/${id}`)
                .then(res => res.json())
                .then(template => {
                    editingTemplateId = id;
                    const form = `
                        <div class="form-group">
                            <label>Name</label>
                            <input type="text" id="edit_name" value="${template.name.replace(/"/g, '&quot;')}">
                        </div>
                        <div class="form-group">
                            <label>Category</label>
                            <select id="edit_category">
                                <option value="messenger" ${template.category=='messenger'?'selected':''}>Messenger</option>
                                <option value="whatsapp" ${template.category=='whatsapp'?'selected':''}>WhatsApp</option>
                                <option value="instagram" ${template.category=='instagram'?'selected':''}>Instagram</option>
                                <option value="tiktok" ${template.category=='tiktok'?'selected':''}>TikTok</option>
                                <option value="facebook_comments" ${template.category=='facebook_comments'?'selected':''}>FB Comments</option>
                                <option value="instagram_comments" ${template.category=='instagram_comments'?'selected':''}>IG Comments</option>
                                <option value="tiktok_comments" ${template.category=='tiktok_comments'?'selected':''}>TT Comments</option>
                                <option value="ascii" ${template.category=='ascii'?'selected':''}>ASCII Art</option>
                                <option value="other" ${template.category=='other'?'selected':''}>Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Description</label>
                            <input type="text" id="edit_description" value="${(template.description || '').replace(/"/g, '&quot;')}">
                        </div>
                        <div class="form-group">
                            <label>Content</label>
                            <textarea id="edit_content" rows="10">${template.content.replace(/</g, '&lt;')}</textarea>
                        </div>
                    `;
                    document.getElementById('editForm').innerHTML = form;
                    document.getElementById('editModal').style.display = 'flex';
                });
        }

        function saveTemplateEdit() {
            const data = {
                name: document.getElementById('edit_name').value,
                category: document.getElementById('edit_category').value,
                description: document.getElementById('edit_description').value,
                content: document.getElementById('edit_content').value
            };
            fetch(`/admin/templates/${editingTemplateId}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(res => {
                if (res.success) {
                    alert('Template updated!');
                    closeEditModal();
                    loadTemplates();
                    loadPending();
                }
            });
        }

        function closeEditModal() {
            document.getElementById('editModal').style.display = 'none';
            editingTemplateId = null;
        }

        function approveTemplate(id) {
            fetch(`/admin/templates/approve/${id}`, {method: 'POST'})
                .then(res => res.json())
                .then(() => { loadPending(); loadTemplates(); });
        }

        function rejectTemplate(id) {
            fetch(`/admin/templates/reject/${id}`, {method: 'POST'})
                .then(res => res.json())
                .then(() => loadPending());
        }

        function deleteTemplate(id) {
            if (confirm('Delete this template?')) {
                fetch(`/admin/templates/delete/${id}`, {method: 'DELETE'})
                    .then(res => res.json())
                    .then(() => { loadTemplates(); loadPending(); });
            }
        }

        function logout() {
            fetch('/admin/logout', {method: 'POST'})
                .then(() => window.location.href = '/admin/login');
        }

        // Search filter
        document.addEventListener('DOMContentLoaded', function() {
            const searchInput = document.getElementById('searchTemplates');
            if (searchInput) {
                searchInput.addEventListener('keyup', function() {
                    const term = this.value.toLowerCase();
                    const filtered = allTemplates.filter(t => 
                        t.name.toLowerCase().includes(term) || 
                        (t.description && t.description.toLowerCase().includes(term))
                    );
                    renderTemplatesTable(filtered);
                });
            }
            loadTemplates();
            loadPending();
            loadFooter();
        });
    </script>
</body>
</html>'''

# ---------- Admin Login HTML ----------
LOGIN_HTML = '''<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            width: 350px;
        }
        h2 { margin-bottom: 30px; color: #333; text-align: center; }
        input {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        .error { color: red; margin-top: 10px; text-align: center; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Admin Login</h2>
        <form method="post" action="/admin/login">
            <input type="password" name="code" placeholder="Enter admin code" required>
            <button type="submit">Login</button>
            {% if error %}<div class="error">{{ error }}</div>{% endif %}
        </form>
    </div>
</body>
</html>'''

# ---------- Flask Routes ----------
@app.route('/')
def home():
    config = load_config()
    return render_template_string(MAIN_HTML, footer_text=config['footer_text'])

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        code = request.form.get('code')
        if code == ADMIN_CODE:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template_string(LOGIN_HTML, error='Invalid code')
    return render_template_string(LOGIN_HTML, error=None)

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    return jsonify({'success': True})

@app.route('/admin')
@admin_required
def admin_dashboard():
    config = load_config()
    return render_template_string(ADMIN_HTML, footer_text=config['footer_text'])

# ---------- API Routes ----------
@app.route('/templates/submit', methods=['POST'])
def submit_template():
    data = request.json
    db = load_templates()
    new_id = max([t['id'] for t in db['approved'] + db['pending'] + db['rejected']] or [0]) + 1
    template = {
        'id': new_id,
        'name': data['name'],
        'category': data['category'],
        'description': data.get('description', ''),
        'content': data['content'],
        'author': 'User Submitted',
        'date_added': datetime.now().strftime('%Y-%m-%d'),
        'status': 'pending'
    }
    db['pending'].append(template)
    save_templates(db)
    return jsonify({'success': True})

@app.route('/templates')
def get_templates():
    category = request.args.get('category')
    db = load_templates()
    templates = db['approved'].copy()
    if category and category != 'all':
        templates = [t for t in templates if t['category'] == category]
    return jsonify(templates)

# Admin template endpoints
@app.route('/admin/templates/approved')
@admin_required
def get_approved_templates():
    db = load_templates()
    return jsonify(db['approved'])

@app.route('/admin/templates/pending')
@admin_required
def get_pending_templates():
    db = load_templates()
    return jsonify(db['pending'])

@app.route('/admin/templates/<int:template_id>')
@admin_required
def get_template(template_id):
    db = load_templates()
    for status in ['approved', 'pending', 'rejected']:
        for t in db[status]:
            if t['id'] == template_id:
                return jsonify(t)
    return jsonify({'error': 'Not found'}), 404

@app.route('/admin/templates/<int:template_id>', methods=['PUT'])
@admin_required
def update_template(template_id):
    data = request.json
    db = load_templates()
    for status in ['approved', 'pending', 'rejected']:
        for t in db[status]:
            if t['id'] == template_id:
                t['name'] = data['name']
                t['category'] = data['category']
                t['description'] = data['description']
                t['content'] = data['content']
                save_templates(db)
                return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route('/admin/templates/approve/<int:template_id>', methods=['POST'])
@admin_required
def approve_template(template_id):
    db = load_templates()
    for i, t in enumerate(db['pending']):
        if t['id'] == template_id:
            t['status'] = 'approved'
            db['approved'].append(t)
            db['pending'].pop(i)
            save_templates(db)
            return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route('/admin/templates/reject/<int:template_id>', methods=['POST'])
@admin_required
def reject_template(template_id):
    db = load_templates()
    for i, t in enumerate(db['pending']):
        if t['id'] == template_id:
            t['status'] = 'rejected'
            db['rejected'].append(t)
            db['pending'].pop(i)
            save_templates(db)
            return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route('/admin/templates/delete/<int:template_id>', methods=['DELETE'])
@admin_required
def delete_template(template_id):
    db = load_templates()
    for status in ['approved', 'pending', 'rejected']:
        for i, t in enumerate(db[status]):
            if t['id'] == template_id:
                db[status].pop(i)
                save_templates(db)
                return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route('/admin/footer', methods=['GET'])
@admin_required
def get_footer():
    config = load_config()
    return jsonify(config)

@app.route('/admin/footer', methods=['POST'])
@admin_required
def update_footer():
    data = request.json
    config = load_config()
    config['footer_text'] = data['footer_text']
    save_config(config)
    return jsonify({'success': True})

if __name__ == '__main__':
    # Ensure data files exist
    load_templates()
    load_config()
    app.run(debug=True)
