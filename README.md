# FastAPI Ganache App

This project is a FastAPI application that connects to a local Ganache Ethereum blockchain. It provides functionalities for wallet generation, balance retrieval, and sending transactions.

## Project Structure

```
fastapi-ganache-app
├── app
│   ├── main.py          # Entry point of the FastAPI application
│   ├── wallet.py        # Functions for interacting with the Ethereum blockchain
│   └── __init__.py      # Marks the app directory as a Python package
├── requirements.txt      # Lists project dependencies
└── README.md             # Project documentation
```

## Requirements

To run this project, you need to have the following dependencies installed:

- FastAPI
- Web3
- Uvicorn (for running the FastAPI server)

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Running the Application

1. Ensure that Ganache is running on your local machine.
2. Navigate to the project directory.
3. Run the FastAPI application using Uvicorn:

```
uvicorn app.main:app --reload
```

4. Access the API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

- **Generate Wallet**
  - **Endpoint:** `/generate_wallet`
  - **Method:** `POST`
  - **Description:** Generates a new Ethereum wallet and returns the address and private key.

- **Get Balance**
  - **Endpoint:** `/get_balance/{address}`
  - **Method:** `GET`
  - **Description:** Retrieves the balance of the specified Ethereum address.

- **Send Transaction**
  - **Endpoint:** `/send_transaction`
  - **Method:** `POST`
  - **Description:** Sends a specified amount of Ether from one address to another.

## License

This project is licensed under the MIT License.