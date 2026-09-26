import time
import uuid

from fastapi import Request


async def request_middleware(
    request: Request,
    call_next
):
    request_id = (
        request.headers.get("X-Request-ID")
        or str(uuid.uuid4())
    )

    start_time = time.time()

    response = await call_next(request)

    process_time = (
        time.time()
        - start_time
    )

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code}"
    )

    return response