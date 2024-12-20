from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.routers import mercado_pago
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tienda-wep-creaciones-vuela.netlify.app"],  # Cambiar según sea necesario
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Incluir las rutas de Mercado Pago
app.include_router(mercado_pago.router)

# Manejo explícito de solicitudes OPTIONS
@app.options("/{any_path:path}")
async def handle_options(any_path: str):
    return JSONResponse(status_code=200)

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a mi API"}

# Ruta para solicitudes HEAD
@app.head("/")
def read_root_head():
    return {"message": "OK"}

if __name__ == "__main__":
    # Detectar el entorno de ejecución
    is_production = os.getenv("RENDER") == "true"  # Variable de entorno para distinguir producción
    port = int(os.getenv("PORT", 8000))  # Usar el puerto definido en las variables de entorno o el predeterminado

    print(f"Ejecutando en entorno {'producción' if is_production else 'desarrollo'}")
    # Configurar y ejecutar Uvicorn
    uvicorn.run(
        app if is_production else "main:app",  # En producción se usa el objeto app directamente
        host="0.0.0.0",  # Escuchar en todas las interfaces
        port=port,  # Puerto dinámico o por defecto
        reload=not is_production  # Activar recarga automática solo en desarrollo
    )
