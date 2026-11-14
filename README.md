
# ISM3232 Module 10 — OOP for Agents

## Project Overview

This project demonstrates object-oriented programming in Python by building a rule-based customer support chatbot and a car dealership assistant.

## Part 1: Customer Support Chatbot

The chatbot, Sunny, can:
- Answer order status questions
- Check product stock
- Refer sensitive requests to a human agent
- Record conversation history
- Count user messages

### Main Classes
- OrderLookup
- StockLookup
- SupportChatbot

## Part 2: OOP Exercises

Exercise 1: Identify classes, objects, attributes, methods, and composition.

Exercise 2: Add a method to count user messages.

Exercise 3: Add a StockLookup tool.

Exercise 4: Create two chatbot objects with separate histories.

## Part 3: Car Dealership Mini-Project

The dealership assistant, Alex, can:
- Answer vehicle price questions
- Check vehicle availability
- Refer financing questions to a sales employee
- Record conversation history

### Main Classes
- VehicleInventory
- DealershipAssistant

## How to Run

Run the support chatbot:

    python3 main.py

Run the two-chatbot example:

    python3 two_bots.py

Run the dealership assistant:

    python3 -m mini_project.main

## Testing

Run all tests:

    pytest -v

Run code quality checks:

    ruff check .
    ruff format --check .

## Test Results

14 automated tests passed:
- 10 customer support chatbot tests
- 4 car dealership assistant tests

## What I Learned

This project demonstrates how classes and objects organize code, how instance attributes store separate conversation histories, and how composition allows chatbots to use separate tools.

It also demonstrates automated testing with pytest and code quality checks with Ruff.

## Module 12 Mini-Project Reflection

My dealership assistant uses model-selected tools to answer customer questions about vehicle prices and availability. A successful request occurs when a customer asks for the price of a Toyota Prius and the assistant selects the get_price tool to return the correct inventory price. The central guardrail refuses a tool request when the model proposes a vehicle that the customer did not mention. Price changes are placed in a pending queue and require staff approval before the inventory is updated. Questions about financing are handed off to the sales team instead of being answered automatically. I updated the assistant's instructions and tool workflow to prioritize verified inventory information, prevent unauthorized changes, and involve a human for sensitive requests.
