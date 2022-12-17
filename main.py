from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return 'Home'

@app.get('/about')
def about():
    return 'About'