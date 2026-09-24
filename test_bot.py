import re

def test_mention_stripping():
    bot_user_id = 123456789
    user_input = f"<@{bot_user_id}> Chào bot!"
    cleaned = re.sub(r"<@!?\d+>", "", user_input).strip()
    assert cleaned == "Chào bot!"

    user_input_nickname = f"<@!{bot_user_id}> Chào bot!"
    cleaned_nickname = re.sub(r"<@!?\d+>", "", user_input_nickname).strip()
    assert cleaned_nickname == "Chào bot!"

    empty_input = f"<@{bot_user_id}>"
    cleaned_empty = re.sub(r"<@!?\d+>", "", empty_input).strip()
    assert cleaned_empty == ""

def test_truncation():
    long_reply = "a" * 2000
    if len(long_reply) > 1900:
        truncated = long_reply[:1897] + "..."
    assert len(truncated) == 1900
    assert truncated.endswith("...")
