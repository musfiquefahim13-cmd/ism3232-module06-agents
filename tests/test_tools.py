from change_queue import ChangeQueue
from order_tool import OrderLookup
from stock_tool import StockLookup
from toolbox import Toolbox


def customer(text):
    """Create a customer message history."""
    return [{"role": "user", "content": text}]


def make_tools():
    """Create all tools with sample data."""

    orders = {
        "A100": {
            "status": "delivered",
            "address": "1 Main Street",
        },
        "A101": {
            "status": "shipped",
            "address": "2 Oak Street",
        },
        "A102": {
            "status": "processing",
            "address": "3 Pine Street",
        },
    }

    stock = {
        "laptop": 5,
        "headphones": 10,
        "keyboard": 3,
    }

    order_tool = OrderLookup(orders)
    stock_tool = StockLookup(stock)
    change_queue = ChangeQueue(order_tool)

    return Toolbox(order_tool, stock_tool, change_queue)


def test_tool_list_has_three_tools():
    tools = make_tools()
    names = [tool.__name__ for tool in tools.tool_list()]

    assert "look_up_order" in names
    assert "check_stock" in names
    assert "request_address_change" in names


def test_known_order_lookup():
    tools = make_tools()

    reply = tools.run(
        "look_up_order",
        {"order_id": "A100"},
        customer("Where is order A100?"),
    )

    assert "delivered" in reply.lower()


def test_unknown_tool_is_refused():
    tools = make_tools()

    reply = tools.run(
        "delete_everything",
        {},
        customer("Please delete everything"),
    )

    assert isinstance(reply, str)
    assert reply


def test_blank_order_id_is_refused():
    tools = make_tools()

    reply = tools.run(
        "look_up_order",
        {"order_id": " "},
        customer("Where is my order?"),
    )

    assert "order" in reply.lower()


def test_blank_stock_item_is_refused():
    tools = make_tools()

    reply = tools.run(
        "check_stock",
        {"item": " "},
        customer("Is this in stock?"),
    )

    assert isinstance(reply, str)
    assert reply


def test_address_change_waits_for_staff():
    tools = make_tools()

    reply = tools.run(
        "request_address_change",
        {
            "order_id": "A102",
            "new_address": "9 Pine Street",
        },
        customer("Change order A102 to 9 Pine Street"),
    )

    assert "approval" in reply.lower() or "staff" in reply.lower()
    assert len(tools.change_queue.waiting()) == 1
    assert tools.order_tool.orders["A102"]["address"] == "3 Pine Street"


def test_approve_makes_the_change_once():
    tools = make_tools()

    tools.run(
        "request_address_change",
        {
            "order_id": "A102",
            "new_address": "9 Pine Street",
        },
        customer("Change order A102 to 9 Pine Street"),
    )

    requests = tools.change_queue.waiting()
    request_number = requests[0]["number"]

    tools.change_queue.approve(request_number)

    assert tools.order_tool.orders["A102"]["address"] == "9 Pine Street"
    assert tools.change_queue.waiting() == []

    tools.change_queue.approve(request_number)

    assert tools.order_tool.orders["A102"]["address"] == "9 Pine Street"


def test_reject_changes_nothing_and_cannot_be_approved_later():
    tools = make_tools()

    tools.run(
        "request_address_change",
        {
            "order_id": "A102",
            "new_address": "9 Pine Street",
        },
        customer("Change order A102 to 9 Pine Street"),
    )

    request_number = tools.change_queue.waiting()[0]["number"]

    tools.change_queue.reject(request_number)

    assert tools.order_tool.orders["A102"]["address"] == "3 Pine Street"
    assert tools.change_queue.waiting() == []

    tools.change_queue.approve(request_number)

    assert tools.order_tool.orders["A102"]["address"] == "3 Pine Street"


def test_approve_unknown_request():
    tools = make_tools()

    reply = tools.change_queue.approve(999)

    assert isinstance(reply, str)
    assert reply


def test_missing_argument_is_refused():
    tools = make_tools()

    reply = tools.run(
        "request_address_change",
        {"order_id": "A102"},
        customer("Change the address for order A102"),
    )

    assert isinstance(reply, str)
    assert reply
    assert tools.change_queue.waiting() == []


def test_order_id_must_come_from_the_customer():
    tools = make_tools()

    reply = tools.run(
        "look_up_order",
        {"order_id": "A101"},
        customer("Where is A100?"),
    )

    assert "has not given that order ID" in reply


def test_customer_said_ignores_capitals():
    tools = make_tools()

    assert tools.customer_said(
        customer("Ship it to 9 PINE STREET"),
        "9 Pine Street",
    )


def test_unknown_order_containing_a_known_id_is_not_queued():
    tools = make_tools()

    reply = tools.change_queue.request_address_change(
        "A1000",
        "9 Pine Street",
    )

    assert "No order" in reply
    assert tools.change_queue.waiting() == []


def test_check_return_for_delivered_order():
    tools = make_tools()

    reply = tools.run(
        "check_return",
        {"order_id": "A100"},
        customer("Can I return order A100?"),
    )

    assert "30 days" in reply


def test_check_return_refuses_order_id_not_given_by_customer():
    tools = make_tools()

    reply = tools.run(
        "check_return",
        {"order_id": "A101"},
        customer("Can I return order A100?"),
    )

    assert "has not given that order ID" in reply
