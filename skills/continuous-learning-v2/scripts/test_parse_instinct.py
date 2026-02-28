"""parse_instinct_file()的测试 - 验证frontmatter后的内容被保留
(Tests for parse_instinct_file() — verifies content after frontmatter is preserved.)"""

import importlib.util
import os

# 加载instinct-cli.py（带连字符的文件名需要importlib）
# Load instinct-cli.py (hyphenated filename requires importlib)
_spec = importlib.util.spec_from_file_location(
    "instinct_cli",
    os.path.join(os.path.dirname(__file__), "instinct-cli.py"),
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
parse_instinct_file = _mod.parse_instinct_file


MULTI_SECTION = """\
---
id: instinct-a
trigger: "when coding"
confidence: 0.9
domain: general
---

## Action
Do thing A.

## Examples
- Example A1

---
id: instinct-b
trigger: "when testing"
confidence: 0.7
domain: testing
---

## Action
Do thing B.
"""


def test_multiple_instincts_preserve_content():
    """测试多个本能保留内容 (Test multiple instincts preserve content)"""
    result = parse_instinct_file(MULTI_SECTION)
    assert len(result) == 2
    assert "Do thing A." in result[0]["content"]
    assert "Example A1" in result[0]["content"]
    assert "Do thing B." in result[1]["content"]


def test_single_instinct_preserves_content():
    """测试单个本能保留内容 (Test single instinct preserves content)"""
    content = """\
---
id: solo
trigger: "when reviewing"
confidence: 0.8
domain: review
---

## Action
Check for security issues.

## Evidence
Prevents vulnerabilities.
"""
    result = parse_instinct_file(content)
    assert len(result) == 1
    assert "Check for security issues." in result[0]["content"]
    assert "Prevents vulnerabilities." in result[0]["content"]


def test_empty_content_no_error():
    """测试空内容不报错 (Test empty content no error)"""
    content = """\
---
id: empty
trigger: "placeholder"
confidence: 0.5
domain: general
---
"""
    result = parse_instinct_file(content)
    assert len(result) == 1
    assert result[0]["content"] == ""
