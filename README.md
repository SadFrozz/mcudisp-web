# Web Display for MCU-compatible devices (ex. Behringer BCF2000)

Эмулятор внешнего дисплея для MIDI-контроллера Behringer BCF2000 или любого другого устройства (в режиме эмуляции Mackie Control Universal), реализованный в виде веб-сервера. Позволяет использовать любое устройство в локальной сети (планшет, телефон, Raspberry Pi) в качестве полноценного дисплея для вашего контроллера при работе в Cockos Reaper.

![Скриншот дисплея](https://i.yapx.ru/Z865V.png) 

---

## Возможности

* **Дисплей треков**: Отображение двух строк по 56 символов (8 ячеек по 7 символов), получаемых по MIDI SysEx.
* **Таймкод**: Отображение таймкода проекта в формате `ЧЧ:ММ:СС:КК`, получаемого по OSC.
* **Статус транспорта**: Отображение статуса `PLAY` или `STOP`.
* **Индикация записи**: Вся цветовая схема интерфейса меняется с зелёной на красную, когда активна запись.
* **Номера каналов**: Статичные номера каналов для удобной навигации.
* **Адаптивный дизайн**: Интерфейс автоматически масштабируется под экран любого размера и соотношения сторон.

---

## Технологии

* **Бэкенд**: Python
    * **Веб-сервер**: Flask + Flask-SocketIO
    * **MIDI**: `mido`
    * **OSC**: `python-osc`
* **Фронтенд**: HTML, CSS (CSS Grid, vmin), JavaScript (Socket.IO client)

---

## Установка и запуск

#### 1. Подготовка

Убедитесь, что у вас установлен **Python 3**.

#### 2. Клонирование и установка зависимостей

```bash
# Клонируйте репозиторий
git clone https://github.com/SadFrozz/mcudisp-web.git
cd mcudisp-web

# Установите необходимые библиотеки
pip install -r requirements.txt
```

#### 3. Настройка Cockos Reaper

Вам нужно настроить два устройства в Reaper: одно для MIDI, другое для OSC.

**A. Настройка MIDI (для дисплея):**

> **Рекомендация:** Вместо стандартного драйвера Mackie Control от Reaper настоятельно рекомендуется использовать **DrivenByMoss4Reaper**. Это обеспечивает более стабильную, полную и корректную реализацию протокола MCU.
>
> Скачать и ознакомиться с инструкцией по установке можно здесь: **[https://mossgrabers.de/Software/Reaper/Reaper.html](https://mossgrabers.de/Software/Reaper/Reaper.html)**

1.  Перейдите в `Options -> Preferences -> Control/OSC/web`.
2.  Добавьте ваше устройство (например, `Mackie Control Universal или DrivenByMoss`).
3.  В настройках устройства в качестве **MIDI Input\Output** выберите ваш контроллер (например, `BCF2000`).

**Б. Настройка OSC (для таймкода и статуса):**
1.  В том же окне `Control/OSC/web` добавьте новое устройство.
2.  Выберите **Control surface mode:** `OSC (Open Sound Control)`.
3.  Настройте его:
    * **Mode:** `Configure device IP + port`
    * **Host:** `127.0.0.1` (IP-адрес этого же компьютера)
    * **Send to port:** `9000`
4.  Убедитесь, что в файле конфигурации OSC (`Default.ReaperOSC` или его копии) активны строки `FRAMES s/frames/str`, `PLAY t/play` и `RECORD t/record`.

#### 4. Конфигурация MIDI-порта

1.  Запустите скрипт `list_ports.py`, чтобы увидеть список доступных MIDI-устройств:
    ```bash
    python list_ports.py
    ```
2.  Скопируйте точное имя вашего контроллера из списка.
3.  Откройте файл `server.py` в текстовом редакторе.
4.  Найдите строку `SEARCH_TERM = "..."` и вставьте ваше имя порта между кавычками. Сохраните файл.

#### 5. Запуск сервера

В командной строке, находясь в папке проекта, выполните:
```bash
python server.py
```
Сервер запустится и будет готов к приему данных.

#### 6. Доступ к дисплею

Откройте веб-браузер на любом устройстве в вашей локальной сети и перейдите по IP-адресу вашего компьютера, указав порт `5000`. Например: `http://192.168.0.174:5000`.

---

## Структура файлов

```
.
├── server.py         # Основной скрипт сервера (Python)
├── list_ports.py     # Вспомогательный скрипт для поиска MIDI-портов
├── templates/
│   └── index.html    # Файл веб-интерфейса
├── requirements.txt  # Список зависимостей Python
└── Readme.md         # Этот файл
```
