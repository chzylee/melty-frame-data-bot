class MoveFrameData:
    input: str
    first_active: str
    active: str
    recovery: str
    frame_adv: str
    proration: str
    invuln: str

    # All properties required.
    def __init__(
        self,
        input: str,
        first_active: str,
        active: str,
        recovery: str,
        frame_adv: str,
        proration: str,
        invuln: str
    ):
        self.input = input
        self.first_active = first_active
        self.active = active
        self.recovery = recovery
        self.frame_adv = frame_adv
        self.proration = proration
        self.invuln = invuln

    def to_dict(self):
        return {
            "input": self.input,
            "first_active": self.first_active,
            "active": self.active,
            "recovery": self.recovery,
            "frame_adv": self.frame_adv,
            "proration": self.proration,
            "invuln": self.invuln
        }

    def __str__(self):
        return str(self.to_dict())

    @classmethod
    def from_dynamoDB_item(cls, item: dict) -> "MoveFrameData":
        # Realistically dict should always have all properties.
        # Assuming this case and will handle errors if they arise.
        return cls(
            input = item["input"],
            first_active = item["first_active"],
            active = item["active"],
            recovery = item["recovery"],
            frame_adv = item["frame_adv"],
            proration = item["proration"],
            invuln = item["invuln"]
        )
