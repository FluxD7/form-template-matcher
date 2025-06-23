import pytest
from tinydb import TinyDB
import os
import stat
from init_db import init_db

def test_init_db_creates_correct_templates():
    if os.path.exists('forms.json'):
        os.remove('forms.json')

    init_db()

    db = TinyDB('forms.json')
    templates = db.all()
    
    assert len(templates) == 3
    assert templates[0] == {
        'name': 'Данные пользователя',
        'login': 'email',
        'tel': 'phone'
    }
    assert templates[1] == {
        'name': 'Форма заказа',
        'customer': 'text',
        'order_id': 'text',
        'дата_заказа': 'date',
        'contact': 'phone'
    }
    assert templates[2] == {
        'name': 'Проба',
        'f_name1': 'email',
        'f_name2': 'date'
    }

def test_init_db_error_handling():
    if os.path.exists('forms.json'):
        os.remove('forms.json')
    os.makedirs('forms.json')
    try:
        with pytest.raises(Exception, match="Failed to initialize database"):
            init_db()
    finally:
        os.rmdir('forms.json')
        init_db()