import subprocess
import sys

from invisible_python import decode, encode


def cli(tmp_path, *args):
    return subprocess.run(
        [sys.executable, "-m", "invisible_python", *args],
        cwd=tmp_path,
        capture_output=True,
        check=True,
    )


def test_encode(tmp_path):
    source = b'print("hello")\n'
    (tmp_path / "hello.py").write_bytes(source)
    cli(tmp_path, "encode", "hello.py")
    assert (tmp_path / "hello.ipy").read_bytes() == encode(source)
    cli(tmp_path, "encode", "hello.py", "-o", "something.ipy")
    assert decode((tmp_path / "something.ipy").read_bytes()) == source


def test_cat_preserves_bytes(tmp_path):
    source = b"# coding: latin-1\r\nprint('caf\xe9')\r\n"
    (tmp_path / "hello.ipy").write_bytes(encode(source))
    assert cli(tmp_path, "cat", "hello.ipy").stdout == source


def test_run_and_argument_forwarding(tmp_path):
    source = (
        b"import sys\n"
        b"assert __name__ == '__main__'\n"
        b"assert __file__ == 'hello.ipy'\n"
        b"assert __package__ is None\n"
        b"assert sys.argv == ['hello.ipy', 'foo', 'bar', '--flag']\n"
        b"print('hello from invisible python')\n"
    )
    (tmp_path / "hello.ipy").write_bytes(encode(source))
    result = cli(tmp_path, "run", "hello.ipy", "foo", "bar", "--flag")
    assert result.stdout == b"hello from invisible python\n"


def test_run_imports_from_script_directory(tmp_path):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "hello.ipy").write_bytes(encode(
        b"import invisible_test_sibling\n"
        b"import invisible_test_visible\n"
        b"print(invisible_test_sibling.answer + invisible_test_visible.answer)\n"
    ))
    (scripts / "invisible_test_sibling.ipy").write_bytes(encode(b"answer = 40\n"))
    (scripts / "invisible_test_visible.py").write_bytes(b"answer = 2\n")
    assert cli(tmp_path, "run", "scripts/hello.ipy").stdout == b"42\n"


def test_run_respects_source_encoding(tmp_path):
    source = b"# coding: latin-1\nprint('caf\xe9')\n"
    (tmp_path / "hello.ipy").write_bytes(encode(source))
    assert cli(tmp_path, "run", "hello.ipy").stdout.decode() == "caf\u00e9\n"
