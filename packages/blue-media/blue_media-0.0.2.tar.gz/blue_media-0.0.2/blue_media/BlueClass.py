import traceback
from aiohttp import (ClientSession, ClientTimeout, TCPConnector)


DEFAULT_TIMEOUT = ClientTimeout(total=1 * 60)
DEFAULT_TCP_SSL = False


class Config:
    """
    When initializing the environment, fill in the necessary parameters;
    otherwise, it will not pass。
    """
    def __init__(self, proxy: str = None, proxy_type="http", token: str = None):
        """
        init
        :param proxy: ip and port
        :param proxy_type: http or https
        :param token: secret token
        """
        self._check_params(proxy=proxy, token=token)
        self.proxy: str = f"{proxy_type}://{str(proxy)}"
        self.token: str = token

    @staticmethod
    def _check_params(**kwargs):
        """
        Check if the parameter is None.
        :param: Kwargs dict.
        :return: None
        :raise Value: If the argument is None, ValueError is raised.
        """
        for key, value in kwargs.items():
            if value is None: raise ValueError(f"{str(key)} is not allowed None")


class BlueMedia(object):

    def __init__(self, config: Config, timeout: ClientTimeout = DEFAULT_TIMEOUT):
        """
        :param config: Config Class
        :param timeout: default timeout(60s)
        """
        self.__proxies: str = config.proxy
        self.__headers: dict = {"Authorization": config.token}
        self.__timeout: ClientTimeout = timeout

    async def async_get(self, url: str, params: dict = None) -> tuple:
        """
        :param url: The target url
        :param params: params dict
        :return: Type: tuple, Example: (response_status, response_body, request_msg)
        """
        status, body, msg = -1, dict(), ''
        try:
            # Create an asynchronous HTTP client session with SSL/TLS support and a specified timeout
            async with ClientSession(connector=TCPConnector(ssl=DEFAULT_TCP_SSL), timeout=self.__timeout) as session:
                # Send a GET request to the specified URL with parameters, headers, and proxies
                async with session.get(url, params=params, headers=self.__headers, proxy=self.__proxies) as response:
                    # Parse the response body as a JSON dictionary
                    response_body: dict = await response.json()
                    status, body = response.status, response_body
        except Exception as e:
            msg = traceback.format_exc()
            raise e
        finally:
            # Return the status code and response body
            return status, body, msg

    async def async_post(self, url: str, payload: dict = None) -> tuple:
        """
        sync post
        :param url: The target url
        :param payload: payload dict
        :return: Type: tuple, Example: (response_status, response_body, request_msg)
        """
        status, body, msg = -1, dict(), ''
        try:
            # Create an asynchronous HTTP client session with SSL/TLS support and a specified timeout
            async with ClientSession(connector=TCPConnector(ssl=DEFAULT_TCP_SSL), timeout=self.__timeout) as session:
                # Send a POST request to the specified URL with payloads, headers, and proxies
                async with session.post(url, json=payload, headers=self.__headers, proxy=self.__proxies) as response:
                    # Parse the response body as a JSON dictionary
                    response_body: dict = await response.json()
                    status, body = response.status, response_body
        except Exception as e:
            msg = traceback.format_exc()
            raise e
        finally:
            # Return the status code and response body
            return status, body, msg
