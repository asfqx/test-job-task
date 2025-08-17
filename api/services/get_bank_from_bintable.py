from bs4 import BeautifulSoup
import httpx
from .banks import banks
from .get_bank_from_redis import redis


async def fetch_bin_codes():
    for bank_ur in banks.keys():
        url = f"https://bintable.com/issuer/ru/{bank_ur}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        bin_links = soup.select('td:first-child > a.text-info[href^="bin/"]')
        bins = [link.text.strip() for link in bin_links]
        for bin in bins:
            await redis.set(f'{bin}', banks[bank_ur])

