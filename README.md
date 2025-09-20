# PotokIgr API

### Цель: создание бекенда торрент-трекера [potokigr](https://github.com/aero-4/PotokIgr.git)

### Stack: FastAPI/sqlite3/TortoiseORM/Pydantic/logging/PyJWT/OpenSSL

## Запуск:
1. указать переменные из config.py 
  [API_KEY_RAWGIO](https://rawg.io/apidocs), [RECAPTCHA_SECRET](https://cloud.google.com/security/products/recaptcha)
2. `pip install -r requirements.txt`
3. запустить файл `python main.py`

## Выполненное

Роутеры:
1. [x] Поиск
   1. [x] По названию
3. [x] Игры
    1. [x] Выдача по названию slug
    2. [x] Выдача похожих в запросе
    3. [x] Загрузка новой из админки
4. [x] Категории
    1. [x] Выдача по offset, limit
5. [x] Комменты
   1. [x] Создать коммент
   2. [x] Оценки: лайк, дизлайк
6. [x] Авторизация/Регистрация
    1. [x] Создание токенов JWT - access, refresh
    2. [x] Проверка Google капчи v2
    3. [x] Логаут
7. [x] Пользователь
    1. [x] Выдача информации основной  
Дополнительно:
1. [x] Microservice поиск метаданных игр через [RawgIO](https://rawg.io/)
2. [x] Microservice под поиск торентов под каждую игру каждые 12 часов
3. [x] Microservice перевод описаний игр с английского на русский каждые 8 часов
4. [x] Description - для каждой игры нужно искать отдельно каждые 4 часов


