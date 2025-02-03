from fastapi import FastAPI, HTTPException, APIRouter, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.wallet import generate_wallet, get_balance, send_transaction
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="FASTAPI SIMPLE GANACHE",
    description="Simple API for Ethereum Wallet Management with Ganache Integration",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    version="1.0.0",
    docs_url=None,
    openapi_tags=[{
        'name': 'Wallet',
        'description': 'Ethereum wallet operations'
    }, {
        'name': 'UI',
        'description': 'Web interface endpoints'
    }]
)

app.mount("/static", StaticFiles(directory="app/template/static"), name="static")
app.mount("/template", StaticFiles(directory="app/template"), name="template")
templates = Jinja2Templates(directory="app/template")

class TransactionRequest(BaseModel):
    sender: str
    receiver: str
    private_key: str
    amount: float

    class Config:
        json_schema_extra = {
            "example": {
                "sender": "0x21a12881C2Fd44BC6D0f908D92c504fEA507b5D4",
                "receiver": "0x8f6a04B0448B89dfeA3f6798Ba0CF428b799b3C5",
                "private_key": "0xd2d3b63e77c58d86f205d6c9d6c4201118e838ea672865fb29af31d0ae7f0262",
                "amount": 1.5
            }
        }

@app.get("/", 
    response_class=HTMLResponse,
    tags=["UI"],
    summary="Web Interface",
    description="Serves the main wallet management web interface"
)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Ethereum Wallet Manager"
    })

wallet_router = APIRouter(
    prefix="/api",
    tags=["Wallet"],
    responses={404: {"description": "Not found"}},
)

@wallet_router.post("/generate-wallet/",
    summary="Generate New Wallet",
    description="Creates a new Ethereum wallet with generated address and private key",
    response_description="Wallet credentials",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Successfully created new wallet",
            "content": {
                "application/json": {
                    "example": {
                        "address": "0x123...abc",
                        "private_key": "0x456...def"
                    }
                }
            }
        }
    }
)
def create_wallet():
    """Generate a new Ethereum wallet with address and private key pair"""
    wallet = generate_wallet()
    return {"address": wallet.address, "private_key": wallet.key.hex()}

@wallet_router.get("/balance/{address}",
    summary="Get Wallet Balance",
    description="Retrieve ETH balance and USD equivalent for a wallet address",
    response_description="Balance information",
    responses={
        200: {
            "description": "Balance retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "address": "0x123...abc",
                        "balance": 2456.78,
                        "eth_balance": 1.5
                    }
                }
            }
        },
        400: {
            "description": "Invalid address format",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid Ethereum address"}
                }
            }
        }
    }
)
def balance(address: str):
    """
    Get balance for a specific Ethereum address
    
    - **address**: Valid Ethereum wallet address (required)
    """
    try:
        eth_balance, usd_balance = get_balance(address)
        return {
            "address": address,
            "balance": usd_balance,
            "eth_balance": eth_balance
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@wallet_router.post("/send-transaction/",
    summary="Send Ethereum Transaction",
    description="Send ETH between wallets using private key authentication",
    response_description="Transaction confirmation",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Transaction successful",
            "content": {
                "application/json": {
                    "example": {
                        "transaction_hash": "0x9a2...b7c",
                        "sender": "0x123...abc",
                        "receiver": "0x456...def",
                        "amount": 1.5,
                        "status": "success"
                    }
                }
            }
        },
        400: {
            "description": "Transaction failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Insufficient funds"}
                }
            }
        }
    }
)
async def transaction(request: TransactionRequest):
    """
    Send ETH between wallets
    
    - **sender**: Valid sender Ethereum address
    - **receiver**: Valid recipient Ethereum address
    - **private_key**: Sender's private key for signing
    - **amount**: ETH amount to send (positive number)
    """
    try:
        tx_hash = send_transaction(
            request.sender,
            request.receiver,
            request.private_key,
            request.amount
        )
        return {
            "transaction_hash": tx_hash,
            "sender": request.sender,
            "receiver": request.receiver,
            "amount": request.amount,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

app.include_router(wallet_router)

@app.get("/docs", 
    include_in_schema=False,
    tags=["UI"],
    summary="API Documentation",
    description="Custom Swagger UI documentation endpoint"
)
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