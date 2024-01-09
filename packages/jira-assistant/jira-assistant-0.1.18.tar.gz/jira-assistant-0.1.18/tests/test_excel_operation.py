# -*- coding: utf-8 -*-
import pathlib

import pytest

from jira_assistant.excel_definition import ExcelDefinition
from jira_assistant.excel_operation import output_to_excel_file, read_excel_file
from jira_assistant.sprint_schedule import SprintScheduleStore
from tests.utils import read_stories_from_excel

from . import ASSETS_FILES, SRC_ASSETS


def test_read_excel_file():
    excel_definition = ExcelDefinition()
    excel_definition.load_file(SRC_ASSETS / "excel_definition.json")
    sprint_schedule = SprintScheduleStore()
    sprint_schedule.load_file(SRC_ASSETS / "sprint_schedule.json")

    columns, stories = read_excel_file(
        ASSETS_FILES / "happy_path.xlsx", excel_definition, sprint_schedule
    )
    assert len(columns) == 24
    assert len(stories) == 8


def test_output_to_excel_file(tmpdir):
    stories = read_stories_from_excel(
        ASSETS_FILES / "happy_path.xlsx",
        SRC_ASSETS / "excel_definition.json",
        SRC_ASSETS / "sprint_schedule.json",
    )

    output_to_excel_file(
        tmpdir / "happy_path_direct_output.xlsx",
        stories,
        ExcelDefinition().load_file(SRC_ASSETS / "excel_definition.json"),
    )

    assert (tmpdir / "happy_path_direct_output.xlsx").exists()


def test_output_to_excel_file_path_is_not_absolute():
    with pytest.raises(ValueError) as e:
        output_to_excel_file(
            "happy_path_direct_output.xlsx",
            [],
            ExcelDefinition().load_file(SRC_ASSETS / "excel_definition.json"),
        )

    assert "The output file path is invalid." in str(e.value)


def test_output_to_excel_file_path_already_exist_over_write_is_true(tmpdir):
    stories = read_stories_from_excel(
        ASSETS_FILES / "happy_path.xlsx",
        SRC_ASSETS / "excel_definition.json",
        SRC_ASSETS / "sprint_schedule.json",
    )

    output_file = tmpdir / "happy_path_direct_output.xlsx"

    pathlib.Path(output_file).resolve().touch()

    output_to_excel_file(
        output_file,
        stories,
        ExcelDefinition().load_file(SRC_ASSETS / "excel_definition.json"),
        over_write=True,
    )

    assert output_file.exists()


def test_output_to_excel_file_path_already_exist_over_write_is_false(tmpdir):
    output_file = tmpdir / "happy_path_direct_output.xlsx"

    pathlib.Path(output_file).resolve().touch()

    with pytest.raises(FileExistsError) as e:
        output_to_excel_file(
            output_file,
            [],
            ExcelDefinition().load_file(SRC_ASSETS / "excel_definition.json"),
            over_write=False,
        )

    assert "already exist." in str(e.value)
