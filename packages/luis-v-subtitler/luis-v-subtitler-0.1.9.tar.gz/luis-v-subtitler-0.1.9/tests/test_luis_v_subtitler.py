from click.testing import CliRunner

from luis_v_subtitler.cli import main


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    # assert result.output == "()\n" # check if the printing is only "()\n"
    assert result.exit_code == 0
