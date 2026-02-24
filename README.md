# Roof Comfort - AI Sales Assistant API

An API to serve as an AI-powered sales assistant for the "Roof Comfort" building, designed to answer customer inquiries about available flats and building amenities, I will be using this in a website that I created.

## Overview

This project is an AI chatbot that can:

*   Provide detailed information about different flat types.
*   Suggest flats based on user requirements (e.g., size, number of rooms).
*   Answer questions about building amenities (Gym, Pool, Tennis Court).
*   Handle basic conversational interactions.
*   Use Ids of Image Assets when needed in the chat directly later to be replaced via the front-end.

## Features

*   **Conversational AI**: Utilizes the Gemini API to provide natural and intelligent responses.
*   **Data-Driven**: Reads flat data from a CSV file, making it easily customizable.
*   **Web & CLI Interface**: Includes a Flask web server for API access and a command-line interface for testing.
*   **Easy to Deploy**: Can be deployed to services like Heroku.

## Setup and Deployment

### Prerequisites

*   Python 3.7+
*   `pip` for installing packages

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ProbChatApi.git
    cd ProbChatApi
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root directory and add your Google API key:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

### Running the Application

*   **To run the web server:**
    ```bash
    python app.py
    ```
    The server will start on `http://127.0.0.1:5000`.

*   **To run the command-line interface:**
    ```bash
    python cli.py
    ```

## API Usage

Make a POST request to the `/api/chat` endpoint with a JSON payload:

```json
{
  "message": "Hello, I'm interested in a 2-bedroom apartment.",
  "history": []
}
```

The `history` array should contain the previous messages in the conversation to maintain context.

## Contribution and Adaptation

This project can be adapted for other use cases or extended with new features.

### Customization

*   **Data Source**: The AI's knowledge is based on the `flats.csv` file. This can be replaced with any other CSV file to suit your needs. The flat table is injected into `system_prompt.txt` using the `{FLAT_DATA}` placeholder.
*   **AI Persona**: Update `system_prompt.txt` to change the assistant's personality and behavior for both `app.py` and `cli.py`.

### Extending the Project

*   **Backend**: The Flask application can be extended to include more data sources, integrate with other APIs, or add more complex business logic.
*   **Frontend**: A user interface can be built to interact with the chatbot's API endpoint.

We welcome contributions to improve this project. Feel free to fork the repository, make your changes, and submit a pull request.
