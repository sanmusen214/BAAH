class __GlobalState:
    __global_state = {}

    def __init__(self) -> None:
        self.__global_state = {}

    def get(self, key, default):
        return self.__global_state.get(key, default)

    def set(self, key, value):
        self.__global_state[key] = value

    def remove(self, key):
        if key in self.__global_state:
            del self.__global_state[key]

class RaidState(__GlobalState):
    Exchange="Exchange"
    Wanted="Wanted"
    NormalQuest="NormalQuest"
    HardQuest="HardQuest"
    Event = "Event"
    def __init__(self) -> None:
        super().__init__()

raidstate = RaidState()