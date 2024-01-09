"""
# QALITA (c) COPYRIGHT 2023 - ALL RIGHTS RESERVED -
"""
import os
import sys
import time
import random
import string
import tarfile
import json
import click
import semver
import croniter
from shutil import copy2
from datetime import datetime
from tabulate import tabulate
import glob

from qalita.cli import pass_config
from qalita.internal.utils import logger, get_version
from qalita.internal.request import send_request, send_api_request
from qalita.commands.pack import run_pack


@click.group()
@click.option(
    "-n",
    "--name",
    help="The name of the agent, it will be used to identify the agent in the qalita platform",
    envvar="QALITA_AGENT_NAME",
)
@click.option(
    "-m",
    "--mode",
    type=click.Choice(["job", "worker"], case_sensitive=False),
    help="The mode of the agent, <worker/job> if you run the agent in worker mode, the agent will loop until it gets a job to do, in job mode it will immediately do a job",
    envvar="QALITA_AGENT_MODE",
)
@click.option(
    "-t",
    "--token",
    help="The API token from the qalita platform, it is user scoped. Make sure you have at least the Data Engineer role to have the ability to register agents.",
    envvar="QALITA_AGENT_TOKEN",
)
@click.option(
    "-u",
    "--url",
    help="The URL to the qalita backend the agent have to register exemple : http://backend:3080/api/v1",
    envvar="QALITA_AGENT_ENDPOINT",
)
@pass_config
def agent(config, name, mode, token, url):
    """Manage Qalita Platform Agents"""

    all_check_pass = True

    # Get QALITA_HOME from the environment or default to ~/.qalita
    qalita_home = os.environ.get("QALITA_HOME", os.path.expanduser("~/.qalita"))

    # Build the file pattern to search for .env-agent-xxxxx files within QALITA_HOME
    file_pattern = os.path.join(qalita_home, f".env-{name}" if name else ".env-*")

    # Check if the name is provided via command line and prepend "agent-" if needed
    if name:
        name = f"{name}"

    env_files = glob.glob(file_pattern)

    if env_files:
        # Read the first found file
        env_file = env_files[0]
        logger.info(f"Found existing agent file: {env_file}")

        # Load values from the file only if the corresponding command-line option is not provided
        with open(env_file, "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                key = key.lower().replace("qalita_agent_", "")
                if key == "name" and not name:
                    name = value
                elif key == "mode" and not mode:
                    mode = value
                elif key == "token" and not token:
                    token = value
                elif key == "endpoint" and not url:
                    url = value

    # Validation of required options
    if not name:
        logger.error("Error: Agent name is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_AGENT_NAME='agent-1'")
        logger.info("\tor add the name as a commandline argument : ")
        logger.info("\t\tqalita agent --name 'agent-1'")
        logger.info(
            "\tthe prefered way is to create a file '.env-file' with the values : "
        )
        logger.info("\t\tQALITA_AGENT_NAME=agent-1")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-file)")
        all_check_pass = False
    if not mode:
        logger.error("Error: Agent Mode is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_AGENT_MODE='job'")
        logger.info("\tor add the mode as a commandline argument : ")
        logger.info("\t\tqalita agent --mode 'job'")
        logger.info(
            "\tthe prefered way is to create a file '.env-file' with the values : "
        )
        logger.info("\t\tQALITA_AGENT_MODE=job")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-file)")
        all_check_pass = False
    if not token:
        logger.error("Error: AGENT_TOKEN is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_AGENT_TOKEN='<your_api_token>'")
        logger.info("\tor add the token as a commandline argument : ")
        logger.info("\t\tqalita agent --token '<your_api_token>'")
        logger.info(
            "\tthe prefered way is to create a file '.env-file' with the values : "
        )
        logger.info("\t\tQALITA_AGENT_TOKEN=<your_api_token>")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-file)")
        all_check_pass = False
    if not url:
        logger.error("Error: AGENT_ENDPOINT is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_AGENT_ENDPOINT='http://localhost:3080/api/v1'")
        logger.info("\tor add the url as a commandline argument : ")
        logger.info("\t\tqalita agent --url 'agent-1'")
        logger.info(
            "\tthe prefered way is to create a file '.env-file' with the values : "
        )
        logger.info("\t\tQALITA_AGENT_ENDPOINT=http://localhost:3080/api/v1")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-file)")
        all_check_pass = False
    if all_check_pass:
        config.name = name
        config.mode = mode
        config.token = token
        config.url = url
    else:
        return


@agent.command()
@pass_config
def info(config):
    """Display Information about the agent"""
    data = config.load_agent_config()

    print("------------- Agent information -------------")
    print(f"Name : {config.name}")
    print(f"Mode : {config.mode}")
    print(f"Backend URL : {config.url}")
    print(f"Registered Agent Id : {data['context']['remote']['id']}")


@pass_config
def send_alive(config, config_file, mode="", status="online"):
    if mode == "":
        mode = config.mode

    """Send a keep alive to the backend"""
    r = send_api_request(
        request=f'/agents/{config_file["context"]["remote"]["id"]}/alive?name={config_file["context"]["local"]["name"]}&mode={mode}&status={status}',
        mode="put",
    )
    if r.status_code != 200:
        logger.warning(f"Agent failed to send alive {r.status_code} - {r.text}")


@pass_config
def authenticate(config):
    """Authenticate the agent to the Qalita Platform"""

    r = send_request(request=f"{config.url}/users/me", mode="get")

    if r.status_code == 200:
        logger.success("Agent Authenticated")
        config_json = {}
        config_json["user"] = r.json()
        try:
            config_json["context"]["local"] = config.json()
        except KeyError:
            config_json["context"] = {}
            config_json["context"]["local"] = config.json()

        config.save_agent_config(config_json)
    else:
        logger.error(
            f"Agent can't authenticate - HTTP Code : {r.status_code} - {r.text}"
        )
        logger.error(
            "Make sure you have generated an API TOKEN from the qalita platform backend or web app"
        )
        sys.exit(1)

    r = send_api_request(request=f"/agents/?name={config.name}", mode="get")

    if r.status_code == 200:
        logger.success("Agent Registered")
    elif r.status_code == 404:
        logger.info("Agent not Registered")
        try:
            logger.info("Registering agent...")
            r = send_api_request(
                request=f"/agents/register",
                mode="post",
                query_params={
                    "name": {config.name},
                    "mode": {config.mode},
                    "status": "online",
                },
            )
            if r.status_code == 201:
                logger.success("Agent Registered")
            else:
                logger.error(
                    f"Agent can't register - HTTP Code : {r.status_code} - {r.text}"
                )
        except Exception as exception:
            logger.error(f"Agent can't communicate with backend : {exception}")
            sys.exit(1)
    else:
        logger.error(
            f"Agent can't authenticate - HTTP Code : {r.status_code} - {r.text}"
        )
        logger.error(
            "Make sure you have generated an API TOKEN from the qalita platform backend or web app"
        )
        sys.exit(1)

    config_json = config.load_agent_config()
    config_json["context"]["remote"] = r.json()
    config.save_agent_config(config_json)

    r = send_api_request(request=f"/partners/1", mode="get")

    if r.status_code == 404:
        logger.info("No registry")
        sys.exit(1)
    elif r.status_code == 200:
        logger.success("Agent Fetched Registry")
    else:
        logger.error(
            f"Agent can't fetch registry - HTTP Code : {r.status_code} - {r.text}"
        )
        logger.error(
            "Make sure you have generated an API TOKEN from the qalita platform backend or web app"
        )
        sys.exit(1)

    partner_data = r.json()
    config_json = config.load_agent_config()
    config_json["registries"] = partner_data["registries"]
    config.save_agent_config(config_json)


@agent.command()
@pass_config
def login(config):
    """
    Register the agent to the Qalita Platform
    """
    if config.verbose:
        logger.info("Verbose mode enabled")

    # check API endpoint version
    r = send_request(request=f"{config.url}/version", mode="get")
    if r.status_code == 200:
        logger.info(f"Qalita Platform Version : {r.json()['version']}")
        logger.info(f"Qalita CLI Version : {get_version()}")
        logger.info(
            "Make sure you are using compatible versions for the platform and the cli,\n\t\t\t\t\t\t\t\t\t > check compatibility matrix on the documentation <"
        )
    authenticate()
    agent_conf = config.load_agent_config()
    send_alive(config_file=agent_conf)


@agent.command()
@pass_config
@click.option(
    "-s",
    "--source-id",
    help="The source ID to run the job against, to get the source ID, run qalita source list",
    envvar="QALITA_AGENT_JOB_SOURCE",
)
@click.option(
    "-sv",
    "--source-version",
    help="The source Version to run the job against, to get the source version, run qalita source -s <source_id> versions, default to latest",
    envvar="QALITA_AGENT_JOB_SOURCE_VERSION",
)
@click.option(
    "-s",
    "--target-id",
    help="The target ID to run the job against, to get the target ID, run qalita source list",
    envvar="QALITA_AGENT_JOB_SOURCE",
)
@click.option(
    "-sv",
    "--target-version",
    help="The target Version to run the job against, to get the target version, run qalita source -s <target_id> versions, default to latest",
    envvar="QALITA_AGENT_JOB_SOURCE_VERSION",
)
@click.option(
    "-p",
    "--pack-id",
    help="The pack ID to run the job against, to get the pack ID, run qalita pack list",
    envvar="QALITA_AGENT_JOB_PACK",
)
@click.option(
    "-pv",
    "--pack-version",
    help="The pack Version to run the job against, to get the pack version, run qalita pack -p <pack_id> versions, default to latest",
    envvar="QALITA_AGENT_JOB_PACK_VERSION",
)
def run(
    config, source_id, source_version, target_id, target_version, pack_id, pack_version
):
    """Runs de agent"""
    # Pre-checks
    if config.mode == "job":
        if source_id is None:
            logger.error("Agent can't run job without source")
            logger.error(
                "Please configure a source with --source or -s or QALITA_AGENT_JOB_SOURCE"
            )
            logger.error("To get the source ID, run qalita source list")
            sys.exit(1)
        if pack_id is None:
            logger.error("Agent can't run job without pack")
            logger.error(
                "Please configure a pack with --pack or -p or QALITA_AGENT_JOB_PACK"
            )
            logger.error("To get the pack ID, run qalita pack list")
            sys.exit(1)
    logger.info("------------- Agent Authenticate -------------")
    authenticate()
    logger.info("------------- Agent Run -------------")
    agent_conf = config.load_agent_config()
    logger.info(f"Agent ID : {agent_conf['context']['remote']['id']}")
    logger.info(f"Agent Mode : {config.mode}")

    # Create a temp folder named "agent_run_temp" if it doesn't already exist
    agent_run_temp_path = config.get_agent_run_path()
    if not os.path.exists(agent_run_temp_path):
        os.makedirs(agent_run_temp_path)

    last_alive_time = time.time()

    if config.mode == "job":
        job_run(source_id, source_version, pack_id, pack_version)
    elif config.mode == "worker":
        try:
            logger.info(f"Worker Start at {time.strftime('%X %d-%m-%Y %Z')}")
            agent_start_datetime = datetime.now()
            send_alive(config_file=agent_conf)
            while True:
                current_time = time.time()
                # If it's been more than 10 seconds since the last alive signal, send another one
                if current_time - last_alive_time >= 10:
                    send_alive(config_file=agent_conf)
                    last_alive_time = current_time

                # check routines before checking jobs
                check_routines(config, agent_start_datetime)

                check_job = send_api_request(
                    request=f'/agents/{agent_conf["context"]["remote"]["id"]}/jobs/next',
                    mode="get",
                )
                if check_job.status_code == 200:
                    jobs = check_job.json()
                    for job in jobs:
                        if job["source_version"] != None:
                            source_version = job["source_version"]["id"]
                        else:
                            source_version = None
                        if job["pack_version"] != None:
                            pack_version = job["pack_version"]["id"]
                        else:
                            pack_version = None
                        job_run(
                            job["source"]["id"],
                            source_version,
                            job["target"]["id"] if job.get("target") else None,
                            target_version,
                            job["pack"]["id"],
                            pack_version,
                            job=job,
                        )
                    time.sleep(1)
                else:
                    logger.warning("Failed to fetch job, retrying in 60 seconds...")
                    time.sleep(60)
        except KeyboardInterrupt:
            logger.warning("KILLSIG detected. Gracefully exiting the program.")
            logger.error("Set Agent OFFLINE...")
            send_alive(config_file=agent_conf, status="offline")
            logger.error("Exit")
    else:
        logger.error("Agent mode not supported : <worker/job>")
        sys.exit(1)


@pass_config
def pull_pack(config, pack_id, pack_version=None):
    logger.info("------------- Pack Pull -------------")
    # Fetch the pack data from api
    response_pack = send_api_request(f"/packs/{pack_id}", "get")
    if response_pack.status_code == 200:
        # The request was successful
        response_pack = response_pack.json()
    else:
        # The request failed
        logger.error(f"Failed to fetch pack info: {response_pack.text}")
        sys.exit(1)

    if pack_version is None:
        # Convert the 'sem_ver_id' to tuple for easy comparison
        for version in response_pack["versions"]:
            version["sem_ver_id"] = tuple(map(int, version["sem_ver_id"].split(".")))

        # Sort the versions in descending order
        response_pack["versions"].sort(key=lambda v: v["sem_ver_id"], reverse=True)

        # Get the highest version
        highest_version = response_pack["versions"][0]

        # Convert the 'sem_ver_id' back to string
        highest_version["sem_ver_id"] = ".".join(
            map(str, highest_version["sem_ver_id"])
        )

        logger.info(
            f"Pack version not specified, Latest pack version is {highest_version['sem_ver_id']}"
        )
        pack_version = highest_version["sem_ver_id"]
        pack_asset_id = highest_version["asset_id"]

    # Filter the version list for the matching version
    matching_versions = [
        v for v in response_pack["versions"] if v["sem_ver_id"] == pack_version
    ]

    if not matching_versions:
        logger.error(f"Version {pack_version} not found in pack {pack_id}")
        sys.exit(1)
    else:
        pack_asset_id = matching_versions[0]["asset_id"]

    # Get the URL from the matching version
    r = send_api_request(f"/assets/{pack_asset_id}", "get")
    pack_url = ""
    if r.status_code == 200:
        pack_url = r.json()["url"]
    else:
        logger.error(f"Failed to fetch pack asset: {r.text}")

    agent_run_temp_path = config.get_agent_run_path()
    # Système de caching, on regarde si le pack est déjà présent dans le cache sinon on le télécharge
    file_name = pack_url.split("/")[-1]
    bucket_name = pack_url.split("/")[3]
    s3_folder = "/".join(pack_url.split("/")[4:-1])
    local_path = f"{agent_run_temp_path}/{bucket_name}/{s3_folder}/{file_name}"

    if os.path.exists(local_path):
        logger.info(f"Using CACHED Pack at : {local_path}")
        return local_path, pack_version
    if not os.path.exists(f"{agent_run_temp_path}/{bucket_name}/{s3_folder}"):
        os.makedirs(f"{agent_run_temp_path}/{bucket_name}/{s3_folder}")

    # Fetch the pack from api
    response = send_api_request(f"/assets/{pack_asset_id}/fetch", "get")

    if response.status_code == 200:
        # The request was successful
        with open(local_path, "wb") as file:
            file.write(response.content)
        logger.info(f"Pack fetched successfully")
        return local_path, pack_version
    else:
        logger.error(f"Failed to fetch pack : {response.text}")
        sys.exit(1)


@pass_config
def job_run(
    config,
    source_id,
    source_version_id,
    target_id,
    target_version_id,
    pack_id,
    pack_version_id,
    job={},
):
    logger.info("------------- Job Run -------------")
    start_time = datetime.now()
    logger.info(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Source {source_id}:{source_version_id}")
    if target_id:
        logger.info(f"Target {target_id}:{target_version_id}")
    logger.info(f"Pack {pack_id}:{pack_version_id}")

    """Runs a job"""
    agent_conf = config.load_agent_config()
    send_alive(config_file=agent_conf, mode="job", status="starting")

    # Get Source Version & Version ID
    # if source_version_id is None:
    # Fetch the source data from api
    response_source = send_api_request(f"/sources/{source_id}", "get")
    if response_source.status_code == 200:
        data = response_source.json()
        versions = data.get("versions", [])
        if versions:
            latest_version = max(
                versions, key=lambda v: semver.parse_version_info(v["sem_ver_id"])
            )
            source_version = latest_version["sem_ver_id"]
            source_version_id = latest_version["id"]

    logger.info(
        f"Source version not specified, Latest source version is {source_version}"
    )

    # Get pack Version & Version ID
    # if pack_version_id is None:
    # Fetch the pack data from api
    response_pack = send_api_request(f"/packs/{pack_id}", "get")
    if response_pack.status_code == 200:
        data = response_pack.json()
        versions = data.get("versions", [])
        if versions:
            latest_version = max(
                versions, key=lambda v: semver.parse_version_info(v["sem_ver_id"])
            )
            pack_version = latest_version["sem_ver_id"]
            pack_version_id = latest_version["id"]
    elif response_pack.status_code == 404:
        logger.error(f"No pack found with id {pack_id}")
        sys.exit(1)

    logger.info(f"pack version not specified, Latest pack version is {pack_version}")

    # Get Pack
    pack_file_path, pack_version = pull_pack(pack_id, pack_version)
    pack_folder = f"{pack_file_path.split('/')[-1].split('.')[0]}_pack"

    # Create a sub folder named with the current datetime and random generated seed
    datetime_string = start_time.strftime("%Y%m%d%H%M%S")
    random_seed = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(5)
    )

    agent_run_temp_path = config.get_agent_run_path()
    temp_folder_name = f"{agent_run_temp_path}/{datetime_string}_{random_seed}"
    os.makedirs(temp_folder_name)

    # Copy the downloaded pack to the temp folder
    copy2(pack_file_path, temp_folder_name)

    # Uncompress the pack
    with tarfile.open(
        os.path.join(temp_folder_name, pack_file_path.split("/")[-1]), "r:gz"
    ) as tar:
        # Validate members
        safe_members = []
        for member in tar.getmembers():
            # Skip if not a file
            if not member.isfile():
                continue
            # Check for path traversal attack
            if member.name.startswith(("/", "..")):
                logger.warning(
                    f"Skipping potentially dangerous tar file member {member.name}"
                )
                continue
            safe_members.append(member)
        # Assert that all members are safe
        assert all(
            not member.name.startswith(("/", "..")) for member in safe_members
        ), "Unsafe tar file member detected"
        # Extract safe members
        tar.extractall(path=temp_folder_name, members=safe_members)
        # Delete the compressed pack
        os.remove(os.path.join(temp_folder_name, pack_file_path.split("/")[-1]))

    # Load the source configuration
    source_conf = config.load_source_config()

    # Find the matching source_id
    matching_sources = [
        s for s in source_conf["sources"] if str(s.get("id")) == str(source_id)
    ]

    if matching_sources:
        # If there is a match, get the first one (there should only be one match anyway)
        source = matching_sources[0]
    else:
        logger.error(f"No source found with id {source_id}")
        sys.exit(1)

    # save the source conf as a json file in the temp folder
    with open(
        os.path.join(temp_folder_name, pack_folder, "source_conf.json"), "w"
    ) as file:
        json.dump(source, file, indent=4)

    if target_id:
        # Find the matching target_id
        matching_targets = [
            s for s in source_conf["sources"] if str(s.get("id")) == str(target_id)
        ]

        if matching_targets:
            # If there is a match, get the first one (there should only be one match anyway)
            target = matching_targets[0]
        else:
            logger.error(f"No target found with source id {target_id}")
            sys.exit(1)

        # save the target conf as a json file in the temp folder
        with open(
            os.path.join(temp_folder_name, pack_folder, "target_conf.json"), "w"
        ) as file:
            json.dump(target, file, indent=4)

    # save the pack config as a conf.json file in the temp folder
    try:
        if job["pack_config_override"] is not None:
            if isinstance(job["pack_config_override"], str):
                pack_config_override = json.loads(job["pack_config_override"])
            else:
                pack_config_override = job["pack_config_override"]

            with open(
                os.path.join(temp_folder_name, pack_folder, "pack_conf.json"), "w"
            ) as file:
                json.dump(pack_config_override, file, indent=4)
    except KeyError:
        pass

    # run the job
    send_alive(config_file=agent_conf, mode="job", status="busy")
    try:
        if job["id"] is not None:
            r = send_api_request(
                request=f"/jobs/{job['id']}",
                mode="put",
                query_params={
                    "name": f"{datetime_string}_{random_seed}",
                    "agent_id": agent_conf["context"]["remote"]["id"],
                    "source_id": source_id,
                    "source_version_id": source_version_id,
                    "pack_id": pack_id,
                    "pack_version_id": pack_version_id,
                    "start_date": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "running",
                },
            )
    except KeyError:
        r = send_api_request(
            request=f"/jobs/create",
            mode="post",
            query_params={
                "name": f"{datetime_string}_{random_seed}",
                "agent_id": agent_conf["context"]["remote"]["id"],
                "source_id": source_id,
                "source_version_id": source_version_id,
                "pack_id": pack_id,
                "pack_version_id": pack_version_id,
                "start_date": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "running",
            },
        )

    if r.status_code == 201:
        # The request was successful
        r = r.json()
        job["id"] = r["id"]
        logger.info(f"Job created with id {job['id']}")
    elif r.status_code == 200:
        # The request was successful
        r = r.json()
        job["id"] = r["id"]
        logger.info(f"Job updated with id {job['id']}")
    else:
        # The request failed
        logger.error(f"Failed to create job : {r.text}")
        sys.exit(1)

    status = run_pack(os.path.join(temp_folder_name, pack_folder))
    logs_id = post_run(
        os.path.join(temp_folder_name, pack_folder),
        f"{datetime_string}_{random_seed}",
        pack_id,
        pack_version_id,
        source_id,
        source_version_id,
    )

    logger.success(f"Job run finished")
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    logger.info(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Elapsed Time: {elapsed_time}")

    if status == 0:
        status = "succeeded"
    else:
        status = "failed"

    send_alive(config_file=agent_conf, mode="job", status=status)
    r = send_api_request(
        request=f"/jobs/{job['id']}",
        mode="put",
        query_params={
            "end_date": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": status,
            "logs_id": logs_id,
        },
    )
    if r.status_code != 200:
        logger.info(f"Failed updating job {job['id']}")
        logger.info(f"HTTP Code : {r.status_code} - {r.text}")


@pass_config
def post_run(
    config, run_path, name, pack_id, pack_version_id, source_id, source_version_id
):
    logger.info("------------- Job Post Run -------------")

    agent_conf = config.load_agent_config()

    #########################################################
    ## LOGS
    # Initialize logs_id to None
    logs_id = None
    logger.info(f"Uploading logs to Qalita Platform...")
    if os.path.exists(run_path + "/logs.txt"):
        api_url = agent_conf["context"]["local"]["url"]
        registry_id = agent_conf["registries"][0]["id"]
        user_id = agent_conf["user"]["id"]

        r = send_request(
            request=f"{api_url}/assets/{registry_id}/upload",
            mode="post-multipart",
            file_path=run_path + "/logs.txt",
            query_params={
                "name": name,
                "bucket": "logs",
                "type": "log",
                "version": "1.0.0",
                "description": "job logs",
                "user_id": user_id,
            },
        )
        if r.status_code == 200:
            logger.success("\tLogs pushed")
            logs_id = r.json()["id"]
        elif r.status_code == 404:
            logger.info("\tNo registry")
            sys.exit(1)
        elif r.status_code == 409:
            logger.error("\tFailed to push logs, logs already exist")
            sys.exit(1)
        else:
            logger.error(
                f"\tFailed pushing the logs - HTTP Code : {r.status_code} - {r.text}"
            )

    else:
        logger.info(f"No logs.txt file found")

    logger.info(f"Uploading results to Qalita Platform...")

    #########################################################
    ## Recommendations
    if os.path.exists(run_path + "/recommendations.json"):
        logger.info(f"\tUploading recommendations to Qalita Platform...")

        api_url = agent_conf["context"]["local"]["url"]
        registry_id = agent_conf["registries"][0]["id"]
        user_id = agent_conf["user"]["id"]

        r = send_request(
            request=f"{api_url}/recommendations/upload",
            mode="post-multipart",
            file_path=run_path + "/recommendations.json",
            query_params={
                "source_id": source_id,
                "source_version_id": source_version_id,
                "pack_id": pack_id,
                "pack_version_id": pack_version_id,
            },
        )
        if r.status_code == 200:
            logger.success("recommendations pushed")
        elif r.status_code == 409:
            logger.error("\tFailed to push recommendations, logs already exist")
            sys.exit(1)
        else:
            logger.error(
                f"\tFailed pushing the recommendations - HTTP Code : {r.status_code} - {r.text}"
            )
    else:
        logger.info(f"No recommendations.json file found")

    #########################################################
    ## Schemas
    if os.path.exists(run_path + "/schemas.json"):
        logger.info(f"\tUploading schemas to Qalita Platform...")

        api_url = agent_conf["context"]["local"]["url"]
        registry_id = agent_conf["registries"][0]["id"]
        user_id = agent_conf["user"]["id"]

        r = send_request(
            request=f"{api_url}/schemas/upload",
            mode="post-multipart",
            file_path=run_path + "/schemas.json",
            query_params={
                "source_id": source_id,
                "source_version_id": source_version_id,
                "pack_id": pack_id,
                "pack_version_id": pack_version_id,
            },
        )
        if r.status_code == 200:
            logger.success("schemas pushed")
        elif r.status_code == 409:
            logger.error("\tFailed to push schemas, logs already exist")
            sys.exit(1)
        else:
            logger.error(
                f"\tFailed pushing the schemas - HTTP Code : {r.status_code} - {r.text}"
            )
    else:
        logger.info(f"No schemas.json file found")

    #########################################################
    ## Metrics
    if os.path.exists(run_path + "/metrics.json"):
        logger.info(f"\tUploading Metrics to Qalita Platform...")

        api_url = agent_conf["context"]["local"]["url"]
        registry_id = agent_conf["registries"][0]["id"]
        user_id = agent_conf["user"]["id"]

        r = send_request(
            request=f"{api_url}/metrics/upload",
            mode="post-multipart",
            file_path=run_path + "/metrics.json",
            query_params={
                "source_id": source_id,
                "source_version_id": source_version_id,
                "pack_id": pack_id,
                "pack_version_id": pack_version_id,
            },
        )
        if r.status_code == 200:
            logger.success("Metrics pushed")
        elif r.status_code == 409:
            logger.error("\tFailed to push Metrics, logs already exist")
            sys.exit(1)
        else:
            logger.error(
                f"\tFailed pushing the Metrics - HTTP Code : {r.status_code} - {r.text}"
            )
    else:
        logger.info(f"No metrics.json file found")

    return logs_id


@agent.command()
@pass_config
def joblist(config):
    """Jobs are the tasks that the agent will execute"""
    tab_jobs = []
    agent_conf = config.load_agent_config()
    headers = [
        "ID",
        "Name",
        "Status",
        "Source ID",
        "Source Version",
        "Pack ID",
        "Pack Version",
        "Start",
        "End",
    ]

    r = send_request(
        request=f"{agent_conf['context']['local']['url']}/agents/{agent_conf['context']['remote']['id']}",
        mode="get",
    )
    if r.status_code == 200:
        jobs = r.json()
        for job in jobs["jobs"]:
            tab_jobs.append(
                [
                    job.get("id", ""),
                    job.get("name", ""),
                    job.get("status", ""),
                    job.get("source_id", ""),
                    job.get("source_version", ""),
                    job.get("pack_id", ""),
                    job.get("pack_version", ""),
                    job.get("start_date", ""),
                    job.get("end_date", ""),
                ]
            )

    else:
        logger.error(
            f"Error cannot fetch job list, make sure you are logged in with > qalita agent login : {r.status_code} - {r.reason}"
        )
        return

    print(tabulate(tab_jobs, headers, tablefmt="simple"))


def create_scheduled_job(routine, agent_conf):
    r = send_api_request(
        request=f"/jobs/create",
        mode="post",
        query_params={
            "agent_id": agent_conf["context"]["remote"]["id"],
            "source_id": routine["source"]["id"],
            "target_id": routine["target"]["id"] if routine.get("target") else None,
            "pack_id": routine["pack"]["id"],
            "routine_id": routine["id"],
            "pack_config_override": routine["config"],
            "type": "routine",
        },
    )
    if r.status_code == 201:
        # The request was successful
        r = r.json()
        job_id = r["id"]
        logger.info(f"Job created with id {job_id}")
    else:
        # The request failed
        logger.error(f"Failed to create job : {r.text}")


def is_time_for_job(last_job_end_date_str="", cron_expression="", start_date_str=""):
    # Convert start_date_str to datetime object
    try:
        start_date = datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))
    except ValueError:
        # Handle cases where start_date_str is not a valid datetime string
        start_date = datetime.min
        logger.warning("Invalid or missing start date. Using 1970-01-01 as fallback.")

    # Check if last_job_end_date_str is None, empty or not a valid string
    if not last_job_end_date_str or not isinstance(last_job_end_date_str, str):
        # logger.warning("Invalid or missing last job end date. Using current time as fallback.")
        last_job_end_date = datetime.now()
    else:
        try:
            # Convert the string to a datetime object
            last_job_end_date = datetime.fromisoformat(last_job_end_date_str)
        except ValueError:
            # Handle cases where last_job_end_date_str is not a valid datetime string
            last_job_end_date = datetime.now()

    # Initialize the cron iterator with the last_job_end_date
    cron = croniter.croniter(cron_expression, last_job_end_date)

    # Get the next datetime that matches the cron expression after last_job_end_date
    next_run = cron.get_next(datetime)

    # Get the current time
    now = datetime.now()
    # logger.info(f"Next run : {next_run}")
    # logger.info(f"Now : {now}")
    # logger.info(f"Start date : {start_date}")

    # Compare the current time with the next run time and the start date
    if now >= next_run and now >= start_date:
        return True
    return False


def check_routines(config, agent_start_datetime):
    """Fonction qui va check les routines de la plateforme
    Permet à l'agent en mode worker de savoir si il est capable
    d'executer des routines.
    Pour cela :
    1. Get all active routines
    2. Check if sources id are locally defined, if not, the agent can't run any routines.
    3. Check if jobs already exists and are running for the routines that the agent can run
    4. if there are not job running evaluate the schedule of the routine
    5. If schedule if older that current date
    6. Create job
    7. Continue ....
    """
    source_conf = config.load_source_config()
    agent_conf = config.load_agent_config()
    extract_ids = lambda x: [source["id"] for source in x["sources"]]
    source_ids = extract_ids(source_conf)

    # 1. Get all active routines
    routines = send_api_request(
        request=f"/routines/all",
        mode="get",
    )

    if routines.status_code in [200, 404]:
        routines = routines.json()
        if isinstance(routines, list):
            jobs = send_api_request(
                request=f"/jobs/all",
                mode="get",
            )
            if jobs.status_code in [200, 404]:
                jobs = jobs.json()
        else:
            # logger.info("No routines found")
            return

        # select only routines with status == active
        routines = [routine for routine in routines if routine["status"] == "active"]

        for routine in routines:
            if routine["status"] == "active":
                # 2. Check if sources id are locally defined, if not, the agent can't run any routines.
                if routine["source"]["id"] in source_ids:
                    # logger.info(f'Found source {routine["source"]["id"]} in local sources')
                    if isinstance(jobs, list):
                        # 3. Check if jobs already exists and are running for the routines that the agent can run
                        last_job = None
                        for job in jobs:
                            if (
                                job["source"]["id"] == routine["source"]["id"]
                                and job["pack"]["id"] == routine["pack"]["id"]
                            ):
                                last_job = job
                                if job["status"] in ["running", "pending"]:
                                    # logger.info(f'Job {job["id"]} already running or pending for routine {routine["id"]}')
                                    break
                        if last_job != None:
                            if is_time_for_job(
                                last_job_end_date_str=last_job["end_date"],
                                cron_expression=routine["schedule"],
                                start_date_str=routine["start_date"],
                            ):
                                create_scheduled_job(routine, agent_conf)
                        else:
                            if is_time_for_job(
                                last_job_end_date_str=agent_start_datetime.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                cron_expression=routine["schedule"],
                                start_date_str=routine["start_date"],
                            ):
                                create_scheduled_job(routine, agent_conf)
                    else:
                        if is_time_for_job(
                            last_job_end_date_str=agent_start_datetime.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            cron_expression=routine["schedule"],
                            start_date_str=routine["start_date"],
                        ):
                            create_scheduled_job(routine, agent_conf)
    else:
        logger.warning("Can't fetch routines or jobs from the platform")
