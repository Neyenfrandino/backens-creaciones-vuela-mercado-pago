import httpx
from fastapi import HTTPException

def mercadopago_repository(schema, sdk):
    try:
        # # Validación del esquema
        # if not isinstance(schema, sdk):
        #     raise ValueError("El esquema debe ser un diccionario válido.")

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
async def confirm_payment(payment_id, access_token: str):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    
    # try:
    #     # Realizar la solicitud GET a la API de MercadoPago
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
        
    #     # Verificar si la respuesta fue exitosa
    #     if response.status_code == 200:
    #         payment_info = response.json()
    #         print("Información del pago:", payment_info)
    #         return payment_info
    #     else:
    #         # Si la respuesta no fue exitosa, lanzar un error
    #         error_message = f"Error al confirmar el pago. Código: {response.status_code}, Detalles: {response.text}"
    #         print(error_message)
    #         raise HTTPException(status_code=response.status_code, detail=error_message)

    # except httpx.RequestError as req_error:
    #     error_message = f"Error al realizar la solicitud HTTP: {str(req_error)}"
    #     print(error_message)
    #     raise HTTPException(status_code=500, detail=error_message)

    # except Exception as e:
    #     error_message = f"Error inesperado al confirmar el pago: {str(e)}"
    #     print(error_message)
    #     raise HTTPException(status_code=500, detail=error_message)
