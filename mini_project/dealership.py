# mini_project/dealership.py
# Module 12: Model-selected tools, guardrails, and human approval.


class VehicleInventory:
    """Store vehicles and their prices."""

    def __init__(self, vehicles):
        # Keep the vehicle names and prices together.
        self.vehicles = vehicles

    def find_vehicle(self, message):
        # Match a vehicle name against the customer's message.
        for vehicle in self.vehicles:
            if vehicle.lower() in message.lower():
                return vehicle
        return None

    def get_price(self, vehicle):
        # Return the price for a known vehicle.
        return self.vehicles.get(vehicle)

    def check_availability(self, vehicle):
        # Only vehicles in the inventory can be confirmed.
        return vehicle in self.vehicles


class DealershipTools:
    """Validate tool requests and queue changes for approval."""

    def __init__(self, inventory):
        # Save inventory and create a pending-change queue.
        self.inventory = inventory
        self.pending = {}
        self.next_id = 1

    def tool_list(self):
        # Describe the actions a model may select.
        return [
            {
                "name": "get_price",
                "description": "Look up a vehicle price.",
                "parameters": ["vehicle"],
            },
            {
                "name": "check_availability",
                "description": "Check whether a vehicle is available.",
                "parameters": ["vehicle"],
            },
            {
                "name": "request_price_change",
                "description": "Request a price change for staff approval.",
                "parameters": ["vehicle", "new_price"],
            },
        ]

    def run(self, name, arguments, history):
        # Reject malformed arguments.
        if not isinstance(arguments, dict):
            return "Invalid tool arguments."

        # Require the customer to mention the vehicle.
        vehicle = str(arguments.get("vehicle", "")).strip()
        customer_text = " ".join(
            str(message.get("content", ""))
            for message in history
            if message.get("role") == "user"
        )

        if not vehicle or vehicle.lower() not in customer_text.lower():
            return "Refused: the customer did not mention that vehicle."

        # Resolve the vehicle against the real inventory.
        matched = self.inventory.find_vehicle(vehicle)
        if matched is None or matched.lower() != vehicle.lower():
            return "That vehicle is not in our inventory."

        if name == "get_price":
            # Read-only tools can run immediately.
            price = self.inventory.get_price(matched)
            return f"The {matched} costs £{price:,}."

        if name == "check_availability":
            # Availability comes from the inventory.
            return f"Yes, the {matched} is currently available."

        if name == "request_price_change":
            # Price changes must never happen automatically.
            try:
                new_price = int(arguments.get("new_price"))
            except (TypeError, ValueError):
                return "Refused: invalid new price."

            if new_price <= 0:
                return "Refused: the new price must be positive."

            # Store the request without changing inventory.
            request_id = self.next_id
            self.next_id += 1
            self.pending[request_id] = {
                "vehicle": matched,
                "new_price": new_price,
            }
            return f"Price change request {request_id} is awaiting staff approval."

        return "Unknown tool request."

    def approve(self, request_id):
        # Staff approval is required to apply a change.
        request = self.pending.pop(request_id, None)
        if request is None:
            return "Request not found."

        self.inventory.vehicles[request["vehicle"]] = request["new_price"]
        return f"Approved price change for {request['vehicle']}."

    def reject(self, request_id):
        # Rejection discards the change.
        if request_id not in self.pending:
            return "Request not found."

        del self.pending[request_id]
        return "Price change rejected."


class DealershipModel:
    """Choose dealership tools based on customer requests."""

    def decide(self, instructions, history, tools):
        # Inspect the latest customer message.
        message = next(
            (item["content"] for item in reversed(history) if item["role"] == "user"),
            "",
        )
        text = message.lower()

        # Route sensitive financial questions to staff.
        if "finance" in text or "payment" in text:
            return {"reply": "Please speak with our sales team about financing."}

        # Detect a vehicle mentioned by the customer.
        inventory = instructions["inventory"]
        vehicle = inventory.find_vehicle(message)

        # Select a tool rather than executing it here.
        if "change" in text and "price" in text:
            return {"reply": "A staff member must approve price changes."}

        if "price" in text:
            if vehicle is None:
                return {"reply": "Which vehicle would you like a price for?"}
            return {
                "tool": "get_price",
                "arguments": {"vehicle": vehicle},
            }

        if "available" in text or "stock" in text:
            if vehicle is None:
                return {"reply": "Which vehicle are you interested in?"}
            return {
                "tool": "check_availability",
                "arguments": {"vehicle": vehicle},
            }

        if "hello" in text:
            return {
                "reply": (
                    f"Hello! I'm {instructions['name']}, your dealership assistant."
                )
            }

        return {"reply": "I can help with vehicle prices and availability."}


class DealershipAssistant:
    """Use a model and guarded tools to help dealership customers."""

    def __init__(self, name, inventory, model=None):
        # Preserve the earlier constructor and history behavior.
        self.name = name
        self.inventory = inventory
        self.history = []
        self.tools = DealershipTools(inventory)
        self.model = model if model is not None else DealershipModel()

    def respond(self, message):
        # Record the customer message.
        self.history.append({"role": "user", "content": message})

        # Ask the model to choose a reply or tool.
        decision = self.model.decide(
            {"name": self.name, "inventory": self.inventory},
            self.history,
            self.tools.tool_list(),
        )

        if not isinstance(decision, dict):
            reply = "Please speak with our sales team for assistance."
        elif "tool" in decision:
            # All model-selected tools pass through one guardrail.
            reply = self.tools.run(
                decision["tool"],
                decision.get("arguments", {}),
                self.history,
            )
        else:
            reply = decision.get(
                "reply",
                "Please speak with our sales team for assistance.",
            )

        # Preserve conversation history for earlier tests.
        self.history.append({"role": "assistant", "content": reply})
        return reply
