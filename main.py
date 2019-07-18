from dataclasses import dataclass
from typing import List
import random
import dataclasses

@dataclass
class Box:
    is_open: bool = False
    has_bomb: bool = False
    around_num: int = 0

    def open(self):
        self.is_open = True
        return self.has_bomb


@dataclass
class GameBoard:
    width: int = 0
    height: int = 0
    boxes: List[List[Box]] = dataclasses.field(default_factory=list)

    def setup(self, width, height):
        self.width = width
        self.height = height

        for i in range(height):
            boxes = []
            [boxes.append(Box()) for j in range(width)]
            self.boxes += [boxes]


    def put_bomb(self, bomb_num):
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                count += 1
                bomb = True if count <= bomb_num else False
                self.boxes[i][j].has_bomb = bomb

        for i in range(100):
            x1 = random.randrange(self.width)
            y1 = random.randrange(self.width)

            x2 = random.randrange(self.width)
            y2 = random.randrange(self.width)

            temp = self.boxes[y1][x1]
            self.boxes[y1][x1] = self.boxes[y2][x2]
            self.boxes[y2][x2] = temp


    def display(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.boxes[i][j].is_open:
                    print("  " + str(self.boxes[i][j].around_num), end="")

                else:
                    print("  ?", end="")

            print()


    def check_around_bomb(self, x, y):
        bomb_num = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x+j >= 0 and y+i >= 0 and x+j < self.width and y+i < self.height:
                    bomb_num = bomb_num + 1 if self.boxes[y+i][x+j].has_bomb else bomb_num

        self.boxes[y][x].around_num = bomb_num

        if self.boxes[y][x].around_num != 0:
            return

        for i in range(-1, 2):
            for j in range(-1, 2):
                if x+j >= 0 and y+i >= 0 and x+j < self.width and y+i < self.height:
                    if not self.boxes[y+i][x+j].is_open:
                        self.boxes[y+i][x+j].open()
                        self.check_around_bomb(x+j, y+i)


def main():
    width = 10
    height = 10
    bomb_num = 10

    game_board = GameBoard()
    game_board.setup(width, height)
    game_board.put_bomb(bomb_num)

    is_continue = True

    while(is_continue):
        game_board.display()

        input_x = int(input())
        input_y = int(input())
        
        if game_board.boxes[input_y][input_x].open():
            is_continue = False

        else:
            game_board.check_around_bomb(input_x, input_y)


if __name__ == '__main__':
    main()
