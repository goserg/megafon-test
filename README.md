Инструкция по запуску:

1. Клонировать репозиторий

git clone https://github.com/goserg/megafon-test.git

2. Перейти в папку с проектом

cd megafon-test

3. Убедиться, что установлен Python 3 и Django.
Для функционального тестировния необходим Selenium.
Установить необходимые зависимости при помощи команд:

pip install pipenv
pipenv install
pipenv shell

4. Запуск Dev сервера:

python manage.py runserver


5. Запуск тестов:

python manage.py test
для запуска функционального тестирования должен быть установлен браузер Chrome 88
