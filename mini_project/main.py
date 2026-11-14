# mini_project/main.py
# Module 12 dealership assistant demonstration.

from mini_project.dealership import DealershipAssistant, VehicleInventory


def main():
    # Create the dealership inventory.
    inventory = VehicleInventory(
        {
            "Toyota Prius": 12000,
            "Honda Civic": 15000,
            "Nissan Leaf": 10000,
        }
    )

    # Create the assistant with model-selected tools.
    bot = DealershipAssistant("Alex", inventory)

    print("Dealership Assistant - Module 12")
    print("Ask about vehicle prices and availability.")
    print("Type 'quit' to exit.")

    while True:
        message = input("\nCustomer: ").strip()

        if message.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        if not message:
            continue

        reply = bot.respond(message)
        print(f"Assistant: {reply}")

        # Staff must approve or reject any pending price changes.
        for request_id, request in list(bot.tools.pending.items()):
            print("\nSTAFF APPROVAL REQUIRED")
            print(f"Request: {request_id}")
            print(f"Vehicle: {request['vehicle']}")
            print(f"New price: £{request['new_price']:,}")

            decision = input("Approve (a) or reject (r)? ").strip().lower()

            if decision == "a":
                print(bot.tools.approve(request_id))
            else:
                print(bot.tools.reject(request_id))


if __name__ == "__main__":
    main()
