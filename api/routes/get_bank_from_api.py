from fastapi import APIRouter
from api.services.get_bank_from_api import get_bank_from_api
from api.schemas.method_names import GetBankResponse

router = APIRouter()


@router.get('/bank_api', response_model=GetBankResponse)
async def route_get_bank(requisite: str, currency: str) -> GetBankResponse:
    requisite = ''.join(requisite.split())
    if requisite.isdigit() and len(requisite) == 16:
        bin = requisite[:6]
    else:
        detail = 'Неверные реквизиты'
        return GetBankResponse(success=False, result={'requisite': requisite}, detail=detail)
    data = await get_bank_from_api(bin)
    try:
        if data['currency'] == currency.upper():
            return GetBankResponse(success=True, result=data)
        else:
            detail = 'Неверная валюта'
            return GetBankResponse(success=False, result={'requisite': requisite}, detail=detail)
    except KeyError:
        detail = data['error']
        return GetBankResponse(success=False, result={'requisite': requisite}, detail=detail)
    except TypeError:
        detail = data
        return GetBankResponse(success=False, result={'requisite': requisite}, detail=detail)


