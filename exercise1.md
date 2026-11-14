# Exercise 1 — Read the Tool History

**1. What did the customer actually provide?**

The customer first requested a shipping address change. They then provided order ID A102 and the new address, 9 Pine Street, Tampa.

**2. Why were the first two tool requests refused?**

The first tool request used an order ID that the customer had not provided. The second used a shipping address the customer had not provided. The toolbox refused both requests because its guardrails check the customer's actual messages.

**3. How many messages will Ollama receive if the customer next types "thanks"?**

Ollama will receive **14 messages**: one system message, four customer messages, three assistant replies, and six messages representing the three earlier tool calls and their results.

**4. Why is the gift-card handoff acceptable?**

The chatbot's safety rule checks for the word "card" and sends the question to a human. This can incorrectly hand off an ordinary gift-card question, but it reduces the risk of missing sensitive payment-card questions. A false-positive handoff is less harmful than mishandling payment information.