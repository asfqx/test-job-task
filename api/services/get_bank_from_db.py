from .dao import MethodNamesDAO


async def get_bank_from_db(bank):
    print(bank)
    if bank:
        bank = await MethodNamesDAO.get_one_or_none(name=f'{bank}')
        if bank is None:
            data = {
                'error': 'Этот банк не обслуживается'
            }
            return data
        data = {
            'id': bank.id,
            'name': bank.name,
            'currency': bank.currency,
        }
        return data
