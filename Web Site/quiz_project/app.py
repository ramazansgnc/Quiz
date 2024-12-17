from flask import Flask, render_template, request,  session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Oturum verileri için güvenli anahtar

# Veritabanını başlatma ve soruları ekleme
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Sorular tablosunu oluştur
    c.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT, 
        correct_answer TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT
    )
    ''')
    
    # Soruları ekle
    c.execute('''INSERT OR IGNORE INTO questions (id, question_text, correct_answer, option_a, option_b, option_c, option_d) 
                 VALUES (1, 'Python''da makine öğrenmesi algoritmalarını eğitmek için hangi kütüphaneler kullanılır?', 'NumPy, Pandas, TensorFlow', 'NumPy, Pandas, TensorFlow', 'Matplotlib, Seaborn, OpenCV', 'Flask, Django, Keras', 'SQLite, MySQL, PostgreSQL')''')
    
    c.execute("INSERT OR IGNORE INTO questions (id, question_text, correct_answer, option_a, option_b, option_c, option_d) VALUES (2, 'Hangi algoritma, bir görüntüyü nesnelerine ayırmak için bilgisayar görüşü projelerinde sıkça kullanılır?', 'YOLO (You Only Look Once)', 'K-Means Kümeleme', 'YOLO (You Only Look Once)', 'LSTM', 'KNN (K-Nearest Neighbors)')")

    
    c.execute('''INSERT OR IGNORE INTO questions (id, question_text, correct_answer, option_a, option_b, option_c, option_d) 
                 VALUES (3, 'Doğal dil işleme (NLP) nedir?', 'İnsan dilini makineler aracılığıyla analiz etme', 'İnsan dilini makineler aracılığıyla analiz etme', 'Görüntüleri analiz etme', 'Ses tanıma', 'Matematiksel modeller oluşturma')''')
    
    c.execute('''INSERT OR IGNORE INTO questions (id, question_text, correct_answer, option_a, option_b, option_c, option_d) 
                 VALUES (4, 'Bir yapay zeka modelinin doğruluğunu ölçmek için yaygın olarak kullanılan metriklerden biri nedir?', 'F1 skoru', 'F1 skoru', 'Normal dağılım', 'Konverjans', 'Linear regresyon')''')
    
    conn.commit()
    conn.close()

# Ana sayfa rotası
@app.route('/')
def quiz():
    return render_template('quiz.html')

# Verilen cevapları işler
@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.form
    score = 0

    # Veritabanından sorulara bakıp kontrol eder
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, correct_answer FROM questions")
    questions = c.fetchall()
    conn.close()

    # Her doğru cevap için 25 puan 
    for question_id, correct_answer in questions:
        if user_answers.get(f"question_{question_id}") == correct_answer:
            score += 25  # Her doğru cevap için 25 puan

    # Kullanıcı puanını saklar
    if 'high_score' not in session or score > session['high_score']:
        session['high_score'] = score

    return render_template('result.html', score=score)

# Flask uygulamasını başlat
if __name__ == '__main__':
    init_db()  # Veritabanını başlat
    app.run(debug=True)
