# mini_project/main.py

from mini_project.dealership import DealershipAssistant, VehicleInventory


def main():
    vehicles = {
        "Toyota Prius": 8995,
        "Honda Jazz": 6495,
        "Toyota Yaris": 7495,
    }

    inventory = VehicleInventory(vehicles)
    bot = DealershipAssistant("Alex", inventory)

    print("Welcome to the Car Dealership Assistant!")
    print("Ask about prices, availability, or financing.")
    print("Type quit to exit.")

    while True:
        message = input("You: ")

        if message.lower() == "quit":
            break

        print(f"{bot.name}: {bot.respond(message)}")

    print(f"Conversation messages: {len(bot.history)}")


if __name__ == "__main__":
    main()
