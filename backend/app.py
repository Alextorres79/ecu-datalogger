import json
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Archivos JSON para almacenar configuraciones
DEFAULT_SETTINGS_FILE = 'car_Default_Settings.json'
CURRENT_SETTINGS_FILE = 'car_Current_Settings.json'

def load_settings(file_path):
    """Cargar configuraciones desde un archivo JSON."""
    if not os.path.exists(file_path):
        return []  # Si no existe, retornar una lista vacía
    with open(file_path, 'r') as file:
        return json.load(file)

def save_settings(file_path, settings):
    """Guardar configuraciones en un archivo JSON."""
    with open(file_path, 'w') as file:
        json.dump(settings, file, indent=4)

# Crear los archivos si no existen con valores predeterminados
if not os.path.exists(DEFAULT_SETTINGS_FILE):
    save_settings(DEFAULT_SETTINGS_FILE, [
        {"Setting": "Volume", "Value": "50"},
        {"Setting": "Brightness", "Value": "70"},
        {"Setting": "Language", "Value": "English"}
    ])

if not os.path.exists(CURRENT_SETTINGS_FILE):
    save_settings(CURRENT_SETTINGS_FILE, [
        {"id": uuid.uuid4().hex, "Setting": "Volume", "Value": "50"},
        {"id": uuid.uuid4().hex, "Setting": "Brightness", "Value": "70"},
        {"id": uuid.uuid4().hex, "Setting": "Language", "Value": "English"}
    ])

@app.route('/landing', methods=['GET', 'POST'])
def all_settings():
    """Obtener o añadir configuraciones."""
    response_object = {'status': 'success'}
    current_settings = load_settings(CURRENT_SETTINGS_FILE)

    if request.method == 'POST':
        post_data = request.get_json()
        new_setting = {
            'id': uuid.uuid4().hex,
            'Setting': post_data.get('Setting'),
            'Value': post_data.get('Value')
        }
        current_settings.append(new_setting)
        save_settings(CURRENT_SETTINGS_FILE, current_settings)
        response_object['message'] = 'Setting added successfully'
    else:
        response_object['settings'] = current_settings

    return jsonify(response_object)

@app.route('/landing/<setting_id>', methods=['PUT'])
def update_setting(setting_id):
    """Actualizar un valor específico."""
    response_object = {'status': 'success'}
    current_settings = load_settings(CURRENT_SETTINGS_FILE)
    put_data = request.get_json()

    for setting in current_settings:
        if setting['id'] == setting_id:
            setting['Value'] = put_data.get('Value')
            save_settings(CURRENT_SETTINGS_FILE, current_settings)
            response_object['message'] = 'Setting updated successfully'
            break
    else:
        response_object['message'] = 'Setting not found'

    return jsonify(response_object)

@app.route('/landing/<setting_id>/reset', methods=['PUT'])
def reset_setting(setting_id):
    """Restablecer un valor específico al predeterminado."""
    response_object = {'status': 'success'}
    current_settings = load_settings(CURRENT_SETTINGS_FILE)
    default_settings = load_settings(DEFAULT_SETTINGS_FILE)

    for setting in current_settings:
        if setting['id'] == setting_id:
            for default in default_settings:
                if setting['Setting'] == default['Setting']:
                    setting['Value'] = default['Value']
                    save_settings(CURRENT_SETTINGS_FILE, current_settings)
                    response_object['message'] = 'Setting reset to default'
                    break
            else:
                response_object['message'] = 'Default setting not found'
            break
    else:
        response_object['message'] = 'Setting not found'

    return jsonify(response_object)

@app.route('/landing/reset', methods=['PUT'])
def reset_all_settings():
    """Restablecer todos los valores al predeterminado."""
    response_object = {'status': 'success'}
    default_settings = load_settings(DEFAULT_SETTINGS_FILE)

    current_settings = [
        {
            'id': uuid.uuid4().hex,
            'Setting': default['Setting'],
            'Value': default['Value']
        } for default in default_settings
    ]
    save_settings(CURRENT_SETTINGS_FILE, current_settings)
    response_object['message'] = 'All settings reset to default'
    return jsonify(response_object)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
