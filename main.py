from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os  # Para leer la variable de entorno

from app.routers import mercado_pago

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://tienda-web-creaciones-vuela.netlify.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.include_router(mercado_pago.router)

if __name__ == "__main__":
    # Usar el puerto proporcionado por el entorno, o 8000 si no está configurado
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run('main:app', host="0.0.0.0", port=port, reload=True)
