from bot import clean_user_input, format_ai_reply


def test_clean_user_input():
    bot_id = 123456789
    # Standard mention
    assert clean_user_input("<@123456789> Xin chào", bot_id) == "Xin chào"
    # Nickname mention
    assert clean_user_input("<@!123456789> Xin chào", bot_id) == "Xin chào"
    # Empty prompt after mention
    assert clean_user_input("<@123456789>", bot_id) == ""
    # Whitespace trimming
    assert clean_user_input("   <@123456789>    Hello   ", bot_id) == "Hello"


def test_format_ai_reply():
    short_reply = "Hello world!"
    assert format_ai_reply(short_reply) == "Hello world!"

    exact_1900 = "a" * 1900
    assert format_ai_reply(exact_1900) == exact_1900

    long_reply = "a" * 1950
    formatted = format_ai_reply(long_reply)
    assert len(formatted) == 1900
    assert formatted.endswith("...")
    assert formatted == ("a" * 1897) + "..."
