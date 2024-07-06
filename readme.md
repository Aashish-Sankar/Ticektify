
# Installation

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
"# Ticektify" 