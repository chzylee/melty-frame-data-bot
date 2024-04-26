class MoveFrameData:
    first_active: str
    active: str
    recovery: str
    frame_adv: str
    proration: str

    # All properties required.
    def __init__(self, first_active, active, recovery, frame_adv, proration):
        self.first_active = first_active
        self.active = active
        self.recovery = recovery
        self.frame_adv = frame_adv
        self.proration = proration
