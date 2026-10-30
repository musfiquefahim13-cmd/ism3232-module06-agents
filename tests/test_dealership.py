# tests/test_dealership.py

from mini_project.dealership import DealershipAssistant, VehicleInventory


def make_assistant():
    """Create a fresh dealership assistant for testing."""
    vehicles = {
        "Toyota Prius": 8995,
        "Honda Jazz": 6495,
        "Toyota Yaris": 7495,
    }
    inventory = VehicleInventory(vehicles)
    return DealershipAssistant("Alex", inventory)


def test_vehicle_price():
    bot = make_assistant()
    reply = bot.respond("What is the price of Toyota Prius?")
    assert reply == "The Toyota Prius costs £8,995."


def test_vehicle_availability():
    bot = make_assistant()
    reply = bot.respond("Is Honda Jazz available?")
    assert reply == "Yes, the Honda Jazz is currently available."


def test_financing_handoff():
    bot = make_assistant()
    reply = bot.respond("Can I get finance?")
    assert "sales team" in reply


def test_conversation_history():
    bot = make_assistant()
    bot.respond("hello")
    bot.respond("What is the price of Toyota Prius?")
    assert len(bot.history) == 4
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"
