<p align="center">
    <img src="https://drive.google.com/uc?id=114NBHl1_mjbSvKDyvJM85t6BygCXZ6ok" alt="pyzeus logo" width="250" height="250" />
</p>

# pyzeus ⚡

The cors middleware that enables a [FastAPI](https://fastapi.tiangolo.com) server to handle cors requests. It also handles preflight requests 😃.

## Installation

```py
pip install pyzeus
```

or

```py
pip3 install pyzeus
```

## Default Response Headers

If no options are provided, the response headers will be as follows:

```txt
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET,HEAD,PUT,PATCH,POST,DELETE
Access-Control-Allow-Headers: Content-Type
Access-Control-Max-Age: 5

```

#### NOTES

1. The allow_headers will always append `Content-Type` to your response headers so no need to add it to the list
2. To handle preflight requests you will specifically need to add a `@router.options(...)` to your router

## Usage Examples

### Router Instance

This implementation is equally

```py
from pyzeus import zeus
from fastapi import APIRouter, Depends

router = APIRouter(dependencies=[Depends(zeus().thunder)])

@router.get("/")
async def hander():
    return { "message": "lorem ipsum" }

@router.options("/")
async def options_hander():
    return None
```

### Specific Route

This implements a sync or async agnostic decorator that requires you to add request and response parameters in your route handler. Worry not, it works if you have pydanyic classes too! Needs python 3.8+ or run `pip install typing_extensions`

```py
from pyzeus import zeus
from fastapi import APIRouter, Depends

router = APIRouter()

# Synchronous example
@router.get("/")
@zeus().smite
def synchronous_handler(request: Request, response: Response):
    return { "message": "lorem ipsum" }

# Asynchronous example
@router.get("/")
@zeus().smite
async def asynchronous_handler(request: Request, response: Response):
    return { "message": "lorem ipsum" }

# Pydantic example
class Item(BaseModel):
    name: str

@router.post("/")
@zeus().smite
async def asynchronous_handler(request: Request, response: Response, item: Item):
    return { "message": item }
```

# Changelog

## v0.1.x

<details open>
<summary><strong>v0.1.2</strong></summary>

- Removed `functools`, and `typing_extensions` from dependencies

</details>

<details>
<summary><strong>v0.1.1</strong></summary>

- Added changelog to README
- Added dependencies

</details>

<details>
<summary><strong>v0.1.0</strong></summary>

- Initial release

</details>
