# LinkedIn Profile Query Bot - Project Structure

This document explains the project structure and how all components fit together.

## Overview

The LinkedIn Profile Query Bot consists of several Python modules that work together to provide a complete system for processing queries about LinkedIn profiles via WhatsApp.

## File Structure

```
linkedin-profile-bot/
├── main.py                 # Main application entry point
├── profile_scraper.py      # LinkedIn profile data capture
├── query_processor.py      # NLP query processor
├── api_server.py           # FastAPI server
├── wati_integration.py     # Wati API integration
├── start.sh                # Linux/Mac startup script
├── start.bat               # Windows startup script
├── profiles/               # Directory for profile data
│   └── john-smith.json     # Example profile data
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment configuration
├── config.json.example     # Example JSON configuration
├── README.md               # Project documentation
└── DEPLOYMENT.md           # Deployment guide
```

## Component Interaction

Here's how the components interact with each other:

1. **main.py**: The entry point that loads configuration and starts the API server and/or Wati integration.

2. **profile_scraper.py**: Provides functions for capturing and storing LinkedIn profile data. Used primarily when adding new profiles to the system.

3. **query_processor.py**: Contains the NLP logic for processing queries about LinkedIn profiles. It:
   - Extracts profile names from queries
   - Identifies query categories (education, experience, etc.)
   - Generates appropriate responses

4. **api_server.py**: Provides the FastAPI server that:
   - Processes queries via HTTP endpoints
   - Handles Wati webhooks
   - Manages profile data

5. **wati_integration.py**: Handles communication with the Wati API, including:
   - Setting up webhooks
   - Sending messages to WhatsApp users
   - Processing incoming messages

## Data Flow

1. **User Query Flow**:
   - User sends a message via WhatsApp
   - Wati forwards the message to the bot's webhook endpoint
   - The webhook handler extracts the message text
   - The query processor analyzes the query
   - The appropriate profile data is retrieved
   - A response is generated and sent back to the user via Wati

2. **Profile Data Flow**:
   - Profile data is captured using the profile scraper
   - Data is stored as JSON files in the profiles directory
   - The API server provides endpoints for adding and retrieving profiles
   - The query processor accesses profile data when processing queries

## Configuration

Configuration can be provided in three ways:

1. **Environment Variables**: Set in the shell or via a .env file
2. **JSON Configuration**: Via config.json file
3. **Command Line Arguments**: For specifying run mode

The main.py script handles loading and merging configuration from these sources.

## Running the Application

The application can be run in three modes:

1. **API Mode**: Only runs the API server
   ```
   python main.py --mode api
   ```

2. **Wati Mode**: Only runs the Wati integration
   ```
   python main.py --mode wati
   ```

3. **All Mode (Default)**: Runs both the API server and Wati integration
   ```
   python main.py --mode all
   ```

For convenience, the start.sh (Linux/Mac) and start.bat (Windows) scripts are provided to set up the environment and run the application.

## Docker Deployment

For containerized deployment, the Dockerfile and docker-compose.yml files are provided. To run with Docker Compose:

```
docker-compose up -d
```

This will start both the API server and Wati integration in separate containers.
