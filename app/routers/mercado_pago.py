from fastapi import APIRouter, Depends
import mercadopago
import os
from dotenv import load_dotenv

from app.repository.mercado_pago_repo import mercadopago_repository, confirm_payment
from app.schema import DataPreference

router = APIRouter(prefix="/mercadopago", tags=["MercadoPago"])

load_dotenv()
# Verificar el valor de la variable de entorno
access_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')

if not access_token:
    raise ValueError("El token de acceso de Mercado Pago no está definido.")

print("Access token cargado correctamente.")

sdk = mercadopago.SDK(access_token)

print(sdk, 'sdk')

def get_mercadopago_sdk():
    if sdk is None:
        raise ValueError("Mercado Pago SDK no está inicializado correctamente.")
    return sdk

@router.post("/create_preference")
def create_preference(schema: DataPreference, sdk: mercadopago.SDK = Depends(get_mercadopago_sdk)):
    try:
        # Llamada al repositorio para crear la preferencia
        response = mercadopago_repository(schema.dict(), sdk)
        return response
    except Exception as e:
        return {"error": str(e)}
    print(schema, 'schema')

@router.get("/verify_payment/{payment_id}")
async def verify_payment(payment_id):
    payment_info = await confirm_payment(payment_id, access_token)
    
    # Puedes realizar lógica adicional con la información del pago
    if payment_info["status"] == "approved":
        return {"status": "approved", "payment_info": payment_info}
    else:
        return {"status": "not approved", "payment_info": payment_info}