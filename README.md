
# Focave

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

*Your personal focus cave*

Focave is free and open source, self hosted planner for or your needs

## Badges

<!-- prettier-ignore -->
| `main` | `dev` |
| ------ | ----- |
| [![Backend format and lint](https://github.com/focave/webapp/actions/workflows/backend_format_and_lint.yml/badge.svg?branch=main&event=push)](https://github.com/focave/webapp/actions/workflows/backend_format_and_lint.yml) | [![Backend format and lint](https://github.com/focave/webapp/actions/workflows/backend_format_and_lint.yml/badge.svg?branch=dev&event=push)](https://github.com/focave/webapp/actions/workflows/backend_format_and_lint.yml)|
| [![Frontend Format and lint](https://github.com/focave/webapp/actions/workflows/frontend_format_and_lint.yml/badge.svg?branch=main&event=push)](https://github.com/focave/webapp/actions/workflows/frontend_format_and_lint.yml) | [![Frontend format and lint](https://github.com/focave/webapp/actions/workflows/frontend_format_and_lint.yml/badge.svg?branch=dev&event=push)](https://github.com/focave/webapp/actions/workflows/frontend_format_and_lint.yml) |
| [![Django tests](https://github.com/focave/webapp/actions/workflows/django.yml/badge.svg?branch=main&event=push)](https://github.com/focave/webapp/actions/workflows/django.yml) | [![Django tests](https://github.com/focave/webapp/actions/workflows/django.yml/badge.svg?branch=dev&event=push)](https://github.com/focave/webapp/actions/workflows/django.yml) |


## Installation


Clone the project
```bash
  git clone https://github.com/focave/webapp
```

Go to the project directory
```bash
  cd focave
```

Build docker compose
```bash
  docker compose build
```

You need to apply migrations for the database to be initialized
```bash
docker compose run backend python manage.py makemigrations
docker compose run backend python manage.py migrate
```

And create super user
```bash
docker compose run backend python manage.py createsuperuser
```

Then start docker compose
```bash
  docker compose up
```

And frontend should be accessible on `127.0.0.1:3000` and backend on `127.0.0.1:8000`

## Features

*Note: At this point the are no features and the app does basically nothing, as time goes on, features will be added to this list*
## Feedback

If you have any feedback, please open an issue


## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)


