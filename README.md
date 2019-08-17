# REST API сервис
REST API сервис, который сохраняет переданные ему наборы данных (выгрузки от поставщика) c жителями, позволяет их просматривать, редактировать информацию об отдельных жителях, а также производить анализ возрастов жителей по городам и анализировать спрос на подарки в разных месяцах для указанного набора данных

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
