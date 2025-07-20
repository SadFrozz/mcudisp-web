import mido

print("---------------------------------------")
print("Доступные MIDI порты для входа:")
print("---------------------------------------")

try:
    input_ports = mido.get_input_names()
    if not input_ports:
        print("Не найдено ни одного MIDI порта.")
    else:
        for port in input_ports:
            print(f"'{port}'")
    print("\nСкопируйте нужное имя порта ВМЕСТЕ С КАВЫЧКАМИ.")
except Exception as e:
    print(f"Произошла ошибка при поиске портов: {e}")

print("---------------------------------------")