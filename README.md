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

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:

```sh
git clone https://github.com/AnalyticAce/fastapi-ganache-app.git
cd fastapi-ganache-app
```

2. Set up the backend:

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Application

#### Backend

1. Start the backend server:

```sh
fastapi run app/main.py --host 0.0.0.0 --port 8080 --reload
```

#### Docker (Optional)

1. Build and run the Docker containers:

```sh
docker compose up --build
```

## API Documentation

The API documentation is available at `/docs` when the backend server is running. It provides detailed information about the available endpoints, request parameters, and responses.

### API Endpoints

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

## Contributing

We welcome contributions from the community! To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License.