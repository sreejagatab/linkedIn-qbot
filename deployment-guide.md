# LinkedIn Profile Query Bot - Deployment Guide

This guide provides instructions for deploying and running the LinkedIn Profile Query Bot, including the Wati integration.

## Overview

The LinkedIn Profile Query Bot consists of several components:

1. **Profile Data Scraper**: Captures and stores LinkedIn profile data
2. **Query Processor**: Processes natural language queries about LinkedIn profiles
3. **API Server**: Provides an API for querying profile data
4. **Wati Integration**: Connects the bot with Wati for WhatsApp messaging

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- A Wati account with API access
- A server with public IP address for webhook access

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/linkedin-profile-bot.git
cd linkedin-profile-bot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```
fastapi==0.95.0
uvicorn==0.21.1
pydantic==1.10.7
requests==2.28.2
spacy==3.5.2
python-dotenv==1.0.0
```

Install the spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

## Configuration

### 1. Create a Configuration File

Create a file named `config.json` with the following content:

```json
{
    "wati_api_key": "your_wati_api_key",
    "bot_api_url": "https://your-server-address/api",
    "profiles_dir": "profiles"
}
```

Replace `your_wati_api_key` with your Wati API key and `your-server-address` with your server's public address.

### 2. Environment Variables (Alternative to Configuration File)

Alternatively, you can use environment variables:

```bash
export WATI_API_KEY="your_wati_api_key"
export BOT_API_URL="https://your-server-address/api"
export PROFILES_DIR="profiles"
```

On Windows:
```cmd
set WATI_API_KEY=your_wati_api_key
set BOT_API_URL=https://your-server-address/api
set PROFILES_DIR=profiles
```

## Adding LinkedIn Profile Data

### Method 1: Using the API

You can add profiles via the API by sending a POST request to `/add-profile` with profile data in the request body. Example using curl:

```bash
curl -X POST "http://localhost:8000/add-profile" \
     -H "Content-Type: application/json" \
     -d @profile_data.json
```

Where `profile_data.json` contains the profile data in the format expected by the system.

### Method 2: Adding Profile Files Directly

You can also add profile data files directly to the `profiles` directory. Each file should be named `{profile_id}.json` and contain profile data in the expected format.

## Running the Bot

### 1. Start the API Server

```bash
python api_server.py
```

This will start the FastAPI server on port 8000.

### 2. Set Up Wati Integration

```bash
python wati_integration.py
```

This will set up the webhook in Wati and start listening for incoming messages.

## Deployment Options

### Option 1: Local Deployment with ngrok

For testing and development, you can use ngrok to expose your local server to the internet:

1. Install ngrok: https://ngrok.com/download
2. Run ngrok on the API server port:

```bash
ngrok http 8000
```

3. Update your `config.json` with the ngrok URL as `bot_api_url`.

### Option 2: Docker Deployment

A Dockerfile is provided for containerized deployment:

```bash
docker build -t linkedin-profile-bot .
docker run -p 8000:8000 -e WATI_API_KEY=your_wati_api_key linkedin-profile-bot
```

### Option 3: Cloud Deployment

The bot can be deployed to cloud platforms like AWS, Google Cloud, or Azure. Follow the platform-specific instructions for deploying Python applications.

## Wati Setup

1. Log in to your Wati account
2. Navigate to Settings > API & Webhook
3. Create a new API key if you don't have one
4. In the Webhook section, the `wati_integration.py` script will automatically set up the webhook for you

## Testing the Bot

1. Send a message to your WhatsApp business number connected to Wati
2. Ask a question about a LinkedIn profile, e.g., "What is the educational qualification of John Smith?"
3. The bot should process the query and respond with the requested information

## Troubleshooting

### Webhook Issues

If the webhook is not receiving messages:

1. Check that your server is publicly accessible
2. Verify that the webhook URL is correct in Wati
3. Check the server logs for any errors

### API Server Issues

If the API server is not responding:

1. Check that the server is running
2. Verify that the port is not blocked by a firewall
3. Check the server logs for any errors

### Query Processing Issues

If queries are not being processed correctly:

1. Check that profile data is loaded correctly
2. Verify that the query format is recognized by the system
3. Check the server logs for any errors in the query processor

## Monitoring and Logging

All components of the system include logging. Logs are written to the console by default. You can redirect logs to a file:

```bash
python api_server.py > api_server.log 2>&1
```

## Extending the Bot

### Adding More Profile Data Fields

To add support for additional profile data fields:

1. Update the profile data structure in `profile_scraper.py`
2. Add handling for the new fields in `query_processor.py`
3. Update the response generation in `_generate_response` method

### Improving NLP Processing

To improve the natural language processing capabilities:

1. Expand the keyword lists in `query_categories` in `ProfileQueryProcessor`
2. Add more sophisticated entity extraction in `extract_profile_name_from_query`
3. Consider integrating with more advanced NLP services like Google's Natural Language API or OpenAI's GPT models

## Security Considerations

- Store API keys securely (use environment variables or a secure vault)
- Implement authentication for the API server
- Use HTTPS for all communications
- Regularly audit access logs
- Consider implementing rate limiting for the API

## Additional Resources

- FastAPI documentation: https://fastapi.tiangolo.com/
- Wati API documentation: https://docs.wati.io/
- spaCy documentation: https://spacy.io/api
