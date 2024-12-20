import httpx
from fastapi import HTTPException
from typing import Dict, Any

# Constante para la URL base de la API de MercadoPago
MP_API_BASE_URL = "https://api.mercadopago.com/v1"

def mercadopago_repository(schema: Dict, sdk) -> Dict:
    """
    Crea una preferencia de pago en MercadoPago.

    Args:
        schema (Dict): Datos necesarios para la creación de la preferencia.
        sdk: SDK de MercadoPago.

    Returns:
        Dict: Respuesta de la creación de la preferencia.

    Raises:
        HTTPException: Si ocurre un error durante la creación.
    """
    try:
        # Crear preferencia usando el SDK
        response = sdk.preference().create(schema)

        # Verificar si la respuesta fue exitosa
        if response.status_code in [200, 201]:  # Estados HTTP de éxito
            preference_data = response.get("response")
            if preference_data:
                print("Preferencia creada exitosamente:", preference_data)
                return preference_data
            else:
                raise HTTPException(status_code=400, detail="No se obtuvo respuesta de la preferencia")
        else:
            error_details = response.get("response", {}).get("message", "Sin detalles")
            error_message = f"Error al crear preferencia. Código: {response.status_code}, Detalles: {error_details}"
            print(error_message)
            raise HTTPException(status_code=400, detail=error_message)

    except ValueError as ve:
        print(f"Error de validación: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        print(f"Error inesperado al crear preferencia: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al procesar la preferencia")


async def confirm_payment(payment_id: str, access_token: str) -> Any:
    """
    Confirma el estado de un pago en MercadoPago.

    Args:
        payment_id (str): ID del pago a confirmar.
        access_token (str): Token de acceso para autenticar la solicitud.

    Returns:
        Any: Información del pago.

    Raises:
        HTTPException: Si ocurre un error durante la confirmación.
    """
    if not payment_id or payment_id == "":
        raise HTTPException(status_code=400, detail="El ID del pago no puede estar vacío.")

    url = f"{MP_API_BASE_URL}/payments/{payment_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
        
        if response.status_code == 200:
            try:
                payment_info = response.json()
            except ValueError as e:
                raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta JSON: {str(e)}")
            
            print("Información del pago:", payment_info)
            return payment_info
        else:
            error_details = response.text
            error_message = f"Error al confirmar el pago. Código: {response.status_code}, Detalles: {error_details}"
            print(error_message)
            raise HTTPException(status_code=response.status_code, detail=error_message)

    except httpx.RequestError as req_error:
        error_message = f"Error al realizar la solicitud HTTP: {str(req_error)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

    except Exception as e:
        error_message = f"Error inesperado al confirmar el pago: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
