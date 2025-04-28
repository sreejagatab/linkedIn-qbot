# LinkedIn Profile Query Bot

A bot that retrieves pre-captured data from LinkedIn profiles and answers user queries based on this information, with Wati integration for WhatsApp.

## Features

- 📊 **Profile Data Capture**: Structured system for capturing and storing LinkedIn profile data
- 🔍 **Natural Language Queries**: Process questions like "What is the educational qualification of [Name]?"
- 🤖 **Intelligent Response Generation**: Context-aware responses based on structured profile data
- 💬 **WhatsApp Integration**: Connect with users via WhatsApp through Wati
- 🔄 **Extensible Architecture**: Easy to add new profile fields and query capabilities

## System Architecture

The system consists of several components:

1. **Profile Data Scraper**: Captures and structures LinkedIn profile data
2. **Query Processor**: NLP system for understanding user queries
3. **API Server**: FastAPI backend for query processing
4. **Wati Integration**: Module for connecting with the Wati API

## Quick Start

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (optional, for containerized deployment)
- Wati account with API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-profile-bot.git
   cd linkedin-profile-bot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. Configure the bot:
   ```bash
   cp .env.example .env
   # Edit .env with your Wati API key and other settings
   ```

### Running the Bot

#### Option 1: Direct Python Execution

1. Start the API server:
   ```bash
   python api_server.py
   ```

2. In a separate terminal, start the Wati integration:
   ```bash
   python wati_integration.py
   ```

#### Option 2: Docker Compose

1. Start all services:
   ```bash
   docker-compose up -d
   ```

2. View logs:
   ```bash
   docker-compose logs -f
   ```

### Adding Profile Data

#### Method 1: API Endpoint

Send a POST request to the `/add-profile` endpoint with profile data:

```bash
curl -X POST "http://localhost:8000/add-profile" \
     -H "Content-Type: application/json" \
     -d @sample_profile.json
```

#### Method 2: Direct File Placement

Add JSON files directly to the `profiles` directory, with filenames in the format `{profile_id}.json`.

## Using the Bot

Once set up, users can interact with the bot via WhatsApp by sending messages to your WhatsApp Business number connected to Wati.

Example queries:
- "What is the educational qualification of John Smith?"
- "Tell me about Sara Johnson's work experience"
- "What skills does John Smith have?"
- "Where is Sara Johnson located?"

## Development

### Project Structure

```
linkedin-profile-bot/
├── api_server.py           # FastAPI server for query processing
├── query_processor.py      # NLP query processor
├── profile_scraper.py      # LinkedIn profile data capture
├── wati_integration.py     # Wati API integration
├── profiles/               # Directory for profile data
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── .env                    # Environment configuration
```

### Extending the Bot

To add support for new profile fields:

1. Update the profile data structure in `profile_scraper.py`
2. Add relevant keywords to `query_categories` in `query_processor.py`
3. Update the response generation in `_generate_response` method

## Deployment Options

### Local Development with ngrok

For testing with Wati webhooks:

1. Install ngrok: https://ngrok.com/download
2. Expose your local server:
   ```bash
   ngrok http 8000
   ```
3. Update `.env` with the ngrok URL as `BOT_API_URL`

### Cloud Deployment

The Docker setup makes it easy to deploy to any cloud platform that supports Docker, including:

- AWS ECS or EC2
- Google Cloud Run or GKE
- Azure Container Instances or AKS
- Digital Ocean App Platform or Droplets

## Technical Details

### Query Processing Flow

1. User sends a message via WhatsApp
2. Wati forwards the message to the bot's webhook
3. The bot processes the query using NLP to identify:
   - Profile being asked about
   - Information category (education, experience, etc.)
   - Specific details being requested
4. The bot retrieves profile data and generates a response
5. The response is sent back to the user via Wati

### Profile Data Structure

Profile data is stored in JSON format with structured fields including:
- Basic information (name, headline, location)
- Contact information
- Work experience
- Education
- Skills
- Languages
- Certifications
- Projects and publications

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The NLP component uses [spaCy](https://spacy.io/) for natural language processing
- API server built with [FastAPI](https://fastapi.tiangolo.com/)
- WhatsApp integration via [Wati API](https://docs.wati.io/)
