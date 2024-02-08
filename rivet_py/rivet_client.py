# rivet_client.py
# https://rivet.ironcladapp.com/docs/api-reference/getting-started-integration

import subprocess
import requests
from time import sleep, time
from platform import system
from os import getenv, environ, path
from dotenv import load_dotenv, find_dotenv


def is_server_running(url: str) -> bool:
    """ Check if the Node.js server is running by querying the health endpoint """
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def wait_for_server_to_start(url: str, timeout: int = 10) -> None:
    """ Wait for the server to be ready to accept connections """
    start_time = time()
    while time() - start_time < timeout:
        if is_server_running(url):
            return
        sleep(1)
    raise RuntimeError("Server did not start within the timeout period.")


def start_server(rivet_server_filepath: str, health_check_url: str) -> None:
    """ Starts the Node.js server `rivet_server.js` """
    print("Starting server...")
    if system() == "Windows":
        command = f'start cmd.exe /k node {rivet_server_filepath}'
    elif system() == "Linux":
        command = f'gnome-terminal -- node {rivet_server_filepath}'
    elif system() == "Darwin":  # macOS is identified as 'Darwin'
        command = f"""osascript -e 'tell app "Terminal" to do script "node {rivet_server_filepath}"'"""
    else:
        raise ValueError(f'Unsupported OS: {system()}')
    subprocess.run(command, shell=True)
    wait_for_server_to_start(health_check_url)
    print(f"Server running: {health_check_url}")


def send_request_to_server(request_payload: dict, server_url: str) -> dict:
    """ Send a POST request to the Node.js server """
    try:
        response = requests.post(server_url, json=request_payload)
        response.raise_for_status()
        output = response.json()
    except requests.HTTPError as err:
        output = err.response.json()  # {'error': 'Graph not found, and no main graph specified.'}
    except Exception as err:
        output = {'error': err}
    return output


def validate_environment(rivet_server_filepath: str, rivet_project_filepath: str) -> None:
    """ Raises KeyError if rivet_server.js, Rivet Project, or OPENAI_API_KEY does not exist """

    # Check if Rivet server file (`rivet_server.js`) exists
    if not path.exists(rivet_server_filepath):
        raise KeyError('rivet_server.js not found')

    # Check if Rivet project file (`*.rivet_py-project`) exists
    if not path.exists(rivet_project_filepath):
        raise KeyError('Rivet Project not found')

    # Check if OPENAI_API_KEY is in .env
    load_dotenv(find_dotenv())  # Load environment variables from .env
    if "OPENAI_API_KEY" not in environ:
        raise KeyError('missing OPENAI_API_KEY in .env')


def setup_rivet(rivet_project_filepath: str = r'.\projects\llm_io.rivet-project',
                rivet_server_filepath: str = r'.\rivet_server.js',
                port: int = 3000,
                ) -> None:
    """ Ensure the Rivet Node.js server is running.

    Args:
        rivet_server_filepath (str): Path to the Rivet Node.js server file ('rivet_server.js').
        rivet_project_filepath (str): Path to the Rivet project file ('*.rivet_py-project').
        port (int): The port number on which the server will listen (default is 3000).

    Returns:
        None: This function ensures the server is running but does not return a value.
    """

    # Set up temporary environment variables
    environ['RIVET_PROJECT_FILEPATH'] = rivet_project_filepath
    environ['PORT'] = str(port)

    # Validate environment
    validate_environment(rivet_server_filepath, rivet_project_filepath)

    # Ensure the Rivet Node.js server is running
    health_check_url = f'http://localhost:{port}/health'
    if is_server_running(health_check_url):
        print(f"Server was already running: {health_check_url}")
    else:
        start_server(rivet_server_filepath, health_check_url)


def call_rivet(inputs: dict = {'input': '3+3'},
               graph: str = 'Main Folder/Main Graph',
               ) -> dict:
    """ Call Rivet from Python using a Node.js server.

    Args:
        inputs (dict): Inputs to be passed to the Rivet graph, where the keys are the Graph Input nodes' IDs.
        graph (str): The name of the graph to be executed in Rivet ('Folder Name/Graph Name').

    Returns:
        dict: A dict with the cost and the outputs from the Rivet graph, where the keys are the Graph Output nodes' IDs,
        and where Split (parallel or sequential) values are in lists; or a dict with an error encountered.

        Example 1:
        {'male_scientist': {'type': 'string', 'value': 'He is Albert Einstein'},
        'dates': {'type': 'number[]', 'value': [1920, 1930, 1940]},
        'cost': {'type': 'number', 'value': 0.000156}}

        Example 2:
        {'error': 'Graph not found, and no main graph specified.'}
    """

    # Define the request payload
    request_payload = {
        'options': {'graph': graph, 'inputs': inputs, 'openAiKey': getenv('OPENAI_API_KEY')}
    }

    # Send a POST request to the Node.js server
    output = send_request_to_server(request_payload, server_url=f'http://localhost:{getenv("PORT")}/run-graph')
    return output


if __name__ == '__main__':
    setup_rivet(r'.\projects\llm_io.rivet-project')
    result = call_rivet(inputs={'input': 'name a female scientist'},
                        graph="Main Folder/Main Graph",
                        )
    print(result)

