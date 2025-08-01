# Web Display for MCU-compatible devices

A web-based display emulator for MCU-compatible MIDI controllers like the Behringer BCF2000.

---

## Language / Язык

* [**Информация на русском**](#%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F-%D0%BD%D0%B0-%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%BC)
* [**Information in English**](#information-in-english)

---
---

## Информация на русском

# Веб-дисплей для MCU-совместимых устройств (например Behringer BCF2000)

Эмулятор внешнего дисплея для MIDI-контроллера Behringer BCF2000 или любого другого устройства (в режиме эмуляции Mackie Control Universal), реализованный в виде веб-сервера. Позволяет использовать любое устройство в локальной сети (планшет, телефон, Raspberry Pi) в качестве полноценного дисплея для вашего контроллера при работе в Cockos Reaper.

![Скриншот дисплея](https://lostpix.com/img/2025-08/02/0wbryozfadli58c3hrxtq231z.jpg) 

### Возможности

* **Дисплей треков**: Отображение двух строк по 56 символов (8 ячеек по 7 символов), получаемых по MIDI SysEx.
* **Таймкод**: Отображение таймкода проекта в формате `ЧЧ:ММ:СС:КК`, получаемого по OSC.
* **Статус транспорта**: Отображение статуса `PLAY` или `STOP`.
* **Индикация записи**: Вся цветовая схема интерфейса меняется с зелёной на красную, когда активна запись.
* **Номера каналов**: Статичные номера каналов для удобной навигации.
* **Адаптивный дизайн**: Интерфейс автоматически масштабируется под экран любого размера и соотношения сторон.

### Технологии

* **Бэкенд**: Python
    * **Веб-сервер**: Flask + Flask-SocketIO
    * **MIDI**: `mido`
    * **OSC**: `python-osc`
* **Фронтенд**: HTML, CSS (CSS Grid, vmin), JavaScript (Socket.IO client)

### Установка и запуск

#### 1. Подготовка

Убедитесь, что у вас установлен **Python 3**.

#### 2. Клонирование и установка зависимостей

```bash
# Клонируйте репозиторий
git clone [https://github.com/SadFrozz/mcudisp-web.git](https://github.com/SadFrozz/mcudisp-web.git)
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

### Структура файлов

```
.
├── server.py         # Основной скрипт сервера (Python)
├── list_ports.py     # Вспомогательный скрипт для поиска MIDI-портов
├── templates/
│   └── index.html    # Файл веб-интерфейса
├── requirements.txt  # Список зависимостей Python
└── Readme.md         # Этот файл
```

---
---

## Information in English

# Web Display for MCU-compatible devices (like Behringer BCF2000)

An external display emulator for the Behringer BCF2000 MIDI controller or any other device (in Mackie Control Universal emulation mode), implemented as a web server. It allows you to use any device on your local network (tablet, phone, Raspberry Pi) as a full-featured display for your controller when working with Cockos Reaper.

![Display Screenshot](https://lostpix.com/img/2025-08/02/0wbryozfadli58c3hrxtq231z.jpg)

### Features

* **Track Display**: Renders two lines of 56 characters each (8 cells x 7 characters), received via MIDI SysEx.
* **Timecode**: Displays the project timecode in `HH:MM:SS:FF` format, received via OSC.
* **Transport Status**: Shows the current transport status (`PLAY` or `STOP`).
* **Recording Indication**: The entire UI color scheme changes from green to red when recording is active.
* **Channel Numbers**: Static channel numbers are displayed for easy navigation.
* **Responsive Design**: The interface automatically scales to fit any screen size and aspect ratio.

### Technology

* **Backend**: Python
    * **Web Server**: Flask + Flask-SocketIO
    * **MIDI**: `mido`
    * **OSC**: `python-osc`
* **Frontend**: HTML, CSS (CSS Grid, vmin), JavaScript (Socket.IO client)

### Installation and Usage

#### 1. Prerequisites

Make sure you have **Python 3** installed.

#### 2. Clone and Install Dependencies

```bash
# Clone the repository
git clone [https://github.com/SadFrozz/mcudisp-web.git](https://github.com/SadFrozz/mcudisp-web.git)
cd mcudisp-web

# Install the required libraries
pip install -r requirements.txt
```

#### 3. Cockos Reaper Setup

You need to configure two devices in Reaper: one for MIDI and another for OSC.

**A. MIDI Setup (for the display):**

> **Recommendation:** Instead of Reaper's standard Mackie Control driver, it is highly recommended to use **DrivenByMoss4Reaper**. It provides a more stable, complete, and correct implementation of the MCU protocol.
>
> You can download it and find installation instructions here: **[https://mossgrabers.de/Software/Reaper/Reaper.html](https://mossgrabers.de/Software/Reaper/Reaper.html)**

1.  Go to `Options -> Preferences -> Control/OSC/web`.
2.  Add your device (e.g., `Mackie Control Universal` or `DrivenByMoss`).
3.  In the device settings, select your controller (e.g., `BCF2000`) as the **MIDI Input/Output**.

**B. OSC Setup (for timecode and status):**
1.  In the same `Control/OSC/web` window, add another device.
2.  Select **Control surface mode:** `OSC (Open Sound Control)`.
3.  Configure it as follows:
    * **Mode:** `Configure device IP + port`
    * **Host:** `127.0.0.1` (IP address of the same computer)
    * **Send to port:** `9000`
4.  Ensure that in your OSC configuration file (`Default.ReaperOSC` or a copy), the following lines are active: `FRAMES s/frames/str`, `PLAY t/play`, and `RECORD t/record`.

#### 4. MIDI Port Configuration

1.  Run the `list_ports.py` script to see a list of available MIDI devices:
    ```bash
    python list_ports.py
    ```
2.  Copy the exact name of your controller from the list.
3.  Open the `server.py` file in a text editor.
4.  Find the line `SEARCH_TERM = "..."` and paste your port name between the quotes. Save the file.

#### 5. Run the Server

In your command line, from the project folder, run:
```bash
python server.py
```
The server will start and be ready to receive data.

#### 6. Access the Display

Open a web browser on any device on your local network and navigate to the IP address of your computer, using port `5000`. For example: `http://192.168.0.174:5000`.

### File Structure

```
.
├── server.py         # Main server script (Python)
├── list_ports.py     # Helper script to find MIDI ports
├── templates/
│   └── index.html    # Web interface file
├── requirements.txt  # Python dependency list
└── Readme.md         # This file
