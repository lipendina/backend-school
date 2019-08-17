# REST API сервис
REST API сервис, который сохраняет переданные ему наборы данных (выгрузки от поставщика) c жителями, позволяет их просматривать, редактировать информацию об отдельных жителях, а также производить анализ возрастов жителей по городам и анализировать спрос на подарки в разных месяцах для указанного набора данных

# Формат присылаемых данных
| Поле | Тип | Значение | 
| :--- | :--- | --- |  
| citizen_id | целое число | Уникальный идентификатор жителя, неотрицательное число. | 
| town | строка | Название города. Непустая строка, содержащая хотя бы 1 букву или цифру | 
| street | строка | Название улицы. Непустая строка, содержащая хотя бы 1 букву или цифру. |
| building  | строка | Номер дома, корпус и строение. Непустая строка, содержащая хотя бы 1 букву или цифру. | 
| apartment | целое число | Номер квартиры, неотрицательное число. |
| name | строка | Непустая строка. |
| birth_date | строка | Дата рождения в формате ДД.ММ.ГГГГ (UTC) |
| gender | строка | Значения `male` , `female` . |
| relatives | список из целых чисел | Ближайшие родственники, уникальные значения существующих `citizen_id` жителей из этой же выгрузки.|

# Установка
Склонируйте репозиторий, создайте виртуальное окружение и установите необходимые библиотеки.
```bash
$ git clone https://github.com/lipendina/backend-school.git
$ python3 -m venv yandex
$ . yandex/bin/activate
(yandex) $ pip install -r pip-req.txt
```

# Запуск
Запустите `main.py`, он запустит сервер.
```bash
(yandex) $ python main.py
```

# Тестирование
Для тестирования запустите `test.sh`.
```bash
(yandex) $ ./test.sh
```
Если не хватает прав, разрешите запуск тестирующему скрипту:
```bash
(yandex) $ chmod +x ./test.sh
```

# Настройка автозагрузки
Для того, чтобы после перезагрузки, сервер запускался сам, необходимо создать сервис.
Необходимо создать по пути `/etc/systemd/system/` файл `NAME.service` (NAME меняем на название вашего сервиса).
```bash
[Unit]
Description=Yandex task for backend school
After=multi-user.target

[Service]
Type=idle
ExecStart=/path/to/env/python /path/to/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Где `path/to/env` - путь до виртуального окружения Python, `path/to/main.py` - путь до файла `main.py`.

Для запуска сервиса выполните следующие команды:
```bash
sudo systemctl daemon-reload
sudo systemctl enable yourservice.service
sudo systemctl start yourservice.service
```

# Обработчики REST API
### POST /imports
Принимает на вход набор с данными о жителях в формате `json` и сохраняет его с
уникальным идентификатором `import_id`. В наборе данных для каждого жителя должны присутствовать все поля.
### PATCH /imports/$import_id/citizens/$citizen_id
Изменяет информацию о жителе в указанном наборе данных. На вход подается JSON в котором можно указать любые данные о жителе, кроме `citizen_id`. В запросе должно быть указано хотя бы одно поле, значения не могут быть `null`.
### GET /imports/$import_id/citizens
Возвращает список всех жителей для указанного набора данных.
### GET /imports/$import_id/citizens/birthdays
Возвращает жителей и количество подарков, которые они будут покупать своим ближайшим родственникам (1-го порядка), сгруппированных по месяцам из указанного набора данных.
### GET /imports/$import_id/towns/stat/percentile/age
Возвращает статистику по городам для указанного набора данных в разрезе возраста (полных лет) жителей: 50-тый, 75-тый и 99-тый перцентили.