from random import randint

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
        self.health = length # количество живых частей корабля 
        
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
        #res = "   " + "".join([f"  {i+1} " for i in range(self.size)])+"\n"
        #for i, n in enumerate(self.field):
        #   res+=f"{i+1}  | "+" | ".join(n)+"\n"
        #res = res.replace('C','0')
        res = ""
        for i in self.field:
            res+= ' '.join(i) +'\n'
        return res

    
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
                    return False
                else:
                    print("Есть пробитие!")
                    return True
        self.field[dot.x][dot.y]="T"
        print("Мимо!")
        return False


board = Board()
board.add_ship(Ship(Dot(2,2),1,True))
board.add_ship(Ship(Dot(5,5),1,True))
board.add_ship(Ship(Dot(5,1),3,False))
board.add_ship(Ship(Dot(0,1),3,False))
board.add_ship(Ship(Dot(0,5),3,True))
board.add_ship(Ship(Dot(1,0),4,True))
board.shot(Dot(1,1))
board.shot(Dot(0,1))
board.shot(Dot(0,2))
board.shot(Dot(0,3))
print(board)



