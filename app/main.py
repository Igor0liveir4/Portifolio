from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Portfólio API",
    description="API e Website do meu Portfólio Profissional",
    version="1.0.0"
)

# Monta a pasta de arquivos estáticos (CSS, JS, Imagens)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura o Jinja2 para renderizar os HTMLs
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"status": "API do Portfólio no ar!"}