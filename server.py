import mido
import threading
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

# --- Конфигурация ---
SEARCH_TERM = 'BCF2000'
BEHRINGER_SYSEX_ID = (0, 32, 50, 0, 20, 120)
HOST_IP = '0.0.0.0'
OSC_IP = "127.0.0.1"
OSC_PORT = 9000
WEB_PORT = 5000

# --- Инициализация ---
app = Flask(__name__)
socketio = SocketIO(app)

# Глобальные переменные для хранения состояния и названий функций
play_state = False
record_state = False
function_names = []
functions_available = False # Флаг, который показывает, найден ли файл func.txt

@app.route('/')
def index():
    return render_template('index.html')

def load_function_names():
    """Читает названия функций из файла func.txt и устанавливает флаг доступности."""
    global function_names, functions_available
    try:
        with open('func.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            function_names = lines[:8] # Берем только первые 8 строк
        while len(function_names) < 8:
            function_names.append("---")
        functions_available = True # Файл найден и прочитан
        print(f"✅ Функции F1-F8 успешно загружены: {function_names}")
    except FileNotFoundError:
        print("⚠️ Файл func.txt не найден. Секция F-клавиш будет скрыта.")
        function_names = []
        functions_available = False # Файл не найден
    except Exception as e:
        print(f"❌ Ошибка при чтении файла func.txt: {e}")
        function_names = []
        functions_available = False # Произошла ошибка

@socketio.on('connect')
def handle_connect():
    """Отправляет начальные данные (названия функций и флаг) новому клиенту."""
    print("🔌 Клиент подключился. Отправка данных о функциях.")
    # Отправляем и названия, и флаг, нужно ли их показывать
    socketio.emit('update_function_names', {'names': function_names, 'available': functions_available})

# --- Логика OSC ---
def osc_handler(address, *args):
    """Универсальный обработчик OSC, который распределяет сообщения."""
    global play_state, record_state
    if address == "/frames/str":
        if args: socketio.emit('update_timecode', {'timecode': args[0]})
    elif address == "/play":
        play_state = bool(args[0]); update_transport_status()
    elif address == "/record":
        record_state = bool(args[0]); socketio.emit('update_record_status', {'is_recording': record_state}); update_transport_status()

def update_transport_status():
    status_text = "■ STOP"
    if play_state: status_text = "▶ PLAY"
    socketio.emit('update_playback_status', {'status_text': status_text})

def start_osc_server():
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(osc_handler)
    server = BlockingOSCUDPServer((OSC_IP, OSC_PORT), dispatcher)
    print(f"🎧 OSC-сервер слушает на {OSC_IP}:{OSC_PORT}")
    server.serve_forever()

# --- Логика MIDI ---
def find_and_listen_midi():
    target_port_name = None; display_data = { 'line1': ' ' * 56, 'line2': ' ' * 56 }
    while True:
        if not target_port_name:
            try:
                available_ports = mido.get_input_names()
                for port in available_ports:
                    if SEARCH_TERM in port:
                        target_port_name = port; print(f"✅ MIDI-порт найден: '{target_port_name}'"); break
            except Exception as e: print(f"Ошибка поиска: {e}")
            if not target_port_name: time.sleep(5); continue
        try:
            with mido.open_input(target_port_name) as inport:
                print(f"🎧 MIDI-слушатель запущен на порту: '{target_port_name}'")
                for msg in inport:
                    if msg.type == 'sysex':
                        data = msg.data
                        if tuple(data[0:len(BEHRINGER_SYSEX_ID)]) == BEHRINGER_SYSEX_ID:
                            offset = data[len(BEHRINGER_SYSEX_ID)]; text_data = ''.join(map(chr, data[len(BEHRINGER_SYSEX_ID)+1:]))
                            if offset < 56:
                                current = list(display_data['line1']);
                                for i, char in enumerate(text_data):
                                    if offset + i < len(current): current[offset + i] = char
                                display_data['line1'] = "".join(current)
                            else:
                                offset -= 56; current = list(display_data['line2']);
                                for i, char in enumerate(text_data):
                                    if offset + i < len(current): current[offset + i] = char
                                display_data['line2'] = "".join(current)
                            socketio.emit('update_display', {'line1': display_data['line1'], 'line2': display_data['line2']})
        except (IOError, OSError) as e:
            print(f"🔌 MIDI-порт '{target_port_name}' был отключен. Ошибка: {e}"); target_port_name = None; time.sleep(2)

if __name__ == '__main__':
    load_function_names() # Загружаем названия функций при старте
    midi_thread = threading.Thread(target=find_and_listen_midi); midi_thread.daemon = True; midi_thread.start()
    osc_thread = threading.Thread(target=start_osc_server); osc_thread.daemon = True; osc_thread.start()
    print(f"🚀 Веб-сервер запущен на http://{HOST_IP}:{WEB_PORT}")
    socketio.run(app, host=HOST_IP, port=WEB_PORT, allow_unsafe_werkzeug=True)

