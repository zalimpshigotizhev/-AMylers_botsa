# AMylers
Этнический дейтинг-бот с возможностью авторизации. Можно отправлять симпатию в виде яблоко. При взаимной симпатии их странички высвечиваются друг другу, и лишь тогда появляется возможность общения.

# Стек
<img src="https://capsule-render.vercel.app/api?type=venom&height=200&color=gradient&text=AMylers&fontColor=082567&fontAlign=50&section=header&animation=fadeIn&stroke=FBCEB1"/>
<div>
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" />
<div/>

  
# .env
Не забудьте заполнить переменные окружения. 

```
TOKEN=""
REDIS_NAME=""
REDIS_PASSWORD=""
REDIS_HOST=""
REDIS_PORT=6379

POSTGRES_NAME=""
POSTGRES_USER=""
POSTGRES_PASSWORD=123456789
POSTGRES_HOST=""
POSTGRES_PORT=5432
PASSWORD_FOR_ADMIN=""

```
# Первый запуск

1) Все переменные окружение должны быть заполнены. Движок докера должен быть активным. Интерпретатор Python 3.10. Для удобства используйте Make [Как установить?](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows).
2) `make containers` - создать все контейнеры Docker Compose.
3) Миграции сделаются сами в `entrypoint.sh`. Там же пристутствует `python bot.py` который запускает бота aiogram.

# Ревью приветствуется! С широко открытым объятием.
