class Padding:
    top: int
    left: int
    bottom: int
    right: int

    def __init__(self, top: int, left: int, bottom: int, right: int):
        """
        :param top: int: number of pixels for the top padding
        :param left: int: number of pixels for the left padding
        :param bottom: int: number of pixels for the bottom padding
        :param right: int: number of pixels for the right padding
        """
        super().__init__()
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right