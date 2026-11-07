
# tests/test_chatbot.py
# Author: Musfique Hossain Fahim

from chatbot import SupportChatbot
from mock_model import MockModel
from order_tool import OrderLookup
from stock_tool import StockLookup


class SilentModel:
    """A model that returns no answer."""

    def reply(self, instructions, history):
        return None


def make_bot():
    """Create a chatbot with mock tools and a mock model."""
    order_tool = OrderLookup({
        "A100": "shipped",
        "A101": "processing",
    })
    stock_tool = StockLookup({
        "rain jacket": 12,
        "day pack": 0,
    })
    return SupportChatbot(
        "Sunny", "Be friendly.", order_tool, stock_tool, MockModel()
    )


def make_bot_with_silent_model():
    """Create a chatbot whose model returns None."""
    order_tool = OrderLookup({
        "A100": "shipped",
        "A101": "processing",
    })
    stock_tool = StockLookup({
        "rain jacket": 12,
        "day pack": 0,
    })
    return SupportChatbot(
        "Sunny", "Be friendly.", order_tool, stock_tool, SilentModel()
    )


def test_chatbot_has_name():
    bot = make_bot()
    assert bot.name == "Sunny"


def test_chatbot_starts_with_empty_history():
    bot = make_bot()
    assert bot.history == []


def test_greeting():
    bot = make_bot()
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_order_lookup():
    bot = make_bot()
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


def test_unknown_order():
    bot = make_bot()
    assert "couldn't find" in bot.respond("Where is order A999?").lower()


def test_address_change_needs_human():
    bot = make_bot()
    assert "human" in bot.respond("Please change my shipping address")


def test_unknown_request_gets_a_safe_reply():
    bot = make_bot()
    reply = bot.respond("Tell me something random")
    assert "not sure" in reply.lower()


def test_two_chatbots_keep_separate_histories():
    first = make_bot()
    second = make_bot()
    first.respond("hello")
    assert len(first.history) == 2
    assert len(second.history) == 0


def test_count_user_messages():
    bot = make_bot()
    bot.respond("hello")
    bot.respond("Where is order A100?")
    user_messages = [
        message for message in bot.history
        if message["role"] == "user"
    ]
    assert len(user_messages) == 2


def test_stock_question_uses_the_tool():
    bot = make_bot()
    assert bot.respond("Is the rain jacket in stock?") == (
        "We have 12 of the rain jacket in stock."
    )


# Week 11: Four additional tests


def test_other_messages_go_to_the_model():
    bot = make_bot()
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_safe_reply_when_the_model_has_no_answer():
    bot = make_bot_with_silent_model()
    assert "try again" in bot.respond("hello")


def test_order_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


def test_handoff_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert "human" in bot.respond("Please change my shipping address")
