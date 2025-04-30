# LinkedIn Profile Query Bot

A comprehensive system that retrieves pre-captured data from LinkedIn profiles and answers natural language queries based on this information, with WhatsApp integration through the Wati API.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-Apache%202.0-orange)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Running the Bot](#running-the-bot)
- [Managing Profiles](#managing-profiles)
- [Query Capabilities](#query-capabilities)
- [WhatsApp Integration](#whatsapp-integration)
- [Deployment Options](#deployment-options)
- [Technical Details](#technical-details)
- [Extending the System](#extending-the-system)
- [Performance and Scalability](#performance-and-scalability)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

The LinkedIn Profile Query Bot is a powerful system designed to store structured LinkedIn profile data and answer natural language queries about these profiles. It features a robust query processing engine that can understand various types of questions and extract relevant information from stored profiles. The system integrates with WhatsApp through the Wati API, allowing users to interact with the bot via WhatsApp messages.

## Features

- 📊 **Comprehensive Profile Storage**: Structured system for storing detailed LinkedIn profile data including education, experience, skills, certifications, languages, projects, and more
- 🔍 **Advanced Natural Language Processing**: Process complex questions like "What is the highest educational qualification of [Name]?" or "Tell me about [Name]'s experience at [Company]"
- 🤖 **Context-Aware Response Generation**: Intelligent responses based on query context and profile data
- 💬 **WhatsApp Integration**: Seamless connection with users via WhatsApp through Wati API
- 🔄 **Extensible Architecture**: Modular design makes it easy to add new profile fields and query capabilities
- 🔌 **API-First Design**: RESTful API for easy integration with other systems
- 🐳 **Docker Support**: Containerized deployment for easy scaling and management
- 🔒 **Secure Profile Management**: Controlled access to profile data through API endpoints

## System Architecture

The system consists of four main components that work together to provide a seamless experience:

1. **Profile Data Management**
   - Stores structured LinkedIn profile data in JSON format
   - Supports adding profiles via API or direct file placement
   - Maintains a consistent data structure for all profiles

2. **Query Processor**
   - Natural language processing to understand user queries
   - Entity extraction to identify profile names and specific requests
   - Category classification to determine query intent (education, experience, skills, etc.)
   - Response generation based on profile data and query context

3. **API Server**
   - FastAPI-based RESTful API for query processing
   - Endpoints for profile management (listing, adding, querying)
   - Webhook endpoint for Wati integration
   - Comprehensive API documentation with Swagger UI

4. **Wati Integration**
   - Connects with Wati API for WhatsApp messaging
   - Processes incoming messages from WhatsApp users
   - Sends responses back to users via WhatsApp
   - Supports template messages and session management

## Installation

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (optional, for containerized deployment)
- Wati account with API key (for WhatsApp integration)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/linkedin-profile-bot.git
cd linkedin-profile-bot
```

### Step 2: Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

For a standard installation:
```bash
pip install -r requirements.txt
```

For a minimal installation (without spaCy):
```bash
pip install -r requirements-simple.txt
```

### Step 4: Configure the Bot

```bash
cp .env.example .env
# Edit .env with your Wati API key and other settings
```

Example `.env` configuration:
```
# Wati API Key
WATI_API_KEY=your_wati_api_key_here

# Bot API URL (for webhook registration)
BOT_API_URL=http://localhost:8000

# Profiles directory
PROFILES_DIR=profiles

# Wati API URL
WATI_API_URL=https://eu-app-api.wati.io/api/v1
```

## Running the Bot

### Option 1: Direct Python Execution

1. Start the API server:
   ```bash
   python api_server.py
   ```

2. In a separate terminal, start the Wati integration:
   ```bash
   python wati_integration.py
   ```

### Option 2: Docker Compose

1. Start all services:
   ```bash
   docker-compose up -d
   ```

2. View logs:
   ```bash
   docker-compose logs -f
   ```

### Verifying the Installation

1. Access the API documentation at `http://localhost:8000/docs`
2. Test a simple query:
   ```bash
   curl -X POST "http://localhost:8000/query" \
        -H "Content-Type: application/json" \
        -d '{"query": "Tell me about John Smith"}'
   ```

## Managing Profiles

The system comes with several sample profiles pre-installed:

- **John Smith**: Senior Software Engineer with cloud and distributed systems expertise
- **Sara Johnson**: Data Scientist specializing in machine learning and AI
- **Michael Zhang**: Full Stack Developer and DevOps Engineer
- **Priya Patel**: Product Manager and UX Strategist
- **James Wilson**: Marketing Director and Growth Strategist

### Adding New Profiles

#### Method 1: API Endpoint

Send a POST request to the `/add-profile` endpoint with profile data:

```bash
curl -X POST "http://localhost:8000/add-profile" \
     -H "Content-Type: application/json" \
     -d @new_profile.json
```

#### Method 2: Direct File Placement

Add JSON files directly to the `profiles` directory, with filenames in the format `{profile_id}.json`.

### Profile Data Structure

Each profile includes the following sections:
- **basics**: Name, headline, location, summary, etc.
- **contact_info**: Email, phone, websites, social media
- **experience**: Work history with company, title, duration, and description
- **education**: Academic background with degrees, institutions, and dates
- **skills**: List of professional skills and competencies
- **languages**: Languages spoken with proficiency levels
- **certifications**: Professional certifications with issuer and date
- **projects**: Notable projects with descriptions and links
- **publications**: Published works with title, publisher, and date
- **recommendations**: Testimonials from colleagues and managers

## Query Capabilities

The system can process a wide range of natural language queries about profiles:

### Education Queries
- "What is the educational qualification of John Smith?"
- "Where did Sara Johnson study?"
- "What is Michael Zhang's highest degree?"
- "Tell me about Priya Patel's MBA"

### Experience Queries
- "What is John Smith's current job?"
- "Tell me about Sara Johnson's work experience at AI Research Lab"
- "What was Michael Zhang's role at Web Innovations?"
- "How long has James Wilson been working at Global Tech Enterprises?"

### Skills Queries
- "What skills does John Smith have?"
- "Is Sara Johnson skilled in machine learning?"
- "Tell me about Michael Zhang's technical skills"
- "What are Priya Patel's product management skills?"

### Languages Queries
- "What languages does John Smith speak?"
- "Is Sara Johnson fluent in French?"
- "Tell me about Michael Zhang's language proficiency"

### Certifications Queries
- "What certifications does John Smith have?"
- "Tell me about Sara Johnson's AWS certification"
- "When did Michael Zhang get his Kubernetes certification?"

### Location Queries
- "Where is John Smith located?"
- "What city does Sara Johnson live in?"
- "Tell me about Michael Zhang's location"

### General Queries
- "Tell me about John Smith"
- "Who is Sara Johnson?"
- "Give me an overview of Michael Zhang's profile"
- "What can you tell me about Priya Patel?"

## WhatsApp Integration

The system integrates with WhatsApp through the Wati API, allowing users to interact with the bot via WhatsApp messages.

### Setting Up Wati Integration

1. Create a Wati account at [https://app.wati.io/](https://app.wati.io/)
2. Set up a WhatsApp Business account and connect it to Wati
3. Get your Wati API key from the Wati dashboard
4. Add the API key to your `.env` file
5. Set up a webhook in the Wati dashboard pointing to your bot's webhook endpoint (`/wati-webhook`)

### Testing the Integration

1. Start the API server and Wati integration
2. Send a message to your WhatsApp Business number
3. The bot should process the query and respond with relevant information

### Webhook Configuration

For production deployment, you'll need to expose your webhook endpoint to the internet. Options include:

- Using a reverse proxy like Nginx
- Deploying to a cloud provider with a public IP
- Using a service like ngrok for testing

## Deployment Options

### Local Development with ngrok

For testing with Wati webhooks during development:

1. Install ngrok: [https://ngrok.com/download](https://ngrok.com/download)
2. Expose your local server:
   ```bash
   ngrok http 8000
   ```
3. Update `.env` with the ngrok URL as `BOT_API_URL`
4. Configure the Wati webhook to point to your ngrok URL

### Docker Deployment

The included Docker configuration makes it easy to deploy the system:

```bash
# Build the Docker image
docker build -t linkedin-profile-bot .

# Run the container
docker run -p 8000:8000 -v ./profiles:/app/profiles linkedin-profile-bot
```

### Cloud Deployment

The Docker setup makes it easy to deploy to any cloud platform that supports Docker:

#### AWS Deployment
- Deploy to ECS (Elastic Container Service) for managed container orchestration
- Use EC2 instances with Docker installed for more control
- Configure an Application Load Balancer for high availability

#### Google Cloud Deployment
- Deploy to Google Cloud Run for serverless container execution
- Use GKE (Google Kubernetes Engine) for Kubernetes-based deployment
- Set up Cloud IAM for secure access control

#### Azure Deployment
- Deploy to Azure Container Instances for simple container hosting
- Use AKS (Azure Kubernetes Service) for Kubernetes-based deployment
- Configure Azure API Management for API gateway functionality

#### Digital Ocean Deployment
- Deploy to Digital Ocean App Platform for managed container hosting
- Use Digital Ocean Droplets with Docker for more control
- Set up a Digital Ocean Load Balancer for high availability

## Technical Details

### Query Processing Flow

1. **User Interaction**: User sends a message via WhatsApp or API
2. **Message Routing**: Wati forwards the message to the bot's webhook
3. **Query Analysis**:
   - Extract profile name/ID from the query
   - Identify query category (education, experience, etc.)
   - Extract specific request details (highest degree, current job, etc.)
4. **Profile Retrieval**: Load the relevant profile data
5. **Response Generation**: Generate a natural language response based on the query and profile data
6. **Response Delivery**: Send the response back to the user via Wati or API

### NLP Implementation

The system uses a combination of techniques for natural language processing:

- **Entity Extraction**: Identify names, organizations, and other entities in the query
- **Keyword Matching**: Match query keywords to predefined categories
- **Pattern Recognition**: Use regex patterns to extract specific request details
- **Context Analysis**: Consider the overall context of the query for better understanding

### API Endpoints

The system provides the following API endpoints:

- **GET /**: API root endpoint
- **GET /profiles**: List all available profiles
- **POST /query**: Process a query about a LinkedIn profile
- **POST /add-profile**: Add a new LinkedIn profile
- **POST /wati-webhook**: Webhook endpoint for Wati integration

## Extending the System

### Adding New Profile Fields

To add support for new profile fields:

1. Update the profile data structure in `profile_scraper.py`
2. Add relevant keywords to `query_categories` in `query_processor.py`
3. Update the response generation in `_generate_response` method

Example: Adding support for "Volunteer Experience"

```python
# In query_processor.py
self.query_categories = {
    # Existing categories...
    "volunteer": ["volunteer", "volunteering", "community service", "nonprofit", "charity"]
}

# In _generate_response method
elif category == "volunteer":
    if not profile.get("volunteer_experience"):
        return f"{profile_name} has no volunteer experience information in their profile."

    vol_list = [f"{vol['role']} at {vol['organization']} ({vol['duration']})"
                for vol in profile["volunteer_experience"]]
    return f"{profile_name}'s volunteer experience: {'; '.join(vol_list)}."
```

### Enhancing NLP Capabilities

For more advanced NLP capabilities, consider:

1. Integrating a full spaCy model for better entity recognition
2. Implementing a machine learning classifier for query categorization
3. Adding support for more complex queries with multiple intents
4. Implementing conversational context to handle follow-up questions

### Adding New Response Types

To support new types of responses:

1. Create a new response generation method in `query_processor.py`
2. Add logic to handle the new response type in the main processing flow
3. Update the API documentation to reflect the new capabilities

## Performance and Scalability

### Current Performance

The system is designed to handle a moderate load of queries:

- **Response Time**: Typically under 200ms per query
- **Concurrency**: Can handle multiple simultaneous requests
- **Profile Capacity**: Efficiently manages hundreds of profiles

### Scaling Strategies

For higher loads, consider the following scaling strategies:

- **Horizontal Scaling**: Deploy multiple instances behind a load balancer
- **Caching**: Implement Redis caching for frequently accessed profiles
- **Database Integration**: Move from file-based storage to a database for larger profile collections
- **Asynchronous Processing**: Implement message queues for handling high volumes of requests

## Security Considerations

### Data Protection

- Profile data is stored as JSON files and should be properly secured
- Consider encrypting sensitive profile information
- Implement access controls for the API endpoints

### API Security

- Add authentication to the API endpoints in production
- Use HTTPS for all API communications
- Implement rate limiting to prevent abuse

### Wati Integration Security

- Keep your Wati API key secure
- Use webhook signatures to verify incoming webhook requests
- Implement IP whitelisting for webhook endpoints

## Troubleshooting

### Common Issues

#### API Server Won't Start
- Check Python version (3.8+ required)
- Verify all dependencies are installed
- Ensure port 8000 is not in use

#### Wati Integration Fails
- Verify Wati API key is correct
- Check Wati API URL is accessible
- Ensure webhook URL is properly configured in Wati dashboard

#### Query Processing Issues
- Check profile data format is correct
- Verify query syntax is supported
- Look for specific error messages in logs

### Logging

The system uses Python's logging module for detailed logs:

- API server logs are output to the console
- Wati integration logs include webhook events and API calls
- Set log level to DEBUG for more detailed information

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgments

- The NLP component uses [spaCy](https://spacy.io/) for natural language processing
- API server built with [FastAPI](https://fastapi.tiangolo.com/)
- WhatsApp integration via [Wati API](https://docs.wati.io/)
- Docker support for containerized deployment
- Sample profiles created for demonstration purposes
