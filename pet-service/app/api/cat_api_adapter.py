import httpx
from app.config import settings
from app.api.middleware import logger


class CatAPIAdapter:
    def __init__(self):
        """
        Initialize the adapter with the API key.
        :param api_key: Your API key for The Cat API.
        """
        self.base_url = "https://api.thecatapi.com/v1/images/search"
        self.headers = {"x-api-key": settings.CAT_API_KEY}

    async def retrieve_image(self) -> dict:
        """
        Makes an API call to retrieve a cat image.
        :return: A dictionary containing image data from the API response.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, headers=self.headers)
                response.raise_for_status()  # Raise an HTTPStatusError for bad responses (4xx and 5xx)
                data = response.json()
                if data:
                    return data[0].get("url")
                else:
                    raise ValueError("No data returned from the API.")
            except httpx.RequestError as e:
                logger.warning(f"An error occurred while making the API call: {e}")
                return None
