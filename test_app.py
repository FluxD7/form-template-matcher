import pytest
from app import process_template
from init_db import init_db
import os
import stat
import subprocess
import sys

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_form_order_match_partial():
    args = ['app.py', 'get_tpl', '--customer=John Smith', '--дата_заказа=27.05.2025']
    output, exit_code = process_template(args)
    expected = '''{
  "customer": "text",
  "дата_заказа": "date"
}'''
    assert output == expected.strip(), f"Expected: {expected.strip()}, Got: {output}"
    assert exit_code == 0

def test_form_order_match_full():
    args = ['app.py', 'get_tpl', '--customer=John Smith', '--дата_заказа=27.05.2025', '--order_id=12345', '--contact=+7 903 123 45 78']
    output, exit_code = process_template(args)
    assert output == 'Форма заказа', f"Expected: Форма заказа, Got: {output}"
    assert exit_code == 0

def test_user_data_match():
    args = ['app.py', 'get_tpl', '--login=user@example.com', '--tel=+7 903 123 45 78']
    output, exit_code = process_template(args)
    assert output == 'Данные пользователя', f"Expected: Данные пользователя, Got: {output}"
    assert exit_code == 0

def test_probe_match():
    args = ['app.py', 'get_tpl', '--f_name1=vasya@example.com', '--f_name2=15.12.2024']
    output, exit_code = process_template(args)
    assert output == 'Проба', f"Expected: Проба, Got: {output}"
    assert exit_code == 0

def test_probe_match_with_extra_fields():
    args = ['app.py', 'get_tpl', '--login=vasya', '--f_name1=aaa@bbb.ru', '--f_name2=27.05.2025']
    output, exit_code = process_template(args)
    assert output == 'Проба', f"Expected: Проба, Got: {output}"
    assert exit_code == 0

def test_no_matching_template():
    args = ['app.py', 'get_tpl', '--tumba=27.05.2025', '--yumba=+7 903 123 45 78']
    output, exit_code = process_template(args)
    expected = '''{
  "tumba": "date",
  "yumba": "phone"
}'''
    assert output == expected.strip(), f"Expected: {expected.strip()}, Got: {output}"
    assert exit_code == 0

def test_no_matching_template_email_text():
    args = ['app.py', 'get_tpl', '--email=user@example.com', '--name=Anna Petrova']
    output, exit_code = process_template(args)
    expected = '''{
  "email": "email",
  "name": "text"
}'''
    assert output == expected.strip(), f"Expected: {expected.strip()}, Got: {output}"
    assert exit_code == 0

def test_invalid_date():
    args = ['app.py', 'get_tpl', '--f_name1=user@example.com', '--f_name2=31.13.2025']
    output, exit_code = process_template(args)
    expected = '''{
  "f_name1": "email",
  "f_name2": "text"
}'''
    assert output == expected.strip(), f"Expected: {expected.strip()}, Got: {output}"
    assert exit_code == 0

def test_invalid_phone():
    args = ['app.py', 'get_tpl', '--tel=1234567890', '--login=user@example.com']
    output, exit_code = process_template(args)
    expected = '''{
  "tel": "text",
  "login": "email"
}'''
    assert output == expected.strip(), f"Expected: {expected.strip()}, Got: {output}"
    assert exit_code == 0

def test_invalid_email():
    args = ['app.py', 'get_tpl', '--login=user@.com', '--tel=+7 903 123 45 78']
    output, exit_code = process_template(args)
    expected = '''{
  "login": "text",
  "tel": "phone"
}'''
    assert output == expected.strip(), f"Expected: {expected.strip()}, Got: {output}"
    assert exit_code == 0

def test_invalid_argument_format():
    args = ['app.py', 'get_tpl', '--customer']
    output, exit_code = process_template(args)
    assert output == 'Invalid argument: customer', f"Expected: Invalid argument: customer, Got: {output}"
    assert exit_code == 1

def test_invalid_argument_no_dash():
    args = ['app.py', 'get_tpl', 'customer=John Smith']
    output, exit_code = process_template(args)
    assert output == 'Invalid argument: customer=John Smith', f"Expected: Invalid argument: customer=John Smith, Got: {output}"
    assert exit_code == 1

def test_unknown_command():
    args = ['app.py', 'invalid_cmd']
    output, exit_code = process_template(args)
    assert output == 'Unknown command', f"Expected: Unknown command, Got: {output}"
    assert exit_code == 1

def test_too_few_arguments():
    args = ['app.py', 'get_tpl']
    output, exit_code = process_template(args)
    assert output == 'Usage: app.py get_tpl --field1=value1 --field2=value2', f"Expected: Usage: app.py get_tpl --field1=value1 --field2=value2, Got: {output}"
    assert exit_code == 1

def test_date_format_iso():
    args = ['app.py', 'get_tpl', '--tumba=2025-05-27']
    output, exit_code = process_template(args)
    expected = '''{
  "tumba": "date"
}'''
    assert output == expected.strip(), f"Expected: {expected.strip()}, Got: {output}"
    assert exit_code == 0

def test_no_arguments():
    args = ['app.py']
    output, exit_code = process_template(args)
    expected = 'Usage: app.py get_tpl --field1=value1 --field2=value2'
    assert output == expected, f"Expected: {expected}, Got: {output}"
    assert exit_code == 1

def test_missing_db_file():
    if os.path.exists('forms.json'):
        os.remove('forms.json')
    args = ['app.py', 'get_tpl', '--customer=John Smith', '--дата_заказа=27.05.2025']
    output, exit_code = process_template(args)
    expected = "Error: Database file 'forms.json' not found"
    assert output == expected, f"Expected: {expected}, Got: {output}"
    assert exit_code == 1
    init_db()

def test_general_exception():
    if os.path.exists('forms.json'):
        os.remove('forms.json')
    with open('forms.json', 'w') as f:
        f.write('{"valid": "data"}')
    os.chmod('forms.json', stat.S_IREAD)
    try:
        args = ['app.py', 'get_tpl', '--customer=John Smith', '--дата_заказа=27.05.2025']
        output, exit_code = process_template(args)
        assert output.startswith("Error: "), f"Expected: Error message, Got: {output}"
        assert exit_code == 1
    finally:
        os.chmod('forms.json', stat.S_IWRITE)
        os.remove('forms.json')
        init_db()

def test_main_block():
    result = subprocess.run(
        [sys.executable, 'app.py', 'get_tpl', '--customer=John Smith', '--дата_заказа=27.05.2025', '--order_id=12345', '--contact=+7 903 123 45 78'],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == 'Форма заказа', f"Expected: Форма заказа, Got: {result.stdout.strip()}"
    assert result.returncode == 0

def test_general_exception_json():
    if os.path.exists('forms.json'):
        os.remove('forms.json')
    with open('forms.json', 'w') as f:
        f.write('{"invalid": }')
    try:
        args = ['app.py', 'get_tpl', '--customer=John Smith', '--дата_заказа=27.05.2025']
        output, exit_code = process_template(args)
        assert output.startswith("Error: "), f"Expected: Error message, Got: {output}"
        assert exit_code == 1
    finally:
        os.remove('forms.json')
        init_db()