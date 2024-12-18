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

if __name__ == "__main__":
    # Obtener el puerto desde la variable de entorno, con un valor predeterminado para desarrollo local.
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
