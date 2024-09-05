# Flask Application with Automated Deployment to Vultr

This repository contains a Flask application that integrates with the OpenAI and Gemini APIs. The application is automatically deployed to a Vultr server using GitHub Actions, providing an easy and consistent way to set up the application on new machines.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)
- [Testing Locally](#testing-locally)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This Flask application serves as a proxy to handle requests to the OpenAI and Gemini APIs. It includes routes for interacting with both APIs securely using API key validation. The GitHub Actions workflow automates the process of creating a Vultr server, setting up the environment, and deploying the application.

## Features

- Secure API key validation for requests.
- Integration with OpenAI and Gemini APIs.
- Automated deployment to Vultr using GitHub Actions.
- Logging for monitoring application behavior.

## Prerequisites

- **Python 3.x**: Ensure Python is installed on your local machine.
- **Vultr Account**: To deploy on Vultr, you need an API key and SSH key configured in your Vultr account.
- **GitHub Account**: For running GitHub Actions.

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment and install dependencies**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure environment variables**:

    Create a `.env` file in the root of the project with the necessary environment variables:

    ```dotenv
    OPENAI_API_KEY=your_openai_api_key
    GEMINI_API_KEY=your_gemini_api_key
    GEMINI_API_URL=your_gemini_api_url
    API_ACCESS_KEY=your_api_access_key
    DEFAULT_OPENAI_MODEL=your_default_openai_model
    DEFAULT_GEMINI_MODEL=your_default_gemini_model
    PORT=5000
    ```

## Deployment

Deployment to a Vultr server is automated using GitHub Actions:

1. **Set up GitHub Secrets**:
   
   Add the following secrets to your GitHub repository under **Settings > Secrets and variables > Actions**:
   
   - `VULTR_API_KEY`
   - `SSH_PRIVATE_KEY`
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - `GEMINI_API_URL`
   - `API_ACCESS_KEY`
   - `DEFAULT_OPENAI_MODEL`
   - `DEFAULT_GEMINI_MODEL`

2. **Trigger the GitHub Action**:

   The GitHub Actions workflow will automatically deploy the application when changes are pushed to the `main` branch or manually triggered via the Actions tab.

3. **Access the Application**:

   After the workflow completes, the application will be available at the IP address of the newly created Vultr server. Check the output of the workflow run for the server IP.

## Environment Variables

The application relies on several environment variables for configuration. Ensure all required variables are set in the `.env` file or as GitHub secrets for automated deployment.

## Testing Locally

To test the GitHub Actions workflow locally, you can use the `act` tool to simulate GitHub Actions on your local machine:

1. **Install Act**:

    ```bash
    brew install act  # macOS
    ```

    ```bash
    curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux
    ```

2. **Run the workflow locally**:

    ```bash
    act
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
