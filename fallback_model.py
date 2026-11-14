class FallbackModel:
    """Use a backup model when the primary model has no decision."""

    def __init__(self, primary, secondary):
        # Save the primary model.
        self.primary = primary

        # Save the backup model.
        self.secondary = secondary

    def decide(self, instructions, history, tools):
        # Ask the primary model to make a decision.
        result = self.primary.decide(instructions, history, tools)

        # If the primary model returns None, use the backup.
        if result is None:
            return self.secondary.decide(instructions, history, tools)

        # Otherwise, keep the primary model's decision.
        return result
