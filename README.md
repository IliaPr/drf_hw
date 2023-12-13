# DRF With Docker

## Запуск приложения с использованием Docker Compose

1. Установите Docker и Docker Compose, если еще не установлены.

2. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/IliaPr/drf_hw.git
    ```

3. Создайте файл `.env` и укажите необходимые переменные окружения (если еще не создан):

    ```plaintext
    DB_NAME='ваша_база_данных'
    DB_USER='ваш_пользователь'
    DB_PASSWORD='ваш_пароль'
    ```

4. Запустите Docker Compose:

    ```bash
    docker-compose up --build
    ```

5. Откройте браузер и перейдите по адресу [http://localhost:8000](http://localhost:8000) для доступа к приложению.

6. Вы можете также отслеживать логи Celery, перейдя по адресу [http://localhost:8000/logs](http://localhost:8000/logs).

7. Для остановки приложения используйте:

    ```bash
    docker-compose down
    ```

Убедитесь, что у вас установлены все необходимые зависимости и переменные окружения правильно настроены.
