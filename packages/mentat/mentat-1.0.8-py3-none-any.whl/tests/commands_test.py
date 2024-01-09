import subprocess
from pathlib import Path
from textwrap import dedent

import pytest

from mentat.code_feature import CodeFeature
from mentat.command.command import Command, InvalidCommand
from mentat.command.commands.context import ContextCommand
from mentat.command.commands.help import HelpCommand
from mentat.session import Session
from mentat.session_context import SESSION_CONTEXT


def test_invalid_command():
    assert isinstance(Command.create_command("non-existent"), InvalidCommand)


@pytest.mark.asyncio
async def test_help_command(mock_call_llm_api):
    command = Command.create_command("help")
    await command.apply()
    assert isinstance(command, HelpCommand)


@pytest.mark.asyncio
async def test_commit_command(temp_testbed, mock_collect_user_input):
    file_name = "test_file.py"
    with open(file_name, "w") as f:
        f.write("# Commit me!")

    mock_collect_user_input.set_stream_messages(
        [
            "/commit",
            "q",
        ]
    )

    session = Session(cwd=temp_testbed, paths=[])
    session.start()
    await session.stream.recv(channel="client_exit")

    assert subprocess.check_output(["git", "status", "-s"], text=True) == ""


# TODO: test without git
@pytest.mark.asyncio
async def test_include_command(temp_testbed, mock_collect_user_input):
    mock_collect_user_input.set_stream_messages(
        [
            "/include scripts",
            "q",
        ]
    )

    session = Session(cwd=temp_testbed)
    session.start()
    await session.stream.recv(channel="client_exit")

    code_context = SESSION_CONTEXT.get().code_context
    assert (
        Path(temp_testbed) / "scripts" / "calculator.py" in code_context.include_files
    )


# TODO: test without git
@pytest.mark.asyncio
async def test_exclude_command(temp_testbed, mock_collect_user_input):
    mock_collect_user_input.set_stream_messages(
        [
            "/exclude scripts",
            "q",
        ]
    )

    session = Session(cwd=temp_testbed, paths=["scripts"])
    session.start()
    await session.stream.recv(channel="client_exit")

    code_context = SESSION_CONTEXT.get().code_context
    assert not code_context.include_files


@pytest.mark.asyncio
async def test_undo_command(temp_testbed, mock_collect_user_input, mock_call_llm_api):
    temp_file_name = "temp.py"
    with open(temp_file_name, "w") as f:
        f.write(dedent("""\
            # This is a temporary file
            # with 2 lines"""))

    mock_collect_user_input.set_stream_messages(
        [
            "Edit the file",
            "y",
            "/undo",
            "q",
        ]
    )

    mock_call_llm_api.set_streamed_values([dedent(f"""\
        Conversation

        @@start
        {{
            "file": "{temp_file_name}",
            "action": "insert",
            "insert-after-line": 1,
            "insert-before-line": 2
        }}
        @@code
        # I inserted this comment
        @@end""")])

    session = Session(cwd=temp_testbed, paths=[temp_file_name])
    session.start()
    await session.stream.recv(channel="client_exit")

    with open(temp_file_name, "r") as f:
        content = f.read()
        expected_content = dedent("""\
            # This is a temporary file
            # with 2 lines""")
    assert content == expected_content


@pytest.mark.asyncio
async def test_redo_command(temp_testbed, mock_collect_user_input, mock_call_llm_api):
    temp_file_name = "temp.py"
    with open(temp_file_name, "w") as f:
        f.write(dedent("""\
            # This is a temporary file
            # with 2 lines"""))

    mock_collect_user_input.set_stream_messages(
        [
            "Edit the file",
            "y",
            "/undo",
            "/redo",
            "q",
        ]
    )

    new_file_name = "new_temp.py"
    mock_call_llm_api.set_streamed_values([dedent(f"""\
        Conversation

        @@start
        {{
            "file": "{temp_file_name}",
            "action": "insert",
            "insert-after-line": 1,
            "insert-before-line": 2
        }}
        @@code
        # I inserted this comment
        @@end
        @@start
        {{
            "file": "{new_file_name}",
            "action": "create-file"
        }}
        @@code
        # I created this file
        @@end
        """)])

    session = Session(cwd=Path.cwd(), paths=[temp_file_name])
    session.start()
    await session.stream.recv(channel="client_exit")

    with open(temp_file_name, "r") as f:
        content = f.read()
        expected_content = dedent("""\
            # This is a temporary file
            # I inserted this comment
            # with 2 lines""")
    assert content == expected_content

    with open(new_file_name, "r") as f:
        content = f.read()
        expected_content = dedent("""\
            # I created this file""")
    assert content == expected_content


@pytest.mark.asyncio
async def test_undo_all_command(
    temp_testbed, mock_collect_user_input, mock_call_llm_api
):
    temp_file_name = "temp.py"
    with open(temp_file_name, "w") as f:
        f.write(dedent("""\
            # This is a temporary file
            # with 2 lines"""))

    mock_collect_user_input.set_stream_messages(
        [
            "",
            "y",
            "/undo-all",
            "q",
        ]
    )

    # TODO: Make a way to set multiple return values for call_llm_api and reset multiple edits at once
    mock_call_llm_api.set_streamed_values([dedent(f"""\
        Conversation

        @@start
        {{
            "file": "{temp_file_name}",
            "action": "insert",
            "insert-after-line": 1,
            "insert-before-line": 2
        }}
        @@code
        # I inserted this comment
        @@end""")])

    session = Session(cwd=temp_testbed, paths=[temp_file_name])
    session.start()
    await session.stream.recv(channel="client_exit")

    with open(temp_file_name, "r") as f:
        content = f.read()
        expected_content = dedent("""\
            # This is a temporary file
            # with 2 lines""")
    assert content == expected_content


@pytest.mark.asyncio
async def test_clear_command(temp_testbed, mock_collect_user_input, mock_call_llm_api):
    mock_collect_user_input.set_stream_messages(
        [
            "Request",
            "/clear",
            "q",
        ]
    )
    mock_call_llm_api.set_streamed_values(["Answer"])

    session = Session(cwd=Path.cwd())
    session.start()
    await session.stream.recv(channel="client_exit")

    conversation = SESSION_CONTEXT.get().conversation
    assert len(conversation.get_messages()) == 1


# TODO: test without git
@pytest.mark.asyncio
async def test_search_command(
    mocker, temp_testbed, mock_call_llm_api, mock_collect_user_input
):
    mock_collect_user_input.set_stream_messages(
        [
            "Request",
            "/search Query",
            "q",
        ]
    )
    mock_call_llm_api.set_streamed_values(["Answer"])
    mock_feature = CodeFeature(
        Path(temp_testbed) / "multifile_calculator" / "calculator.py"
    )
    mock_score = 1.0
    mocker.patch(
        "mentat.code_context.CodeContext.search",
        return_value=[(mock_feature, mock_score)],
    )
    session = Session(cwd=Path.cwd())
    session.start()
    await session.stream.recv(channel="client_exit")

    rel_path = mock_feature.path.relative_to(Path(temp_testbed))
    assert str(rel_path) in session.stream.messages[-3].data
    assert "cost" in session.stream.messages[-2].data


@pytest.mark.asyncio
async def test_context_command(temp_testbed, mock_call_llm_api):
    command = Command.create_command("context")
    await command.apply()
    assert isinstance(command, ContextCommand)


@pytest.mark.asyncio
async def test_config_command(mock_call_llm_api):
    session_context = SESSION_CONTEXT.get()
    config = session_context.config
    stream = session_context.stream
    command = Command.create_command("config")
    await command.apply("test")
    assert stream.messages[-1].data == "Unrecognized config option: test"
    await command.apply("model")
    assert stream.messages[-1].data.startswith("model: ")
    await command.apply("model", "test")
    assert stream.messages[-1].data == "model set to test"
    assert config.model == "test"
    await command.apply("model", "test", "lol")
    assert stream.messages[-1].data == "Too many arguments"


@pytest.mark.asyncio
async def test_screenshot_command(mocker):
    # Mock the session context and its attributes
    session_context = SESSION_CONTEXT.get()
    mock_vision_manager = mocker.MagicMock()
    session_context.vision_manager = mock_vision_manager
    config = session_context.config
    stream = session_context.stream
    conversation = session_context.conversation

    assert config.model != "gpt-4-vision-preview"

    mock_vision_manager.screenshot.return_value = "fake_image_data"

    screenshot_command = Command.create_command("screenshot")
    await screenshot_command.apply("fake_path")

    mock_vision_manager.screenshot.assert_called_once_with("fake_path")
    assert config.model == "gpt-4-vision-preview"
    assert stream.messages[-1].data == "Screenshot taken for: fake_path."
    assert conversation._messages[-1] == {
        "role": "user",
        "content": [
            {"type": "text", "text": "A screenshot of fake_path"},
            {"type": "image_url", "image_url": {"url": "fake_image_data"}},
        ],
    }

    # Test non-gpt models aren't changed
    config.model = "test"
    await screenshot_command.apply("fake_path")
    assert config.model == "test"

    # Test other models containing vision aren't changed
    config.model = "gpt-vision"
    await screenshot_command.apply("fake_path")
    assert config.model == "gpt-vision"
