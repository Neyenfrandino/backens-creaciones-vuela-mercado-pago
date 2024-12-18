from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.routers import mercado_pago

app = FastAPI()

# Configuración de CORS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://tienda-wep-creaciones-vuela.netlify.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


# Incluir las rutas de mercado_pago
app.include_router(mercado_pago.router)

# Manejo explícito de solicitudes OPTIONS
@app.options("/{any_path:path}")
async def handle_options(any_path: str):
    return JSONResponse(status_code=200)

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
