import os

import pytest

from libre_chat.conf import parse_conf
from libre_chat.utils import ChatResponse, download_file, parallel_download


def test_no_conf_file() -> None:
    """Test no conf file found"""
    conf = parse_conf("nothinghere.yml")
    assert len(conf.llm.model_path) > 2


def test_chat_response() -> None:
    """Test ChatResponse schema"""
    with pytest.raises(ValueError) as exc_info:
        ChatResponse(message="toast", sender="wrong")
    assert "sender must be bot or user" in str(exc_info.value)
    with pytest.raises(ValueError) as exc_info:
        ChatResponse(message="toast", type="wrong")
    assert "type must be start, stream or end" in str(exc_info.value)


def test_download_file_fail() -> None:
    """Test fail downloading file"""
    download_file("http://broken", "tests/tmp/noddl")
    assert not os.path.exists("tests/tmp/noddl")


def test_parallel_download_success() -> None:
    """Test downloading file"""
    ddl_test = [
        {
            "url": "https://raw.githubusercontent.com/vemonet/libre-chat/main/README.md",
            "path": "tests/tmp/README.md",
        },
        {
            "url": "https://github.com/vemonet/libre-chat/raw/main/tests/config/amsterdam.zip",
            "path": "tests/tmp/amsterdam.txt",
        },
    ]
    parallel_download(ddl_test)
    assert os.path.exists("tests/tmp/amsterdam.txt")
