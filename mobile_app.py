from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# بيانات الفروع
branches = [
    "ملتقى الوسامة (الفرع الرئيسي)",
    "فرع 2",
    "فرع 3",
    "مؤسسة ربيع كير"
]

# بيانات الموظفين
employees = [
    {"name": "أحمد محمد", "branch": "ملتقى الوسامة (الفرع الرئيسي)", "job": "حلاق محترف", "salary": 3500.0},
    {"name": "سعد خالد", "branch": "مؤسسة ربيع كير", "job": "مندوب مبيعات", "salary": 4000.0}
]

# بيانات الوثائق (مع رقم الوثيقة وتاريخ الانتهاء)
documents = [
    {"title": "رخصة البلدية", "number": "LIC-9881", "branch": "ملتقى الوسامة (الفرع الرئيسي)", "expiry": "2026-12-31"},
    {"title": "عقد الإيجار", "number": "CNT-5520", "branch": "مؤسسة ربيع كير", "expiry": "2026-06-15"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إدارة ملتقى الوسامة</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #f8f9fa; margin: 0; padding: 15px; color: #333; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { color: #0d6efd; text-align: center; }
        .card { background: #f1f3f5; padding: 12px; margin-bottom: 10px; border-radius: 8px; border-right: 4px solid #198754; }
        .expired { border-right-color: #dc3545 !important; background: #fff5f5; }
        .warning { border-right-color: #ffc107 !important; background: #fff9db; }
        form { background: #e9ecef; padding: 12px; border-radius: 8px; margin-bottom: 15px; }
        input, select { width: 100%; padding: 8px; margin: 5px 0 10px 0; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box; }
        button { background: #0d6efd; color: white; border: none; padding: 10px; width: 100%; border-radius: 4px; font-weight: bold; cursor: pointer; }
        .nav { display: flex; justify-content: space-around; background: #212529; padding: 10px; border-radius: 8px; margin-top: 20px; }
        .nav a { color: white; text-decoration: none; font-weight: bold; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🏢 نظام إدارة الفروع</h2>
        <hr>
        
        <h3>📂 إضافة وثيقة حكومية جديدة</h3>
        <form action="/add_doc" method="POST">
            <label>نوع الوثيقة:</label>
            <input type="text" name="title" placeholder="مثل: رخصة البلدية، التأمينات" required>
            
            <label>رقم الوثيقة:</label>
            <input type="text" name="number" placeholder="رقم السجل أو الترخيص" required>
            
            <label>الفرع:</label>
            <select name="branch">
                {% for b in branches %}
                <option value="{{ b }}">{{ b }}</option>
                {% endfor %}
            </select>
            
            <label>تاريخ الانتهاء:</label>
            <input type="date" name="expiry" required>
            
            <button type="submit">حفظ الوثيقة</button>
        </form>

        <h3>📋 متابعة الوثائق وتواريخها</h3>
        {% for doc in docs_info %}
        <div class="card {% if doc.days_left < 0 %}expired{% elif doc.days_left <= 30 %}warning{% endif %}">
            <strong>📌 {{ doc.title }}</strong> (رقم: {{ doc.number }})<br>
            <small>الفرع: {{ doc.branch }}</small><br>
            <small>تاريخ الانتهاء: {{ doc.expiry }}</small><br>
            <strong style="color: {% if doc.days_left < 0 %}red{% elif doc.days_left <= 30 %}orange{% else %}green{% endif %};">
                {% if doc.days_left < 0 %}
                    منتهية منذ {{- doc.days_left }} يوم!
                {% elif doc.days_left == 0 %}
                    تنتهي اليوم!
                {% else %}
                    متبقي عليها: {{ doc.days_left }} يوم
                {% endif %}
            </strong>
        </div>
        {% endfor %}

        <div class="nav">
            <a href="/">الوثائق</a>
            <a href="/employees">الموظفين</a>
            <a href="/branches">الفروع</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    today = datetime.now().date()
    docs_info = []
    for doc in documents:
        expiry_date = datetime.strptime(doc['expiry'], "%Y-%m-%d").date()
        days_left = (expiry_date - today).days
        docs_info.append({
            **doc,
            "days_left": days_left
        })
    return render_template_string(HTML_TEMPLATE, docs_info=docs_info, branches=branches)

@app.route('/add_doc', methods=['POST'])
def add_doc():
    title = request.form.get('title')
    number = request.form.get('number')
    branch = request.form.get('branch')
    expiry = request.form.get('expiry')
    
    if title and number and branch and expiry:
        documents.append({
            "title": title,
            "number": number,
            "branch": branch,
            "expiry": expiry
        })
    return redirect(url_for('index'))

@app.route('/employees')
def employees_page():
    html = """
    <html lang="ar" dir="rtl"><body style="font-family:Tahoma; padding:20px; background:#f8f9fa;">
    <h2>👥 سجل الموظفين</h2>
    """
    for emp in employees:
        html += f"""<div style="background:white; padding:10px; margin-bottom:8px; border-radius:6px; border:1px solid #ddd;">
        <b>{emp['name']}</b><br><small>الفرع: {emp['branch']} | الوظيفة: {emp['job']} | الراتب: {emp['salary']} ر.س</small></div>"""
    html += '<br><a href="/">العودة للرئيسية</a></body></html>'
    return html

@app.route('/branches')
def branches_page():
    html = """
    <html lang="ar" dir="rtl"><body style="font-family:Tahoma; padding:20px; background:#f8f9fa;">
    <h2>⚙️ الفروع التجارية</h2>
    <ul>"""
    for b in branches:
        html += f"<li><b>{b}</b></li>"
    html += '</ul><br><a href="/">العودة للرئيسية</a></body></html>'
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)