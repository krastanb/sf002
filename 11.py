from random import randint, choice

class Dot:
    """
    Класс точки
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Dot({self.x};{self.y})"
    
    def __eq__(self, another):
        return self.x == another.x and self.y == another.y
    
    def __add__(self, another):
        x = self.x + another.x
        y = self.y + another.y
        return Dot(x, y)
    

class Ship:
    """
    Класс корабля
    """
    def __init__(self, startpos: Dot, length: int, vertical: bool):
        self.startpos = startpos # начальная позиция корабля 
        self.length = length # длина корабля
        self.vertical = vertical # если T-> корабль вертикальный
        self.health = length # здоровье корабля 
        
    @property
    def dots(self):
        dots = []
        for i in range(self.length):
            #dots = [self.startpos]
            x = self.startpos.x
            y = self.startpos.y
            if self.vertical:
                x+=i
            else:
                y+=i
            dots.append(Dot(x, y))
            
        return dots
    
    def hit(self, hit:Dot):
        return hit in self.dots
    

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Выберите точку внутри поля!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли сюда!"
    
class BoardWrongShipException(BoardException):
    pass 
    
class Board:
    def __init__(self, hidden=False, size =6):
        self.size = size # размер поля
        self.hidden = hidden # Если False - значит это наше поле и мы видим свои корабли
        self.field = [["0"]*size for _ in range(size)] # само поле 
        self.ships = [] # список кораблей доски
        self.busy = [] # точки, куда мы уже стреляли 
        self.count = 0

    def __repr__(self):
        res = "   "+''.join([f" {i}  " for i in range(1, self.size+1)])+"\n"
        for num, i in enumerate(self.field, start=1):
            res+= f"{num}   "+' | '.join(i) +'\n'
        res = res.replace('C','0')
        return res if not self.hidden else res.replace('■','0')
    
    def out_dot_check(self, dot:Dot): # проверяет, входит ли точка в поле вообще
        if dot.x>=0 and dot.x<self.size and dot.y>=0 and dot.y<self.size:
            return False
        else:
            return True

    def add_ship(self, ship):
        for dot in ship.dots:
            if not self.out_dot_check(dot) and self.field[dot.x][dot.y] =="0" and self.field[dot.x][dot.y] !="C":        # проверяем, что точки внутри поля И поле пустое И точка не на контуре 
                pass
            else:
                raise BoardWrongShipException
        self.ships.append(ship)
        temp = [(1,0), (0,1), (-1,0), (0,-1)] # закрашиваем контур 
        for dot in ship.dots: 
            self.field[dot.x][dot.y] = "■"
            for conture in temp:
                tempDot = dot + Dot(*conture)
                if not self.out_dot_check(tempDot) and self.field[tempDot.x][tempDot.y]!="■": # чтобы контур не закрашивал корабли 
                    self.field[tempDot.x][tempDot.y]="C" # рисуем контур, диагональ не включил

    def shot(self, dot:Dot): # 
        if self.out_dot_check(dot):
            raise BoardOutException
        if dot in self.busy:
            raise BoardUsedException
        self.busy.append(dot)
        for ship in self.ships:
            if dot in ship.dots:
                ship.health-=1
                self.field[dot.x][dot.y] = "X"
                if ship.health==0:
                    self.count+=1
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Есть пробитие!")
                    return True
        self.field[dot.x][dot.y]="T"
        print("Мимо!")
        return False

class Player:
    def __init__(self, board:Board, enemyboard):
        self.board = board
        self.enemyboard = enemyboard
    
    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemyboard.shot(target)
                return repeat
            except BoardException as e:
                if type(self)!=Computer:
                    print(e)
                else:
                    print("Но такой ход у него уже был")


class Computer(Player):
    def ask(self):
        dot = Dot(randint(0,5),randint(0,5))
        print(f"Компьютер сходил: {dot.x+1} {dot.y+1}")
        return dot


class User(Player):
    def ask(self):
        while True:
            s = input("Введите координаты через пробел: ").split()
            if len(s)!=2:
                print("Введите 2 координаты!")
                continue
            x,y=s
            if not x.isdigit() or not y.isdigit():
                print("Введите числа!")
                continue
            x, y = int(x), int(y)
            return Dot(x-1, y-1)

class Game:
    def __init__(self, size=6, cheats=False):
        self.size = size
        playerboard = self.generate_board()
        compboard = self.generate_board()
        compboard.hidden = False if cheats else True
        self.player = User(playerboard, compboard)
        self.computer = Computer(compboard, playerboard)

    def generate_board(self):
        length_ships = [3,2,2,1,1,1,1]
        board = Board(size=self.size)
        for length in length_ships:
            while True:
                ship = Ship(Dot(randint(0, self.size), randint(0,self.size)),length, choice([True, False]))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        return board
    
    def welcome(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def start(self):
        step = 0
        while True:
            print('-'*20)
            print("Ваша доска")
            print(self.player.board)
            print('-'*20)
            print("Доска компьютера")
            print(self.computer.board)
            if step%2 == 0:
                print("Ваш ход: ")
                repeat = self.player.move()
            else:
                print("Сейчас ходит компьютер")
                repeat = self.computer.move()
            if repeat:
                step-=1
            if self.computer.board.count == 7:
                print("Вы выиграли!")
                break
            if self.player.board.count == 7:
                print("Компьютер выиграл!")
                break
            step+=1


g = Game(cheats=True)
#g = Game()
g.welcome()
g.start()





