from enum import Enum

class Result(Enum):
    NOT_YET_PLAYED = 0
    WHITE_WON = 1
    BLACK_WON = 2
    DRAW = 3

    @staticmethod
    def parse(result):
        if result == 'white':
            return Result.WHITE_WON
        elif result == 'black':
            return Result.BLACK_WON
        elif result == None:
            return Result.DRAW

    @staticmethod
    def reverse(result):
        if result == Result.WHITE_WON:
            return Result.BLACK_WON
        elif result == Result.BLACK_WON:
            return Result.WHITE_WON
        elif result == Result.DRAW:
            return Result.DRAW