import os
from flask import Flask, render_template, request, jsonify, url_for, redirect
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user="root", 
            password=os.getenv('MYSQL_PASS'), 
            host="amvera-singlefon-run-database",
            port="3306",
            database="svadba"
        )
        print("Соединение с базой данных установлено успешно.")
        return conn
    except mysql.connector.Error as err:
        print(f"Ошибка при подключении к базе данных: {err}")
        raise
application = Flask(__name__)

application.static_folder = 'static'


@application.route("/")
def load_page():  
    return render_template('invite.html')  

@application.route("/submit", methods=["POST"])
def submit_survey():
    try:
        # Получаем данные из формы
        attendance = request.form.get("attendance")
        names = request.form.getlist("name[]")
        drinks = request.form.getlist("drinks[]")
        non_alcoholic_drink = request.form.get("non_alcoholic_drink", "")

        # Преобразуем список имен и напитков в строки
        names_str = ", ".join(names)
        drinks_str = ", ".join(drinks)

        # Подключаемся к базе данных
        conn = get_db_connection()
        cursor = conn.cursor()

        # Вставляем данные в таблицу
        cursor.execute(
            """
            INSERT INTO survey_responses (attendance, name, drinks)
            VALUES (%s, %s, %s)
            """,
            (attendance, names_str, drinks_str if drinks_str else non_alcoholic_drink),
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Редирект на главную страницу
        return redirect(url_for('load_page'))
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")
        return jsonify({"error": "Произошла ошибка при обработке данных"}), 500


if __name__ == '__main__':
    application.run(debug=False)
