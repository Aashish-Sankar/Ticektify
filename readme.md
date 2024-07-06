# Ticketify Installation

## Backend

```bash
  cd backend
  pip install flask
  pip install -U Flask-SQLAlchemy
  curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
  sudo apt-get update
  sudo apt-get install redis
  pip install flask-Redis-celery
  pip install flask-jwt-extended

```

## Frontend

```bash
  cd Frontend
  npm install  #it will reinstall all the dependencies listed in the package.json
  npm run serve
```

## Redis and Celeruy

```bash
  cd server
  redis-server
  celery -A jobs worker --loglevel=info
  celery -A jobs beat --loglevel=info

  // for manually running the jobs:

  celery -A jobs call jobs.send_daily_emails
  celery -A jobs call jobs.monthly_mail_sender

```

