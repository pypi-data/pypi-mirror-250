import requests
import json
import time
import boto3
import os
import base64
import binascii
from base64 import b64encode
from nacl import encoding, public
import zipfile
import logging

from validation import IAMRoleValidator
from configs import load_cfg

# declare global variable
cfg = load_cfg()
logger = logging.getLogger(__name__)


def get_stack_outputs(stack_name, region, aws_access_key_id, aws_secret_access_key, aws_session_token):
    """
    Returns the EMR cluster ID.

            Parameters:
                    stack_name (str): The name of the cloudformation stack
                    region (str): The aws region from where the output has to be fetched
                    aws_access_key_id (str): AWS Temp Credentials: Access Key ID
                    aws_secret_access_key (str): AWS Temp Credentials: Secret Access Key
                    aws_session_token (str): AWS Temp Credentials: Session Token

            Returns:
                    EMR Cluster ID (str): It returns the output of the stack i.e.
                    EMR Cluster ID to the trigger_workflow function
    """
    client = boto3.client('cloudformation', region_name=region, aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    try:
        stack = client.describe_stacks(StackName=stack_name)
        outputs = stack['Stacks'][0]['Outputs']

        return {output['OutputKey']: output['OutputValue'] for output in outputs}

    except client.exceptions.ClientError as e:
        print(f"Error getting stack outputs: {e}")
        return {}


def fetch_stack_status_with_retry(stack_name, aws_region, aws_access_key_id, aws_secret_access_key, aws_session_token,
                                  max_retries=15, retry_delay=60, initial_delay=120):
    """
    Returns the EMR cluster ID.

            Parameters:
                    stack_name (str): The name of the cloudformation stack
                    aws_region (str): The aws region from where the output has to be fetched
                    aws_access_key_id (str): AWS Temp Credentials: Access Key ID
                    aws_secret_access_key (str): AWS Temp Credentials: Secret Access Key
                    aws_session_token (str): AWS Temp Credentials: Session Token
                    max_retries (int): Max retries to trigger the AWS to check if the stack deployment is complete
                    retry_delay (int): Delay seconds between each retry
                    initial_delay (int): The initial delay in seconds before checking on the stack creation

            Returns:
                    If the stack creation has been successful or not
    """
    # Initial waiting period before starting retries
    print(f"Waiting for stack {stack_name} to be created...")
    time.sleep(initial_delay)
    client = boto3.client('cloudformation', region_name=aws_region, aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    # Retry fetching the EMR Cluster ID with a delay in case of 404 errors
    for retry_count in range(max_retries):
        try:
            stack_resources = client.list_stack_resources(StackName=stack_name)
            stack_resources = stack_resources['StackResourceSummaries']
            print("Resources:")
            for resource in stack_resources:
                print("| {} | {} | {} | {} |".format(resource['LogicalResourceId'], resource['PhysicalResourceId'],
                                                     resource['ResourceType'], resource['ResourceStatus']))

            stack = client.describe_stacks(StackName=stack_name)
            status = stack['Stacks'][0]['StackStatus']

            if status.endswith('COMPLETE'):
                print(f"Stack {stack_name} creation complete.")
                return True

            elif status.endswith('ROLLBACK'):
                print(f"Stack {stack_name} creation failed.")
                return False

        except client.exceptions.ClientError as e:
            if 'does not exist' in str(e):
                pass  # Stack doesn't exist yet, continue waiting
            else:
                raise

        print(
            f'Retry {retry_count + 1}/{max_retries}. EMR Cluster creation in progress, waiting {retry_delay}'
            f' seconds before fetching more details...')
        time.sleep(retry_delay)

    print(f'Exceeded maximum retries. Failed to retrieve EMR Cluster ID. Please check the logs for more information.')
    return None


def get_latest_workflow_run_id(organization, repository, workflow_name, token):
    """
    Retrieve the ID of the latest run for a specified GitHub Actions workflow.

    Parameters:
    - organization (str): The GitHub organization or username.
    - repository (str): The name of the GitHub repository.
    - workflow_name (str): The name of the GitHub Actions workflow.
    - token (str): Personal access token for authentication.

    Returns:
    - int or None: The ID of the latest workflow run if available, or None if no runs exist or an error occurs.

    This function sends a GET request to the GitHub API to fetch information about the workflow runs
    for the specified repository and workflow. It extracts the ID of the latest run and returns it.
    If there are no runs or if an error occurs during the API request, the function returns None.

    Note: Make sure the provided token has the necessary permissions to access workflow run information.
    """

    url = f'https://api.github.com/repos/{organization}/{repository}/actions/workflows/{workflow_name}/runs'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        if data['workflow_runs']:
            # Assuming the first run is the latest one
            latest_run = data['workflow_runs'][0]
            return latest_run['id']
        else:
            return None
    else:
        print(f'Error: {response.status_code}, {response.text}')
        return None


def get_workflow_run_details(owner, repo, run_id, github_token):
    """
    Retrieve detailed information about a specific GitHub Actions workflow run.

    Parameters:
    - owner (str): The owner of the GitHub repository (organization or username).
    - repo (str): The name of the GitHub repository.
    - run_id (int): The ID of the GitHub Actions workflow run to retrieve details for.
    - github_token (str): Personal access token for authentication.

    Returns:
    - dict or str: A dictionary containing detailed information about the workflow run if successful,
      or an error message string if the API request fails.

    This function sends a GET request to the GitHub API to fetch detailed information about the specified
    workflow run in the given repository. The information includes metadata, status, conclusion, and other details.
    If the request is successful (status code 200), the function returns the data as a dictionary.
    If an error occurs during the API request, the function returns an error message string.

    Note: Ensure that the provided token has the necessary permissions to access workflow run details.
    """

    url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}'
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f'Error: {response.status_code}, {response.text}'


def print_step_logs(organization, repository, workflow_run_id, token):
    """
    Print and analyze the details of each step in a GitHub Actions workflow run.

    Parameters:
    - organization (str): The GitHub organization or username.
    - repository (str): The name of the GitHub repository.
    - workflow_run_id (int): The ID of the GitHub Actions workflow run to analyze.
    - token (str): Personal access token for authentication.

    Returns:
    - str: A message indicating the status of the workflow run. If the workflow is successful,
      the message is "workflow successfully ran". If there are failed steps, it provides details
      about the failure and advises checking downloaded logs for more information.

    This function retrieves information about the jobs and steps in a GitHub Actions workflow run.
    It prints the status of each step and, if any step fails, provides details about the failure
    along with a message suggesting checking the downloaded logs for more information.

    Note: Ensure that the provided token has the necessary permissions to access workflow run details
    and annotations.
    """

    jobs_url = f'https://api.github.com/repos/{organization}/{repository}/actions/runs/{workflow_run_id}/jobs'

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(jobs_url, headers=headers, verify=False)
    print(f"job-response-code:{response.status_code}")

    if response.status_code == 200:
        jobs_data = response.json().get('jobs', [])
        for job in jobs_data:
            job_name = job.get('name', '')
            job_status = job.get('conclusion', '')

            step_failure_list = []
            for step in job["steps"]:
                step_name = step["name"]
                step_status = step["conclusion"]
                print(f" Step : {step_name} :{step_status}")
                if step_status == "failure":
                    step_failure_list.append(step_name)

                    failure_step = step_name
            check_run_url = job["check_run_url"]
            get_failure_msgs_details = requests.get(check_run_url, headers=headers, verify=False)
            annotation_url = get_failure_msgs_details.json()["output"]["annotations_url"]
            if len(step_failure_list) != 0:
                failure_response = requests.get(annotation_url, headers=headers, verify=False)
                workflow_message = failure_response.json()[0]["message"]
                print(f"Github workflow failed at {failure_step} step  with error message : {workflow_message}. "
                      f"Check downloaded logs for more details")
                get_workflow_run_logs(organization, repository, workflow_run_id, token)
                return workflow_message
            else:
                workflow_message = "success"
                print("workflow successfully ran")
                return workflow_message

    else:
        print(f'Failed to fetch jobs. Status code: {response.status_code}')


def get_workflow_run_logs(owner, repo, run_id, token):
    """
    Download and extract the logs of a specific GitHub Actions workflow run.

    Parameters:
    - owner (str): The owner of the GitHub repository (organization or username).
    - repo (str): The name of the GitHub repository.
    - run_id (int): The ID of the GitHub Actions workflow run to retrieve logs for.
    - token (str): Personal access token for authentication.

    Returns:
    - int or None: The HTTP status code indicating the success of the operation (200 for success),
      or None if an error occurs during the API request.

    This function sends a GET request to the GitHub API to fetch the logs of the specified
    GitHub Actions workflow run in the given repository. If the request is successful (status code 200),
    the function downloads the logs as a zip file, extracts the contents, and returns the HTTP status code.
    If an error occurs during the API request, the function prints an error message and returns None.

    Note: Ensure that the provided token has the necessary permissions to access workflow run logs.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/logs"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        zip_file_path = os.path.join('downloaded_file.zip')
        with open(zip_file_path, 'wb') as f:
            f.write(response.content)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall()
        return response.status_code
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def create_github_secret(key_id, key, owner, repo, token, secret_name, secret_value):
    url = f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/{secret_name}'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'encrypted_value': encrypt(key, secret_value),
        'key_id': key_id
    }

    response = requests.put(url, json=data, headers=headers, verify=False)

    if response.status_code == 201:
        print(f"Secret '{secret_name}' added successfully.")
    elif response.status_code == 204:
        print(f"Secret '{secret_name}' updated successfully.")
    else:
        print(f"Failed to add/update secret '{secret_name}'. Status code: {response.status_code}")
        print(response.text)


def get_github_public_key(owner, repo, token):
    url = f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        key_data = response.json()
        key_id = key_data['key_id']
        key = key_data['key']

        # If the key is not in PEM format, try to decode it
        try:
            decoded_key = base64.b64decode(key)
            encoded_key = base64.b64encode(decoded_key).decode('utf-8')
            return key_id, encoded_key
        except binascii.Error as e:
            print(f"Failed to decode key: {e}")
            return None, None
    else:
        print(f"Failed, Status code: {response.status_code}")
        print(response.text)
        return None, None


def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def trigger_workflow(organization, repository, workflow_name, event_type, aws_region, token, inputs=None):
    """
    Triggers the GitHub actions to create the AWS infrastructure for Luminex.

            Parameters:
                    organization (str): The name of the organization which the Repo belongs to
                    repository (str): The name of the Repo
                    workflow_name (str): The GitHub action that needs to be triggered to deploy the infra
                    event_type (str): The type of the event to trigger
                    aws_region (str): The aws region from where the emr creation status has to be fetched
                    token (str): The personal access token need to trigger the GitHub action
                    inputs (dict): The inputs variables that needs to be passed to the GitHub action

            Returns:
                    Returns the EMR Cluster ID
    """

    url = f'https://api.github.com/repos/{organization}/{repository}/dispatches'
    stack_name = inputs['stack-name']
    aws_access_key_id = inputs['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = inputs['AWS_SECRET_ACCESS_KEY']
    aws_session_token = inputs['AWS_SESSION_TOKEN']
    headers = {
        'Accept': 'application/vnd.github.everest-preview+json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    payload = {
        'event_type': event_type,
        'client_payload': {
            'workflow': workflow_name,
            'inputs': inputs or {},
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

    if response.status_code == 204:
        print(f'Response status code: {response.status_code}, Workflow triggered successfully.Fetching workflow run id')
        time.sleep(15)
        latest_run_id = get_latest_workflow_run_id(organization, repository, workflow_name, token)
        if latest_run_id is not None:
            print(f'Latest Workflow Run ID: {latest_run_id}. Getting Workflow status step by step')
            time.sleep(20)
            workflow_run_details = get_workflow_run_details(organization, repository, latest_run_id, token)
            if workflow_run_details is not None:
                conclusion = workflow_run_details['conclusion']
                print(f'Workflow status : {conclusion}')

                if 'conclusion' in workflow_run_details:
                    failure_reason = print_step_logs(organization, repository, latest_run_id, token)
                    if failure_reason == "success":
                        if fetch_stack_status_with_retry(stack_name, aws_region, aws_access_key_id, aws_secret_access_key,
                                                         aws_session_token):
                            outputs = get_stack_outputs(stack_name, aws_region, aws_access_key_id, aws_secret_access_key, aws_session_token)
                            for key, value in outputs.items():
                                print(f"Infra has been set.{key}: {value} ")
                        else:
                            print("Failed to create the stack.")

                        return failure_reason

        else:
            print('Failed to retrieve the latest Workflow Run ID.')
            return None
    else:
        print(
            f'Failed to trigger the GitHub Actions workflow. Status code: {response.status_code}, '
            f'Content: {response.text}')
        return None


def run_infra(pat, stack_name):
    """
    Retrieves values from different sources and finally triggers the function to run the GitHub action

            Parameters:
                    pat (str): Personal Access token to trigger GitHub action.
                    stack_name (str): Name of the stack that manages Luminex infra resources.
                    ENV -  AWS_ACCESS_KEY_ID (str): AWS Temp Credentials: Access Key ID
                    ENV -  AWS_SECRET_ACCESS_KEY (str): AWS Temp Credentials: Secret Access Key
                    ENV - AWS_SESSION_TOKEN (str): AWS Temp Credentials: Session Token

            Returns:
                    Calls the trigger workflow function with required parameters (From config file: organization_name,
                    repository_name, workflow_name, event_type, From user: personal_access_token, workflow_inputs)
    """
    # Access AWS config
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_session_token = os.environ.get('AWS_SESSION_TOKEN')

    if not aws_access_key_id or not aws_secret_access_key or not aws_session_token:
        print("Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN environment variables.")
        return

    # Validation logic
    permissions_validator = IAMRoleValidator(cfg)
    permissions_validator.validate_roles()

    organization_name = cfg["INFRA"]["GITHUB_ORGANIZATION"]
    repository_name = cfg["INFRA"]["GITHUB_REPOSITORY"]
    workflow_name = cfg["INFRA"]["GITHUB_WORKFLOW"]
    event_type = cfg["INFRA"]["GITHUB_EVENT_TYPE"]
    aws_region = cfg["AWS"]["REGION"]
    personal_access_token = pat

    workflow_inputs = {
        'AWS_ACCESS_KEY_ID': aws_access_key_id,
        'AWS_SECRET_ACCESS_KEY': aws_secret_access_key,
        'AWS_SESSION_TOKEN': aws_session_token
    }

    for secret_name, secret_value in workflow_inputs.items():
        key_id, key = get_github_public_key(organization_name, repository_name, personal_access_token)
        create_github_secret(key_id, key, organization_name, repository_name, personal_access_token,
                             secret_name, secret_value)

    workflow_inputs['stack-name'] = stack_name
    trigger_workflow(organization_name, repository_name, workflow_name, event_type, aws_region, personal_access_token,
                     workflow_inputs)
