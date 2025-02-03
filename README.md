# RevUp-assessment

An API that facilitates a multi-agent conversational system to assist users in managing tasks, answering general questions, analyzing sentiments, and summarizing the conversation.

## Installation

```sh
# Clone the repository
git clone git@github.com:10kartik/RevUp-assessment.git
# Change directory to the repository
cd CV4Hire-Backend

# Create a virtual environment and install the dependencies
python3 -m venv my_virtual_environment
source my_virtual_environment/bin/activate
pip install -r requirements.txt
```

## Usage

- set the environment variable `FIREWORKS_API_KEY` to the API key for the [Fireworks API](https://fireworks.ai/account/api-keys). Edit sample.env for reference.

```sh
# Start the server
uvicorn server:app --host 127.0.0.1 --port 8000
```
