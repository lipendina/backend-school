sudo systemctl stop yandex-task.service
python tests/database_tests.py
python tests/helper_tests.py
python tests/main_tests.py
sudo systemctl start yandex-task.service

