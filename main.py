from flask import Flask, jsonify, request
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)  # Разрешает запросы с любых доменов

# Используем список для хранения студентов
students = [
    {"id": 1, "name": "Елизавета Дерюга", "group": "ПИ-101"},
    {"id": 2, "name": "Анна Петрова", "group": "ИС-202"}
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
# Добавление
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
# Удаление
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_students(student_id):
    # Ищем студента по id
    for index, student in enumerate(students):
        if student["id"] == student_id:
            deleted_student = students.pop(index)
            return jsonify({"message": "Студент удалён"})
    return jsonify({"error": "Студент не найден"}), 404      

# Редактирование
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Ищем студента по ID
    for i, student in enumerate(students):
        if student['id'] == student_id:
            # Обновляем поля (если они переданы в запросе)
            if 'name' in data:
                student['name'] = data['name']
            if 'group' in data:
                student['group'] = data['group']
            # Можно также добавить обновление даты, если нужно
            # student['updated'] = datetime.now().isoformat()
            
            return jsonify({
                "message": "Студент обновлён",
                "student": student
            }), 200
    
    return jsonify({"error": "Студент не найден"}), 404
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
 
