from mini_project.dealership import (
    DealershipAssistant,
    DealershipTools,
    VehicleInventory,
)


def make_inventory():
    return VehicleInventory(
        {
            "Toyota Prius": 12000,
            "Honda Civic": 15000,
        }
    )


class FakeModel:
    """Return a predetermined decision for testing."""

    def __init__(self, decision):
        self.decision = decision

    def decide(self, instructions, history, tools):
        return self.decision


def test_model_selects_price_tool():
    inventory = make_inventory()
    model = FakeModel(
        {
            "tool": "get_price",
            "arguments": {"vehicle": "Toyota Prius"},
        }
    )

    bot = DealershipAssistant("Alex", inventory, model)
    reply = bot.respond("What is the price of Toyota Prius?")

    assert reply == "The Toyota Prius costs £12,000."


def test_guardrail_refuses_invented_vehicle():
    inventory = make_inventory()
    model = FakeModel(
        {
            "tool": "get_price",
            "arguments": {"vehicle": "Honda Civic"},
        }
    )

    bot = DealershipAssistant("Alex", inventory, model)
    reply = bot.respond("What is the price of Toyota Prius?")

    assert "Refused" in reply
    assert "Honda Civic" not in reply


def test_price_change_waits_for_staff_approval():
    inventory = make_inventory()
    tools = DealershipTools(inventory)

    result = tools.run(
        "request_price_change",
        {
            "vehicle": "Toyota Prius",
            "new_price": 11000,
        },
        [
            {
                "role": "user",
                "content": "Change the Toyota Prius price to 11000.",
            }
        ],
    )

    assert "awaiting staff approval" in result
    assert inventory.get_price("Toyota Prius") == 12000

    approval = tools.approve(1)

    assert "Approved" in approval
    assert inventory.get_price("Toyota Prius") == 11000


def test_rejected_price_change_does_not_apply():
    inventory = make_inventory()
    tools = DealershipTools(inventory)

    tools.run(
        "request_price_change",
        {
            "vehicle": "Toyota Prius",
            "new_price": 10000,
        },
        [
            {
                "role": "user",
                "content": "Change the Toyota Prius price to 10000.",
            }
        ],
    )

    result = tools.reject(1)

    assert "rejected" in result.lower()
    assert inventory.get_price("Toyota Prius") == 12000


def test_financing_question_goes_to_human():
    inventory = make_inventory()
    bot = DealershipAssistant("Alex", inventory)

    reply = bot.respond("Can I get finance for a Toyota Prius?")

    assert "sales team" in reply.lower()
