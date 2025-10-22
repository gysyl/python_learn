from basics.main import normalize_text


def test_normalize_text_basic():
    assert normalize_text("  Hello ") == "hello"


def test_normalize_text_empty():
    assert normalize_text("   ") == ""


def test_normalize_text_mixed_case():
    assert normalize_text("PyThoN") == "python"


def test_preserve_case_true():
    assert normalize_text("PyThoN", preserve_case=True) == "PyThoN"


def test_no_collapse_spaces():
    # 保留连续空白（空格与制表符）
    assert normalize_text("a   b\tc", collapse_spaces=False) == "a   b\tc"


def test_collapse_spaces_newlines_tabs_lower():
    # 折叠换行/制表符为空格并转小写
    assert normalize_text(" Foo\nBar\tBaz ") == "foo bar baz"


def test_preserve_case_and_collapse():
    # 保留大小写并折叠空白
    assert normalize_text("  Mix\tED   Case ", preserve_case=True) == "Mix ED Case"


def test_crossline_only_preserve_inline_spaces():
    # 仅折叠跨行空白：没有换行时，行内多空白保留
    assert (
        normalize_text(
            "  Mix\tED   Case ", preserve_case=True, collapse_crossline_only=True
        )
        == "Mix\tED   Case"
    )


def test_crossline_only_fold_newlines_keep_tabs():
    # 折叠跨行空白，但保留行内制表符与多空格
    assert (
        normalize_text(" Foo\nBar\tBaz ", collapse_crossline_only=True)
        == "foo bar\tbaz"
    )


def test_crossline_only_windows_crlf():
    # Windows CRLF 行结尾的跨行折叠
    assert normalize_text("A\r\nB   C") == "a b c"
    assert normalize_text("A\r\nB   C", collapse_crossline_only=True) == "a b   c"
