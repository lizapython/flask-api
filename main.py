from flask import Flask, jsonify, request
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)  # Разрешает запросы с любых доменов

# Используем список для хранения студентов
students = [
    {'id': 1, 'name': 'Герасимова Бронислав Фролович', 'group': 'БИ-303', 'email': 'xermakov@example.com'},
    {'id': 2, 'name': 'Кудряшова Милица Августович', 'group': 'ИС-202', 'email': 'efrem_1974@example.com'},
    {'id': 3, 'name': 'Князева Дорофей Иосипович', 'group': 'ИС-202', 'email': 'januari1984@example.net'},
    {'id': 4, 'name': 'Суворова Амвросий Викторовна', 'group': 'БИ-303', 'email': 'klavdi2013@example.com'},
    {'id': 5, 'name': 'Овчинникова Аверьян Зиновьевич', 'group': 'ИС-202', 'email': 'valentinafedorova@example.org'},
    {'id': 6, 'name': 'Куликов Антонин Тарасовна', 'group': 'ВТ-505', 'email': 'iljatsvetkov@example.org'},
    {'id': 7, 'name': 'Михайлов Фаина Богдановна', 'group': 'ПИ-101', 'email': 'valentinorlov@example.com'},
    {'id': 8, 'name': 'Сазонов Афиноген Игнатович', 'group': 'ПИ-101', 'email': 'nekrasovsidor@example.net'},        
    {'id': 9, 'name': 'Исаков Фома Жоресович', 'group': 'ИТ-404', 'email': 'veronika1978@example.net'},
    {'id': 10, 'name': 'Семенова Анисим Феликсович', 'group': 'ИС-202', 'email': 'ribakovanaina@example.com'},       
    {'id': 11, 'name': 'Исаев Парфен Трофимович', 'group': 'БИ-303', 'email': 'wkapustin@example.org'},
    {'id': 12, 'name': 'Егорова Феоктист Игоревна', 'group': 'ИС-202', 'email': 'klavdija_98@example.com'},
    {'id': 13, 'name': 'Павлова Владимир Ефстафьевич', 'group': 'ВТ-505', 'email': 'svjatoslav_2025@example.org'},   
    {'id': 14, 'name': 'Гаврилова Ярополк Тарасовна', 'group': 'ИТ-404', 'email': 'vladilen21@example.org'},
    {'id': 15, 'name': 'Цветкова Куприян Александровна', 'group': 'ПИ-101', 'email': 'emilijaaksenova@example.com'}, 
    {'id': 16, 'name': 'Савин Наум Феофанович', 'group': 'ВТ-505', 'email': 'pestovaevgenija@example.net'},
    {'id': 17, 'name': 'Шарапова София Богдановна', 'group': 'ИС-202', 'email': 'klavdija_2013@example.net'},        
    {'id': 18, 'name': 'Трофимов Леонид Теймуразович', 'group': 'ВТ-505', 'email': 'faina1996@example.net'},
    {'id': 19, 'name': 'Федоров Викентий Максимовна', 'group': 'БИ-303', 'email': 'vseslavmuravev@example.org'},     
    {'id': 20, 'name': 'Родионов Касьян Эдуардовна', 'group': 'БИ-303', 'email': 'evpraksija_2015@example.com'},  
]


# Получаем ключ из переменных окружения
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    print("⚠️ ВНИМАНИЕ: API_KEY не установлен в переменных окружения!")
    print("Установите API_KEY в Render Dashboard → Environment Variables")
    API_KEY = "default_key_for_dev"  # только для локальной разработки

# Защита API
@app.before_request
def check_api_key():
    # Разрешаем GET запросы без ключа (для фронтенда)
    if request.method == 'GET':
        return
    
    # Для POST/DELETE проверяем ключ
    if request.method in ['POST', 'DELETE', 'PUT']:
        provided_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not API_KEY:
            return jsonify({"error": "API key not configured on server"}), 500
        
        # if API_KEY == "default_key_for_dev":
        #     return
            
        if provided_key != API_KEY:
            print(f"❌ Неверный ключ! Ожидался: {API_KEY[:5]}..., получен: {provided_key}")
            return jsonify({
                "error": "Invalid API key",
                "message": "Provide valid X-API-Key header"
            }), 403
            
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

# до добавления частичного поиска
# @app.route('/students', methods=['GET'])
# def get_students():
#     group_filter = request.args.get('group')

#     if group_filter:
#         # Фильтруем список по группе
#         filtered = [s for s in students if s.get('group') == group_filter]
#         return jsonify({
#             "count": len(filtered),
#             "students": filtered,
#             "filter": {"group": group_filter}
#         })
#     else:
#         return jsonify({
#             "count": len(students),
#             "students": students
#         })
    # @app.route('/students', methods=['GET'])
# def get_students():
#     return jsonify({
#         "count": len(students),
#         "students": students
#     })

@app.route('/students', methods=['GET']) 
def get_students(): 
    # Получаем параметры запроса 
    search_term = request.args.get('search', '').strip().lower() 
    group_filter = request.args.get('group', '').strip()  # если есть фильтр по группе 
    filtered_students = students  # начинаем со всего списка 
    # Применяем фильтр по группе (если параметр передан) 
    if group_filter: 
        filtered_students = [s for s in filtered_students if s.get('group') == group_filter] 
    # Применяем поиск по имени (если параметр search передан) 
    if search_term: 
        filtered_students = [ 
            s for s in filtered_students 
            if search_term in s.get('name', '').lower() 
        ] 
 
    return jsonify({ 
        "count": len(filtered_students), 
        "students": filtered_students, 
        "filters": { 
            "search": search_term if search_term else None, 
            "group": group_filter if group_filter else None 
        } 
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
 
