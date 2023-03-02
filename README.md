**warning! the project is not finished yet!**

# news_service
Another very cool simple project developed during the Rosatom Labs. REST API, which is a service for generating and managing news


<!-- TOC -->
* [news_service](#newsservice)
  * [How to configure](#how-to-configure)
  * [How to run](#how-to-run)
<!-- TOC -->

<p align="center">
    <img src="https://www.pngplay.com/wp-content/uploads/7/Newspaper-Background-PNG.png" />
</p>

## How to configure
The application is configured using the following environment variables:

| Variable name | Description                                                             | Value Example                                                                   |
|---------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| `DB_HOST`     | database hostname in docker network                                     | recommend `db`                                                                  |
| `DB_PORT`     | database port in docker network                                         | recommend `5432`                                                                |
| `DB_NAME`     | database name                                                           | any reasonable                                                                  |
| `DB_USER`     | database user name                                                      | like `postgres`                                                                 |
| `DB_PSWD`     | database user password                                                  | not like `qwerty1234`                                                           |
| `APP_PORT`    | application port in docker network and localhost                        | like `8080`                                                                     |
| `APP_HOST`    | application host in docker network                                      | recommend `0.0.0.0`                                                             | 
| `SECRET_K`    | secret key of your app. will be used as a token generator in the future | copy from `python -c "import secrets; print(secrets.token_hex(16))"`  and paste |

You can define all this environment variables or use .env file. dotenv file example is already in `/.env.example`. You can just edit and rename it. 

## How to run
The entire project, along with the database, runs in docker containers. so before starting, make sure you [install](https://docs.docker.com/engine/install/) it.
Now you can enter these commands to run project
```commandline
git clone https://github.com/saladware/news_service.git
cd news_service
docker-compose up -d
```
After up the project you need to run the migrations to create the database tables
```commandline
docker-compose exec app alembic upgrade head
```
To create admin user use this
```commandline
docker-compose exec app python -m app.create_admin
```

## Features


### Users
* [x] создание пользователя
* [x] авторизация и аутентификация
* [x] получение, изменение и удаление текущего пользователя
* [x] смена пароля
* [x] получения пользователя по id (без его новостей и комментариев)
* [x] удаление, редактирование, пользователя по id (может только сам пользователь или админ)

### News
* [x] создание новости сразу привязывая пользователя
* [x] удаление и изменение новости (может только автор или админ)
* [x] получение новости по id
* [ ] поиск новости по тегу, автору, дате создания
* [x] добавление и удаление тегов

### Comments
* [ ] создание комментария сразу привязывая пользователя и новость 
* [ ] редактирование, удаление комментария (может автор или админ)
* [ ] получение всех новостей пользователя
* [ ] получение всех комментариев пользователя
* [ ] получение комментария по id

### Other
* [x] admin creator cli tool `app/create_admin.py`
