from tinydb import TinyDB
import os

def init_db():
    try:
        if os.path.exists('forms.json'):
            os.remove('forms.json')
        db = TinyDB('forms.json')
        db.insert({
            "name": "Данные пользователя",
            "login": "email",
            "tel": "phone"
        })
        db.insert({
            "name": "Форма заказа",
            "customer": "text",
            "order_id": "text",
            "дата_заказа": "date",
            "contact": "phone"
        })
        db.insert({
            "name": "Проба",
            "f_name1": "email",
            "f_name2": "date"
        })
    except Exception as e:
        raise Exception(f"Failed to initialize database: {str(e)}")

if __name__ == '__main__':
    init_db()