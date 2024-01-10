import os
import sys
from pathlib import Path
from unittest.mock import Mock, call, ANY
import zipfile
import re
import json

import pytest

from ploomber_core.exceptions import COMMUNITY

from ploomber_cloud.cli import cli
from ploomber_cloud import init, api, zip_, deploy
from ploomber_cloud.constants import FORCE_INIT_MESSAGE
from ploomber_cloud.exceptions import BasePloomberCloudException

CMD_NAME = "ploomber-cloud"

COMMUNITY = COMMUNITY.strip()


def test_set_key(monkeypatch, fake_ploomber_dir):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "key", "somekey"])

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    assert (
        "cloud_key: somekey"
        in (fake_ploomber_dir / "stats" / "config.yaml").read_text()
    )


INIT_MESSAGE = f"""Error: Project already initialized with id: someid. \
Run \'ploomber-cloud deploy\' to deploy your \
project. To track its progress, add the --watch flag.
{COMMUNITY}"""


@pytest.mark.parametrize(
    "args", [[CMD_NAME, "init"], [CMD_NAME, "init", "--from-existing"]]
)
def test_init(monkeypatch, fake_ploomber_dir, capsys, args):
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')

    monkeypatch.setattr(sys, "argv", args)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    assert INIT_MESSAGE == capsys.readouterr().err.strip()


def test_init_invalid_env(monkeypatch, set_key):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init"])
    monkeypatch.setattr(init.click, "prompt", Mock(side_effect=["docker"]))
    monkeypatch.setenv("_PLOOMBER_CLOUD_ENV", "invalid")

    with pytest.raises(BasePloomberCloudException) as excinfo:
        monkeypatch.setattr(api.endpoints, api.PloomberCloudEndpoints())

    assert (
        "Unknown environment: invalid. Valid options are: prod, dev, local"
        in str(excinfo.value).strip()
    )


def test_init_flow(monkeypatch, set_key):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init"])
    monkeypatch.setattr(init.click, "prompt", Mock(side_effect=["docker"]))
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid"}))

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/projects/docker",
        headers={"accept": "application/json", "api_key": "somekey"},
    )


def test_init_force_flow(monkeypatch, set_key):
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')

    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init", "--force"])
    monkeypatch.setattr(init.click, "prompt", Mock(side_effect=["docker"]))
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "some-other-id"}))

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/projects/docker",
        headers={"accept": "application/json", "api_key": "somekey"},
    )
    assert "some-other-id" == json.loads(Path("ploomber-cloud.json").read_text())["id"]


def test_init_flow_with_server_error(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init"])
    monkeypatch.setattr(init.click, "prompt", Mock(side_effect=["sometype"]))
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(ok=False, json=Mock(return_value={"detail": "some error"}))

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/projects/sometype",
        headers={"accept": "application/json", "api_key": "somekey"},
    )

    assert (
        (
            f"""Error: An error occurred: some error
{COMMUNITY}"""
        )
        in capsys.readouterr().err.strip()
    )


def test_init_infers_project_type_if_dockerfile_exists(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init"])
    monkeypatch.setattr(init.click, "confirm", Mock(side_effect=["y"]))
    mock_requests_post = Mock(name="requests.post")
    Path("Dockerfile").touch()

    def requests_post(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid"}))

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/projects/docker",
        headers={"accept": "application/json", "api_key": "somekey"},
    )


def test_init_from_existing_flow(monkeypatch, set_key):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init", "--from-existing"])
    monkeypatch.setattr(init.click, "prompt", Mock(side_effect=["someid"]))
    mock_requests_get = Mock(name="requests.get")

    def requests_get(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(
                return_value={"projects": [{"id": "someid"}], "type": "sometype"}
            ),
        )

    mock_requests_get.side_effect = requests_get
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    # Delete ploomber-cloud.json if it exists
    path_to_json = Path("ploomber-cloud.json")
    if path_to_json.exists():
        path_to_json.unlink()

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert path_to_json.exists()
    with open(path_to_json) as f:
        assert json.loads(f.read()) == {
            "id": "someid",
            "type": "sometype",
        }
    assert excinfo.value.code == 0
    mock_requests_get.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects",
                headers={"accept": "application/json", "api_key": "somekey"},
            ),
            call(
                "https://cloud-prod.ploomber.io/projects/someid",
                headers={"accept": "application/json", "api_key": "somekey"},
            ),
        ]
    )


def test_init_from_existing_no_project_message(monkeypatch, set_key, capsys):
    # Try to init from existing with no existing projects
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "init", "--from-existing"])
    mock_requests_get = Mock(name="requests.get")

    def requests_get(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(
                return_value={
                    "projects": [],
                }
            ),
        )

    mock_requests_get.side_effect = requests_get
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    with pytest.raises(SystemExit):
        cli()

    assert (
        "You have no existing projects. Initialize without --from-existing."
        in capsys.readouterr().out
    )


def test_deploy_error_if_missing_key(monkeypatch, fake_ploomber_dir, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    assert (
        "Error: API key not found. Please run 'ploomber-cloud key YOURKEY'\n"
        f"{COMMUNITY}" == capsys.readouterr().err.strip()
    )


def test_deploy(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))

    # so the zip file is not deleted
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return

        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)

    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
    )

    with zipfile.ZipFile("app-someuuid.zip") as z:
        mapping = {}
        for name in z.namelist():
            mapping[name] = z.read(name)

    assert mapping == {
        "Dockerfile": b"FROM python:3.11",
        "app.py": b"print('hello world')",
        "fake-ploomber-dir/stats/config.yaml": b"cloud_key: somekey",
    }

    assert "Deploying project with id: someid" in capsys.readouterr().out


@pytest.mark.parametrize(
    "response_detail, error",
    [
        ["some error", "Error: An error occurred: some error"],
        [
            "Project some-project-123 was not found",
            f"Error: An error occurred: Project some-project-123 was "
            f"not found\n{FORCE_INIT_MESSAGE}",
        ],
        [
            "Project 123456 was not found",
            f"Error: An error occurred: Project 123456 was "
            f"not found\n{FORCE_INIT_MESSAGE}",
        ],
        [
            "Project some_project was not found",
            f"Error: An error occurred: Project some_project was "
            f"not found\n{FORCE_INIT_MESSAGE}",
        ],
    ],
)
def test_deploy_when_not_ok_response(
    monkeypatch, set_key, capsys, response_detail, error
):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))

    # so the zip file is not deleted
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return

        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)

    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=False,
            json=Mock(return_value={"detail": response_detail}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
    )
    assert (
        f"""{error}
{COMMUNITY}"""
        in capsys.readouterr().err.strip()
    )


@pytest.mark.parametrize(
    "job_status, expected_msg",
    [
        (
            {
                "summary": [
                    ["build-docker", "finished"],
                    ["deploy", "finished"],
                    ["webservice", "finished"],
                    ["serving-traffic", "active"],
                ],
                "resources": {
                    "webservice": "http://someid.ploomberapp.io",
                    "is_url_up": True,
                },
                "status": "running",
            },
            """Deployment success.
View project dashboard: https://www.platform.ploomber.io/dashboards/someid/jobid
View your deployed app: http://someid.ploomberapp.io""",
        ),
        (
            {
                "summary": [
                    ["build-docker", "failed"],
                    ["deploy", "failed"],
                    ["webservice", "pending"],
                    ["serving-traffic", "pending"],
                ],
                "resources": {"is_url_up": False},
                "status": "docker-failed",
            },
            """Deployment failed.
View project dashboard: https://www.platform.ploomber.io/dashboards/someid/jobid""",
        ),
        (
            {
                "summary": [
                    ["build-docker", "finished"],
                    ["deploy", "finished"],
                    ["webservice", "failed"],
                    ["serving-traffic", "failed"],
                ],
                "resources": {"is_url_up": False},
                "status": "infrastructure-failed",
            },
            """Deployment failed.
View project dashboard: https://www.platform.ploomber.io/dashboards/someid/jobid""",
        ),
        (
            {
                "summary": [
                    ["build-docker", "finished"],
                    ["deploy", "finished"],
                    ["webservice", "finished"],
                    ["serving-traffic", "failed"],
                ],
                "resources": {"is_url_up": False},
                "status": "failed",
            },
            """Deployment failed.
View project dashboard: https://www.platform.ploomber.io/dashboards/someid/jobid""",
        ),
    ],
)
def test_deploy_watch(monkeypatch, set_key, capsys, job_status, expected_msg):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", "--watch"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))

    # Configure file zipping
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return
        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    # Mock 'post' call for client.deploy()
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    # Mock 'get' call to return different job status info in deploy._watch()
    mock_requests_get = Mock(name="requests.get")

    def requests_get(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value=job_status),
        )

    mock_requests_get.side_effect = requests_get
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    # Call CLI
    with pytest.raises(SystemExit):
        cli()

    # Assert success/fail message is displayed
    assert expected_msg in capsys.readouterr().out


# Assert timeout is enforced when deploy hangs
@pytest.mark.parametrize(
    "timeout, interval, expected_regex, count",
    [
        (0, 0, r"(Timeout reached\.)", 1),
        (
            0.016,  # timeout = 1 second
            0.5,  # interval = 0.5 second
            r"(build-docker: finished \| deploy: finished \| webservice: active \| serving-traffic: pending \|)",  # noqa
            2,  # should ping twice
        ),
    ],
)
def test_deploy_watch_timeout(
    monkeypatch, set_key, capsys, timeout, interval, expected_regex, count
):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", "--watch"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))
    monkeypatch.setattr(deploy, "TIMEOUT_MINS", timeout)
    monkeypatch.setattr(deploy, "INTERVAL_SECS", interval)

    # Configure file zipping
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return
        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    # Mock 'post' call for client.deploy()
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    # Mock 'get' call to return job status info in deploy._watch()
    mock_requests_get = Mock(name="requests.get")

    def requests_get(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(
                return_value={
                    "summary": [
                        ["build-docker", "finished"],
                        ["deploy", "finished"],
                        ["webservice", "active"],
                        ["serving-traffic", "pending"],
                    ],
                    "resources": {"is_url_up": False},
                    "status": "pending",
                }
            ),
        )

    mock_requests_get.side_effect = requests_get
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    # Call CLI
    with pytest.raises(SystemExit):
        cli()

    # Assert expected message is displayed 'count' number of times
    found = re.findall(expected_regex, capsys.readouterr().out)
    assert len(found) == count


@pytest.mark.parametrize(
    "file_contents, error",
    (
        [
            '{"id": "someid", "type" "docker"}',
            f"""Error: Please add a valid ploomber-cloud.json file.
{FORCE_INIT_MESSAGE}
{COMMUNITY}
            """,
        ],
        [
            '{"id": "someid", "type": ""}',
            f"""Error: There are some issues with the ploomber-cloud.json file:
Missing value for key 'type'

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid"}',
            f"""Error: There are some issues with the ploomber-cloud.json file:
Mandatory key 'type' is missing.

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": 123, "type": "docker"}',
            f"""
Error: There are some issues with the ploomber-cloud.json file:
Only string values allowed for key 'id'

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "id": "duplicate", "type": "docker", '
            '"type": "streamlit"}',
            f"""
Error: Please add a valid ploomber-cloud.json file. \
Duplicate keys: 'id', and 'type'
{FORCE_INIT_MESSAGE}
{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "some-type", "some-key": "some-value"}',
            f"""
Error: There are some issues with the ploomber-cloud.json file:
Invalid type 'some-type'. Valid project types are: 'docker', 'panel', and 'streamlit'
Invalid key: 'some-key'. Valid keys are: 'id', and 'type'

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
    ),
    ids=[
        "invalid-json",
        "empty-type-value",
        "type-key-missing",
        "non-string-value",
        "duplicate-keys",
        "invalid-key-value-combination",
    ],
)
def test_deploy_error_if_invalid_json(
    monkeypatch, set_key, capsys, file_contents, error
):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    Path("ploomber-cloud.json").write_text(file_contents)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    assert error.strip() in capsys.readouterr().err.strip()
