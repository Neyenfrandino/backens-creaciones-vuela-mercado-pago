import httpx
from fastapi import HTTPException

def mercadopago_repository(schema: dict, sdk):
    try:
        # Validación del esquema
        if not isinstance(schema, dict):
            raise ValueError("El esquema debe ser un diccionario válido.")

        # Crear preferencia usando el SDK
        response = sdk.preference().create(schema)

        # Validar respuesta de la API
        if response.get("status") in [200, 201]:  # Estados HTTP de éxito
            print("Preferencia creada exitosamente:", response.get("response"))
            return response.get("response")
        else:
            error_message = f"Error al crear preferencia. Código: {response.get('status')}, Detalles: {response.get('response')}"
            print(error_message)
            raise Exception(error_message)

    except ValueError as ve:
        print(f"Error de validación: {ve}")
        raise ve  # Re-lanzar para que el controlador lo maneje si es necesario

    except Exception as e:
        print(f"Error inesperado al crear preferencia: {str(e)}")
        raise e  # Re-lanzar para mantener el contexto del error

# Función para confirmar el pago en MercadoPago
async def confirm_payment(payment_id: str, access_token: str):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    
    # Realizar la solicitud GET a la API de MercadoPago
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
        print(response)
        
        payment_info = response.json()
     
        return payment_info
