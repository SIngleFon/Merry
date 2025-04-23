import os
from flask import Flask, render_template, request, jsonify, url_for, redirect
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user="u3104955_singlef", 
            password=os.getenv('MYSQL_PASS'), 
            host="localhost",
            port="3306",
            database="u3104955_default"
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

@application.route("/invitelist")
def invite_list():
    try:
        # Подключаемся к базе данных
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Используем dictionary=True для удобства работы с данными

        # Извлекаем данные из таблицы
        cursor.execute("SELECT * FROM survey_responses")
        responses = cursor.fetchall()

        cursor.close()
        conn.close()

        # Передаём данные в шаблон
        return render_template('invitelist.html', responses=responses)
    except Exception as e:
        print(f"Ошибка при извлечении данных: {e}")
        return jsonify({"error": f"Произошла ошибка: {str(e)}"}), 500
    
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

        # Логируем полученные данные
        print(f"attendance: {attendance}")
        print(f"names: {names}")
        print(f"drinks: {drinks}")
        print(f"non_alcoholic_drink: {non_alcoholic_drink}")

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
        # Логируем подробности ошибки
        print(f"Ошибка при обработке данных: {e}")
        return jsonify({"error": f"Произошла ошибка: {str(e)}"}), 500


if __name__ == '__main__':
    # application.run(debug=True, host='0.0.0.0')
    application.run(debug=False)

