from flask import Flask, jsonify, request
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)  # Разрешает запросы с любых доменов

# Используем список для хранения студентов
students = [
    {"id": 1, "name": "Иван Иванов", "group": "ПИ-101"},
    {"id": 2, "name": "Мария Петрова", "group": "ИС-202"}
]

@app.route('/')
def home():
    return jsonify({
        "message": "🎓 Student API работает!",
        "endpoints": {
            "GET /students": "Все студенты",
            "POST /students": "Добавить студента",
            "GET /check": "Проверка работы"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "count": len(students),
        "students": students
    })

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Нужно поле 'name'"}), 400
    
    # Находим максимальный ID
    max_id = max([s['id'] for s in students]) if students else 0
    
    student = {
        "id": max_id + 1,
        "name": data['name'],
        "group": data.get('group', 'Не указана'),
        "created": datetime.now().isoformat()
    }
    
    students.append(student) 
    return jsonify(student), 201


@app.route('/check')
def health():
    return jsonify({
        "status": "✅ OK",
        "service": "Student API",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
 
