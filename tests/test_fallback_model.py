from fallback_model import FallbackModel


class SilentModel:
    """A model that cannot make a decision."""

    def decide(self, instructions, history, tools):
        return None


class BackupModel:
    """A backup model that returns a response."""

    def decide(self, instructions, history, tools):
        return {"reply": "Backup model is working."}


def test_fallback_model_uses_backup():
    primary = SilentModel()
    secondary = BackupModel()

    model = FallbackModel(primary, secondary)

    result = model.decide(
        instructions="Help the customer.",
        history=[],
        tools=[],
    )

    assert result == {"reply": "Backup model is working."}
