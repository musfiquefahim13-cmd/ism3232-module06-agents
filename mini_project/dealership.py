# mini_project/dealership.py


class VehicleInventory:
    """Store vehicles and their prices."""

    def __init__(self, vehicles):
        self.vehicles = vehicles

    def find_vehicle(self, message):
        """Find a vehicle mentioned in a message."""
        for vehicle in self.vehicles:
            if vehicle.lower() in message.lower():
                return vehicle
        return None

    def get_price(self, vehicle):
        """Return a vehicle's price."""
        return self.vehicles.get(vehicle)


class DealershipAssistant:
    """Answer dealership questions using vehicle inventory."""

    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory
        self.history = []

    def respond(self, message):
        """Respond to a customer and save conversation history."""
        self.history.append({"role": "user", "content": message})
        text = message.lower()

        if "finance" in text or "payment" in text:
            reply = "Please speak with our sales team about financing."

        elif "price" in text:
            vehicle = self.inventory.find_vehicle(message)

            if vehicle is None:
                reply = "Which vehicle would you like a price for?"
            else:
                price = self.inventory.get_price(vehicle)
                reply = f"The {vehicle} costs £{price:,}."

        elif "available" in text or "stock" in text:
            vehicle = self.inventory.find_vehicle(message)

            if vehicle is None:
                reply = "Which vehicle are you interested in?"
            else:
                reply = f"Yes, the {vehicle} is currently available."

        elif "hello" in text:
            reply = f"Hello! I'm {self.name}, your dealership assistant."

        else:
            reply = "I can help with vehicle prices and availability."

        self.history.append({"role": "assistant", "content": reply})
        return reply
