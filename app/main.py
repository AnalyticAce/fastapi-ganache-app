from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.wallet import generate_wallet, get_balance, send_transaction

app = FastAPI(
    title="FASTAPI SIMPLE GANACHE",
    description="Simple API for Ethereum Wallet",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    version="1.0.0",
    docs_url=None,
)
    
wallet_router = APIRouter(
    prefix="/api",
    tags=["Wallet"],
    responses={404: {"description": "Not found"}},
)

@wallet_router.post("/generate-wallet/")
def create_wallet():
    wallet = generate_wallet()
    return {"address": wallet.address, "private_key": wallet.key.hex()}

@wallet_router.get("/balance/{address}")
def balance(address: str):
    try:
        eth_balance, balance = get_balance(address)
        return {
            "address": address,
            "balance": balance,
            "eth_balance": eth_balance
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@wallet_router.post("/send-transaction/")
def transaction(sender: str, receiver: str, private_key: str, amount: float):
    try:
        tx_hash = send_transaction(sender, receiver, private_key, amount)
        return {
            "transaction_hash": tx_hash,
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

app.include_router(wallet_router)

app.mount("/template", StaticFiles(directory="app/template"), name="template")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    with open("app/template/custom_swagger.html") as f:
        template = f.read()
    
    return HTMLResponse(
        template.replace(
            "{{ title }}", 
            "FASTAPI SIMPLE GANACHE Documentation"
        ).replace(
            "{{ openapi_url }}", 
            "/openapi.json"
        )
    )