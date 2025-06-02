from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <h1>Test Page</h1>
            <p>If you can see this, the server is working!</p>
        </body>
    </html>
    """ 