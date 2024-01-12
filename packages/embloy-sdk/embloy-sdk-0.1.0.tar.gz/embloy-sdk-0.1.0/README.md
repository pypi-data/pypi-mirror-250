# Embloy Node

Embloy's Node SDK for interacting with your Embloy integration.

## Usage

Install Embloy-Node SDK:

```Bash
pip install embloy-sdk
```

Integrate it in your service:

```Python
// In your application or script
client_token = 'your_client_token'
session_data = {
    'success_url': 'https://example.com/success',
    'cancel_url': 'https://example.com/cancel',
    'job_slug': 'example_job'
}

embloy_client = EmbloyClient(client_token, session_data)
try:
    result = embloy_client.make_request()
    print(result)
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

## Publish Package
```Bash
python setup.py sdist bdist_wheel

twine upload dist/*
```

---

© Carlo Bortolan, Jan Hummel

> Carlo Bortolan &nbsp;&middot;&nbsp;
> GitHub [@carlobortolan](https://github.com/carlobortolan) &nbsp;&middot;&nbsp;
> contact via [bortolanoffice@embloy.com](mailto:bortolanoffice@embloy.com)
>
> Jan Hummel &nbsp;&middot;&nbsp;
> GitHub [@github4touchdouble](https://github.com/github4touchdouble) &nbsp;&middot;&nbsp;
> contact via [hummeloffice@embloy.com](mailto:hummeloffice@embloy.com)

