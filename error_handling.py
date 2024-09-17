# use http status code
# customize error messages
# use fastapi exception hanmdles
# logging
# global error handler
# consistent error response format
# validation errors

# custome exception handling
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

async def custom_exception_handler(request: Request, exc: HTTPException):
  return JSONResponse(
    status_code=500, 
    content={"message": "Internal Sever Error"})

app.add_exception_handler(Exception, custom_exception_handler)

@app.get("/custom")
async def custom_endpoint():
  try:
    result = 1 / 0
    return {"result": result}
  except Exception as e:
    return await custom_exception_handler(None, e)