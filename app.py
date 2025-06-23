import sys
import re
from datetime import datetime
from tinydb import TinyDB
import os

def is_date(string):
    try:
        datetime.strptime(string, "%d.%m.%Y")
        return True
    except ValueError:
        try:
            datetime.strptime(string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

def is_phone(string):
    pattern = r"^\+7\s+\d{3}\s+\d{3}\s+\d{2}\s+\d{2}$"
    return bool(re.match(pattern, string))

def is_email(string):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, string))

def get_field_type(value):
    if is_date(value):
        return "date"
    elif is_phone(value):
        return "phone"
    elif is_email(value):
        return "email"
    return "text"

def process_template(args):
    try:
        if not os.path.exists('forms.json'):
            raise FileNotFoundError("Database file 'forms.json' not found")
        db = TinyDB('forms.json')
        if len(args) < 2:
            return "Usage: app.py get_tpl --field1=value1 --field2=value2", 1

        command = args[1]
        if command != 'get_tpl':
            return "Unknown command", 1

        if len(args) < 3:
            return "Usage: app.py get_tpl --field1=value1 --field2=value2", 1

        fields = {}
        for arg in args[2:]:
            if not arg.startswith('--'):
                return f"Invalid argument: {arg}", 1
            parts = arg[2:].split('=', 1)
            if len(parts) != 2:
                return f"Invalid argument: {parts[0]}", 1
            key, value = parts
            fields[key] = value

        templates = db.all()
        for template in templates:
            if not template.get('name'):
                continue
            match = True
            template_fields = {k: v for k, v in template.items() if k != 'name'}
            for key, typ in template_fields.items():
                if key not in fields:
                    match = False
                    break
                value = fields[key]
                if typ == 'date' and not is_date(value):
                    match = False
                    break
                elif typ == 'phone' and not is_phone(value):
                    match = False
                    break
                elif typ == 'email' and not is_email(value):
                    match = False
                    break
                elif typ == 'text':
                    pass
            if match:
                return template['name'], 0

        result = {key: get_field_type(value) for key, value in fields.items()}
        output = ['{']
        items = list(result.items())
        for i, (k, v) in enumerate(items):
            output.append(f'  "{k}": "{v}"')
            if i < len(items) - 1:
                output[-1] += ','
        output.append('}')
        return '\n'.join(output), 0
    except FileNotFoundError:
        return "Error: Database file 'forms.json' not found", 1
    except Exception as e:
        return f"Error: {str(e)}", 1

if __name__ == '__main__':
    output, exit_code = process_template(sys.argv)
    print(output)
    sys.exit(exit_code)