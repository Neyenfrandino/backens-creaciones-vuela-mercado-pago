from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.routers import mercado_pago
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tienda-wep-creaciones-vuela.netlify.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# "http://localhost:3000",

# Incluir las rutas de mercado_pago
app.include_router(mercado_pago.router)

# Manejo explícito de solicitudes OPTIONS
@app.options("/{any_path:path}")
async def handle_options(any_path: str):
    return JSONResponse(status_code=200)    


@app.get("/")
def read_root():
    return {"message": "Bienvenido a mi API"}

@app.head("/")
def read_root_head():
    return {"message": "OK"}

if __name__ == "__main__":
    # Detectar el entorno de ejecución
    is_production = os.getenv("RENDER") is not None  # Render define algunas variables de entorno únicas.
    
    # Obtener el puerto dinámicamente o usar un valor predeterminado para desarrollo local
    port = int(os.getenv("PORT", 8000))
    
    # Configurar el servidor
    uvicorn.run(
        app if is_production else "main:app",
        host="0.0.0.0",
        port=port,
        reload=not is_production  # Habilitar reload solo en desarrollo
    )
