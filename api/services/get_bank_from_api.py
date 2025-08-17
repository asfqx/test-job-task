from httpx import AsyncClient, Timeout
from api.config import settings
from .get_bank_from_db import get_bank_from_db
from .get_bank_from_redis import get_bank_from_redis
from .banks import banks


async def get_bank_from_api(bin):
    timeout = Timeout(10)
    async with AsyncClient(timeout=timeout) as client:
        try:
            headers = {
                'apikey': settings.API_KEY,
            }
            response = await client.get(url=f'https://api.apilayer.com/bincheck/{bin}', headers=headers)
        except Exception as e:
            data = {
                'error': 'Такого bin не существует',
            }
            return data
    if response.status_code == 200:
        result = response.json()
        bank_name = result['bank_name'].replace(' ', '-').upper()
        if bank_name in banks.keys():
            bank = await get_bank_from_redis(bin)
        else:
            bank = 'По номеру карты'
        return await get_bank_from_db(bank)
    else:
        data = {
            'error': 'Такого bin не существует',
        }
        return data
