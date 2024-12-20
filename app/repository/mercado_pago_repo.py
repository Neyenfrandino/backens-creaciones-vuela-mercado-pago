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

        # Validar respuesta de la API
        if response.get("status") in [200, 201]:  # Estados HTTP de éxito
            print("Preferencia creada exitosamente:", response.get("response"))
            return response.get("response")
        else:
            error_details = response.get("response", {}).get("message", "Sin detalles")
            error_message = f"Error al crear preferencia. Código: {response.get('status')}, Detalles: {error_details}"
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
    # Validar que el payment_id no sea vacío
    if not payment_id:
        raise HTTPException(status_code=400, detail="El ID del pago no puede estar vacío.")

    url = f"{MP_API_BASE_URL}/payments/{payment_id}"
    
    try:
        # Realizar la solicitud GET a la API de MercadoPago
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
        
        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            payment_info = response.json()
            print("Información del pago:", payment_info)
            return payment_info
        else:
            # Si la respuesta no fue exitosa, lanzar un error
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
