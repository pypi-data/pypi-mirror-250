# -*- coding: utf-8 -*-
from __future__ import annotations

from requests_mock import Mocker

from jira_assistant.jira_client import (
    JiraClient,
    get_jira_field,
    get_field_paths_of_jira_field,
    convert_fields_to_create_issue_body,
)
from tests.mock_server import (
    mock_jira_requests,
    mock_jira_requests_with_failed_status_code,
    mock_jira_stories,
)

from . import ASSETS_FILES

DEFAULT_JIRA_URL = "http://localhost"
DEFAULT_JIRA_ACCESS_TOKEN = "123"


def test_get_stories_detail():
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        stories = client.get_stories_detail(
            ["A-1", "A-2", "B-1"],
            [
                {
                    "name": "domain",
                    "jira_name": "customfield_15601",
                    "jira_path": "customfield_15601.value",
                },
                {
                    "name": "status",
                    "jira_name": "status",
                    "jira_path": "status.name",
                },
            ],
        )
        assert len(stories) == 3


def test_get_stories_detail_with_large_amount_of_stories():
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        stories = client.get_stories_detail(
            list(mock_jira_stories.keys()),
            [
                {
                    "name": "domain",
                    "jira_name": "customfield_15601",
                    "jira_path": "customfield_15601.value",
                },
                {
                    "name": "status",
                    "jira_name": "status",
                    "jira_path": "status.name",
                },
            ],
        )
        assert len(stories) == 247


def test_health_check():
    with Mocker(real_http=False, adapter=mock_jira_requests()):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        assert client.health_check() is True


def test_health_check_failed():
    with Mocker(real_http=False, adapter=mock_jira_requests_with_failed_status_code()):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        assert client.health_check() is False


def test_get_stories_detail_failed():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests_with_failed_status_code(),
    ):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        stories = client.get_stories_detail(
            ["A-1", "A-2", "B-1"],
            [
                {
                    "name": "domain",
                    "jira_name": "customfield_15601",
                    "jira_path": "customfield_15601.value",
                },
                {
                    "name": "status",
                    "jira_name": "status",
                    "jira_path": "status.name",
                },
            ],
        )
        assert len(stories) == 0


def test_get_stories_detail_with_large_amount_of_stories_failed():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests_with_failed_status_code(),
    ):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        stories = client.get_stories_detail(
            list(mock_jira_stories.keys()),
            [
                {
                    "name": "domain",
                    "jira_name": "customfield_15601",
                    "jira_path": "customfield_15601.value",
                },
                {
                    "name": "status",
                    "jira_name": "status",
                    "jira_path": "status.name",
                },
            ],
        )
        assert len(stories) == 0


def test_get_all_fields():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        result = client.get_all_fields()

        assert len(result) == 5


def test_get_projects():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        result = client.get_projects()

        assert len(result) == 2
        assert "POC" in [r["name"] for r in result]
        assert "SD" in [r["name"] for r in result]

        result = client.get_projects(include_archived=True, force_refresh=True)
        assert len(result) == 3
        assert "POC" in [r["name"] for r in result]
        assert "SD" in [r["name"] for r in result]
        assert "APPSEC" in [r["name"] for r in result]


def test_get_issue_types():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        result = client.get_issue_types("POC")

        assert len(result) == 7
        assert "Release" in [item["name"] for item in result]


def test_get_fields_by_project_name_and_issue_name():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        project = client.get_project_by_project_name("POC")
        assert project is not None

        issue_type = client.get_issue_type_by_project_name_and_issue_name(
            project["name"], "Story"
        )
        assert issue_type is not None

        result = client.get_fields_by_project_id_and_issue_id(
            project["id"], issue_type["id"]
        )

        assert len(result) == 2


def test_get_fields_by_unkown_project_name_and_issue_name():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        issue_type = client.get_issue_type_by_project_name_and_issue_name(
            "Proj1", "Story1"
        )
        assert issue_type is None


def test_get_fields_by_project_name_and_unkown_issue_name():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        project = client.get_project_by_project_name("POC")
        assert project is not None

        issue_type = client.get_issue_type_by_project_name_and_issue_name(
            project["name"], "Story1"
        )
        assert issue_type is None


def test_get_fields_by_project_id_and_issue_name():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        client = JiraClient(DEFAULT_JIRA_URL, DEFAULT_JIRA_ACCESS_TOKEN)

        project = client.get_project_by_project_name("POC")
        assert project is not None

        issue_type = client.get_issue_type_by_project_id_and_issue_name(
            project["id"], "Story"
        )
        assert issue_type is not None

        result = client.get_fields_by_project_id_and_issue_id(
            project["id"], issue_type["id"]
        )

        assert len(result) == 2


def test_convert_fields_to_create_issue_body():
    issue_fields = {
        "issuetype.name": "Release Support",
        "issuetype.id": "1000",
        "summary": "test",
        "project.id": 10100,
        "project.key": "Sandbox",
    }

    create_issue_fields = convert_fields_to_create_issue_body(issue_fields)
    assert create_issue_fields["issuetype"]["name"] == "Release Support"
    assert create_issue_fields["issuetype"]["id"] == "1000"
    assert create_issue_fields["summary"] == "test"
    assert create_issue_fields["project"]["id"] == 10100
    assert create_issue_fields["project"]["key"] == "Sandbox"


def test_get_jira_field_use_basic_type():
    assert get_jira_field(None) is None
    assert get_jira_field("abc") is None
    actual_field = get_jira_field("any")
    assert actual_field is not None
    assert "isBasic" in actual_field
    assert actual_field.get("isBasic", False) is True


def test_get_jira_field_use_complex_type():
    actual_field = get_jira_field("status")
    assert actual_field is not None
    assert "isBasic" in actual_field
    assert actual_field.get("isBasic", True) is False
    assert actual_field.get("type") == "status"
    properties = actual_field.get("properties")
    assert properties is not None
    assert "name" in [p.get("name", "") for p in properties]
    assert "statusCategory" in [p.get("name", "") for p in properties]


def test_get_field_paths_of_jira_field_use_unkown_type():
    actual_field_paths = get_field_paths_of_jira_field(
        "abc", "abc", ASSETS_FILES / "jira_field_type.json"
    )
    assert actual_field_paths is None


def test_get_field_paths_of_jira_field_use_child_array_type():
    actual_field_paths = get_field_paths_of_jira_field(
        "array-level1", "abc", ASSETS_FILES / "jira_field_type.json"
    )
    assert actual_field_paths is not None
    assert "abc.name.level3" in [item["path"] for item in actual_field_paths]


def test_get_field_paths_of_jira_field_use_basic_type():
    actual_field_paths = get_field_paths_of_jira_field("string", "customfield_17001")
    assert actual_field_paths is not None
    assert "customfield_17001" == actual_field_paths[0]["path"]
    assert not actual_field_paths[0]["isArray"]


def test_get_field_paths_of_jira_field_use_complex_type_no_hierarchy():
    # Author
    actual_field_paths = get_field_paths_of_jira_field("author", "abc")
    assert actual_field_paths is not None
    assert len(actual_field_paths) == 2
    assert "abc.name" in [item["path"] for item in actual_field_paths]
    assert "abc.emailAddress" in [item["path"] for item in actual_field_paths]


def test_get_field_paths_of_jira_field_use_complex_type_multiple_hierarchy():
    # Project
    actual_field_paths = get_field_paths_of_jira_field("project", "abc")
    assert actual_field_paths is not None
    assert len(actual_field_paths) == 5
    assert "abc.name" in [item["path"] for item in actual_field_paths]
    assert "abc.key" in [item["path"] for item in actual_field_paths]
    assert "abc.projectTypeKey" in [item["path"] for item in actual_field_paths]
    assert "abc.projectCategory.description" in [
        item["path"] for item in actual_field_paths
    ]
    assert "abc.projectCategory.name" in [item["path"] for item in actual_field_paths]


def test_get_field_paths_of_jira_field_use_array_type_no_hierarchy():
    # comments-page
    actual_field_paths = get_field_paths_of_jira_field("comments-page", "abc")
    assert actual_field_paths is not None
    assert len(actual_field_paths) == 5
    assert "abc.comments.author.name" in [item["path"] for item in actual_field_paths]
    assert "abc.comments.author.emailAddress" in [
        item["path"] for item in actual_field_paths
    ]
    assert "abc.comments.author.id" in [item["path"] for item in actual_field_paths]
    assert "abc.comments.author.body" in [item["path"] for item in actual_field_paths]
    assert "abc.comments.author.created" in [
        item["path"] for item in actual_field_paths
    ]
