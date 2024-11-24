class EmulatorBlockError(Exception):
    """
    模拟器卡顿错误，通常发生在游戏启动阶段
    """
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo