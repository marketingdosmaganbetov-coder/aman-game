from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Функция для создания базы данных, если её нет
def init_db():
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS winners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            iin TEXT,
            score INTEGER,
            bonus TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Отдаем страницу с игрой
@app.route('/')
def index():
    return render_template('index.html')

# Принимаем данные от игры после победы
@app.route('/api/claim-bonus', methods=['POST'])
def claim_bonus():
    data = request.json
    phone = data.get('phone')
    iin = data.get('iin')
    score = data.get('score')
    bonus = data.get('bonus')

    # Сохраняем в базу данных
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()
    c.execute("INSERT INTO winners (phone, iin, score, bonus) VALUES (?, ?, ?, ?)",
              (phone, iin, score, bonus))
    conn.commit()
    conn.close()

    # Здесь же в будущем ты сможешь добавить код отправки сообщения в Telegram!

    return jsonify({"status": "success", "message": "Бонус успешно прикреплен!"})

if __name__ == '__main__':
    app.run(debug=True)
