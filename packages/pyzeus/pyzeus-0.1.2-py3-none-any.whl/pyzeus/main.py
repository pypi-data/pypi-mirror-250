from fastapi import Request, Response, status, HTTPException
from functools import wraps
from typing_extensions import Union, List, Optional, Callable, Any

class Zeus:
    """The Zeus return type; `thunder` is what you would use for all paths on a router whereas `smite` is what you would use for a singular"""

    thunder: Callable[[Request, Response], None]
    """Use to add cors to all paths on a router with the FastAPI `Depends` function in the FastAPI `APIRouter(dependencies=[Depends(...)])` class"""
    smite: Callable[[Any], Any]
    """Use to add cors to a specific routen a router with decorator notation; `@zeus().smite`"""

    def __init__(
        self,
        thunder: Callable[[Request, Response], None],
        smite: Callable[[Any], Any],
    ):
        self.thunder = thunder
        self.smite = smite


def zeus(
    origins: Optional[Union[str, List[str]]] = None,
    methods: Optional[List[str]] = None,
    allowed_headers: Optional[List[str]] = None,
    max_age: Optional[int] = None,
    allow_credentials: Optional[bool] = None,
    exposed_headers: Optional[List[str]] = None,
) -> Zeus:
    """
    ## Zeus ⚡

    The cors middleware that enables a `FastAPI` server to handle cors requests, specifically, on the router and individual route level. It also handles preflight requests :)

    ### Default Response Headers

    If no options are provided, the response headers will be as follows:

    ```txt
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Methods: GET,HEAD,PUT,PATCH,POST,DELETE
    Access-Control-Allow-Headers: Content-Type
    Access-Control-Max-Age: 5

    ```

    ##### NOTES
    1. The allow_headers will always append `Content-Type` to your response headers so no need to add it to the list
    2. To handle preflight requests you will specifically need to add a `@router.options(...)` to your router

    ### Usage Examples

    #### Router Instance

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

    #### Specific Route

    This implements a sync or async agnostic decorator that requires you to add request and response parameters in your route handler. Worry not, it works if you have pydanyic classes too!

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
    """

    __origins: Union[str, List[str]] = "*" if not origins else origins

    __methods: List[str] = (
        ["GET", "HEAD", "PUT", "PATCH", "POST", "DELETE"] if not methods else methods
    )

    __allowed_headers: List[str] = (
        ["Content-Type"] if not allowed_headers else allowed_headers
    )

    if "Content-Type" not in __allowed_headers:
        __allowed_headers.append("Content-Type")

    __max_age: int = 5 if not max_age else max_age

    __allow_credentials: Optional[bool] = (
        None if not allow_credentials else allow_credentials
    )

    __exposed_headers: Optional[List[str]] = (
        None if not exposed_headers else allowed_headers
    )

    def __is_origin__(path: str) -> bool:
        if isinstance(__origins, list):
            return path in __origins
        else:
            return path == __origins

    def __is_valid_method__(method: str) -> bool:
        return method in __methods

    def __is_valid_request_headers__(headers: str) -> bool:
        headers_list = headers.split(",")
        allowed_headers_list = ",".join(__allowed_headers).lower().split(",")
        valid: bool = True

        for header in headers_list:
            if header.lower().strip() not in allowed_headers_list:
                valid = False

        return valid

    def __valid_req_handler__(res: Response, origin: str) -> None:
        if isinstance(__origins, list):
            res.headers.append("Access-Control-Allow-Origin", origin)
            res.headers.append("Vary", "Accept-Encoding, Origin")
        else:
            res.headers.append("Access-Control-Allow-Origin", "*")
            res.headers.append("Vary", "Accept-Encoding, Origin")

        res.headers.append("Access-Control-Allow-Headers", ",".join(__allowed_headers))

        res.headers.append("Access-Control-Max-Age", str(__max_age))

        if __allow_credentials:
            res.headers.append("Access-Control-Allow-Credentials", "true")

        if __exposed_headers:
            res.headers.append(
                "Access-Control-Expose-Headers", ",".join(__exposed_headers)
            )

    def __middleware__(req: Request, res: Response) -> None:
        """CORS middleware"""
        origin: str = ""
        is_valid_origin: bool = False
        method: str = ""
        is_valid_method: bool = False
        request_headers: Union[str, None] = None
        is_valid_headers: bool = False

        if req.method == "OPTIONS":
            # Get the origin header and compare it's value to the initialised value
            origin = req.headers["origin"] if req.headers.get("origin") else "*"
            is_valid_origin: bool = (
                True if __origins == "*" else __is_origin__(path=origin)
            )

            # Get the request method header (if none, then use the request mehtod) and compare it's value to the initialised value
            method = (
                req.headers["access-control-request-method"]
                if req.headers.get("access-control-request-method")
                else req.method
            )
            is_valid_method = __is_valid_method__(method=method)

            # In case of a preflight, check the request headers and compare them to the allowed headers
            request_headers = (
                req.headers["access-control-request-headers"]
                if req.headers.get("access-control-request-headers")
                else None
            )

            is_valid_headers = (
                True
                if not request_headers
                else __is_valid_request_headers__(headers=request_headers)
            )

            if is_valid_origin and is_valid_method and is_valid_headers:
                __valid_req_handler__(res=res, origin=origin)

                res.headers.append("Access-Control-Allow-Methods", ",".join(__methods))

                res.status_code = status.HTTP_204_NO_CONTENT
                return None

            elif not is_valid_origin:
                res.status_code = status.HTTP_400_BAD_REQUEST
                raise HTTPException(status_code=400, detail="Bad request")

            elif not is_valid_method:
                res.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
                raise HTTPException(status_code=405, detail="Method not allowed")

            else:
                res.status_code = status.HTTP_406_NOT_ACCEPTABLE
                raise HTTPException(status_code=406, detail="Not acceptable")
        else:
            host = req.headers["host"]
            is_valid_origin: bool = (
                True if __origins == "*" else __is_origin__(path=host)
            )
            is_valid_method = __is_valid_method__(method=req.method)

            if is_valid_origin and is_valid_method:
                __valid_req_handler__(res=res, origin=host)

            elif not is_valid_method:
                res.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
                raise HTTPException(status_code=405, detail="Method not allowed")

            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                raise HTTPException(status_code=400, detail="Bad request")

    def __decorator__(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                request: Request = kwargs["request"]
                response: Response = kwargs["response"]

                __middleware__(req=request, res=response)

                if response.status_code and response.status_code > 300:
                    return None

                try:
                    return await func(*args, **kwargs)
                except:
                    return func(*args, **kwargs)
            except:
                raise HTTPException(
                    status_code=500,
                    detail="Ensure that both 'request: Request' and 'response: Response' are params in your route handler",
                )

        return wrapper

    return Zeus(thunder=__middleware__, smite=__decorator__)
