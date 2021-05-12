import requests

API_SECRET = ''


def authenticate(api_secret: str):
    global API_SECRET

    API_SECRET = api_secret

    return API_SECRET


def fetch_json(
        url: str,
        http_method: str = "GET",
        data: dict = None,
        params=None,
        headers=None,
        use_api_secret: bool = True
):
    if not headers:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Apisecret {API_SECRET}'
        }

    headers['Accept'] = 'application/json'
    if use_api_secret:
        headers['Authorization'] = f'Apisecret {API_SECRET}'

    response = requests.request(method=http_method,
                                url=url,
                                data=data,
                                headers=headers,
                                params=params)

    if response.status_code == 401:
        raise Exception(f"Unauthorized: {response.text} - {url} - {response}")

    if response.status_code == 400:
        raise Exception(f'Error: {response.text} - {url}')

    return response


def get(url: str, data: dict = None, params: dict = None):
    response = fetch_json(url=url, http_method="GET", data=data, params=params)

    return response


def post(url: str,
         data=None,
         params: dict = None,
         headers: dict = None,
         use_api_secret: bool = True
         ):
    response = fetch_json(url=url,
                          http_method="POST",
                          data=data,
                          params=params,
                          headers=headers,
                          use_api_secret=use_api_secret)

    return response


def put(url: str, data=None, params: dict = None):
    response = fetch_json(url=url, http_method="PUT", data=data, params=params)

    return response


def delete(url: str, data=None, params: dict = None):
    response = fetch_json(url=url, http_method="DELETE", data=data, params=params)

    return response
