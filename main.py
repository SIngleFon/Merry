import os
from flask import Flask, render_template, request, jsonify, url_for, redirect
import sqlite3
from datetime import datetime, timedelta
import hashlib
import hmac
import json
from operator import itemgetter
from typing import Callable, Any, Dict
from urllib.parse import parse_qsl
import jwt
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector


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
app = Flask(__name__)

app.static_folder = 'static'
app.config['SECRET_KEY'] = "asdf139@mmdilarqw!/ASASKqsad"

SECRET_KEY = "asdf139@mmdilarqw!/ASASKqsad"
# TELEGRAM_BOT_TOKEN = "6906358974:AAF7kFk6CsE1sTGxT6mvtXRPCxX511_rRGY"


# SECRET_KEY = os.getenv("SECRET_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")



# @app.route("/miniapp")
# # @token_required
# def web():  
#     return render_template('miniapp.html')  

@app.route("/")
def load_page():  
    return render_template('invite.html')  

@app.route("/submit", methods=["POST"])
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
    app.run(debug=True, host="0.0.0.0", port='80')
    # create_tables()