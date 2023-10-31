class Dot:
    """
    Класс точки
    """
    def __init__(self, x, y):
        self.x = y
        self.y = x

    def __repr__(self):
        return f"Dot({self.x};{self.y})"
    
    def __eq__(self, another):
        return self.x == another.x and self.y == another.y
    

class Ship:
    """
    Класс корабля
    """
    def __init__(self, startpos: Dot, length: int, vertical: bool):
        self.startpos = startpos # начальная позиция корабля 
        self.length = length # длина корабля
        self.vertical = vertical # если T-> корабль вертикальный
        self.alives = length # количество живых частей корабля 
        
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


class Board:
    def __init__(self, hidden=False, size =6):
        self.size = size # размер поля
        self.hidden = hidden # Если False - значит это наше поле и мы видим свои корабли
        self.field = [["0"]*size for _ in range(size)] # само поле 
        self.ships = [] # список кораблей доски
        self.busy = [] # точки, куда мы уже стреляли 

    def __repr__(self):
        res = "   " + "".join([f"  {i+1} " for i in range(self.size)])+"\n"
        for i, n in enumerate(self.field):
            res+=f"{i+1}  | "+" | ".join(n)+"\n"
        return res.replace('F','0')
    
    
    def out_dot_check(self, dot:Dot): # проверяет, входит ли точка в поле вообще
        if dot.x>0 and dot.x<self.size and dot.y>0 and dot.y<self.size:
            return True
        else:
            return False

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out_dot_check(dot) and self.field[dot.y-1][dot.x-1] =="0":        # проверяем, что точки внутри поля И поле пустое И вокруг точки (нет кораблей)
                pass
            else:
                raise BoardException
        for dot in ship.dots:
            self.field[dot.y-1][dot.x-1] = "■"

b = Board()
a = Ship(Dot(2,4),4,False)
b.add_ship(a)
b.add_ship(Ship(Dot(2,1),2,True))

print(b)
#print(*b.field, sep='\n')




