# Fenrir Api for Python

Python SDK for accessing Fenrir Cloud API.

## Warning

The contents of this repository is generated automatically using [openapi-generator](https://openapi-generator.tech).
Please refer to the [Cloud.Sdk.Templates](https://github.com/FenrirServer/Cloud.Sdk.Templates) repository.

## Installation

You can install this package from pip repository:

```bash
pip install fenrir-api
```

## Getting Started

```python
import fenrir_api
from fenrir_api.rest import ApiException

configuration = fenrir_api.Configuration(access_token = "YOUR_FENRIR_API_TOKEN")


with fenrir_api.ApiClient(configuration) as api_client:
    api_instance = fenrir_api.FenrirApi(api_client)

    try:
        result = api_instance.get_applications()    

        for application in result.applications:
            print(application)

    except ApiException as e:
        print(e)

```

## Documentation for API Endpoints

For the documentation for API endpoints, please refer to the [**docs/FenrirApi.md**](docs/FenrirApi.md)


## Contribution guide

Please refer to the [Cloud.Sdk.Templates](https://github.com/FenrirServer/Cloud.Sdk.Templates) repository for contributing.
We currently do not accept pull requests in this repo.
