import shutil
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from libre_chat.__main__ import cli

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_version() -> None:
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0


def test_build() -> None:
    result = runner.invoke(
        cli,
        [
            "build",
            "config/chat-vectorstore-qa.yml",
            "--vector",
            "vectorstore/db_faiss",
            "--documents",
            "documents",
        ],
    )
    assert result.exit_code == 0


def test_build_no_args() -> None:
    shutil.rmtree("vectorstore/db_faiss")
    result = runner.invoke(
        cli,
        [
            "build",
            "config/chat-vectorstore-qa.yml",
        ],
    )
    assert result.exit_code == 0


# Mock uvicorn.run to prevent API hanging
@patch("libre_chat.__main__.uvicorn.run")
def test_start(mock_run: MagicMock) -> None:
    mock_run.return_value = None
    result = runner.invoke(cli, ["start"])
    assert result.exit_code == 0
