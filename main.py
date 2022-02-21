from copy import deepcopy
import sys
import random
import pygame
pygame.init()

Help = pygame.Rect(1, 406, 134, 45)
Check = pygame.Rect(136, 406, 134, 45)
Quit = pygame.Rect(271, 406, 134, 45)
Field = pygame.Rect(0, 0, 404, 404)
Grey = (128, 128, 128)
LightGrey = (200, 200, 200)
Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 255, 0)
Red = (255, 0, 0)
CheckColor = White
ColorCell = White
WindowSize = 81
WindowMultiplier = 5
WindowWidth = WindowSize * WindowMultiplier
WindowHeight = WindowSize * WindowMultiplier
SquareSize = (WindowSize * WindowMultiplier) / 3
CellSize = SquareSize / 3
NumberSize = 25
TextSize = 30
NumberFont = pygame.font.SysFont("calibri", NumberSize)
TextFont = pygame.font.SysFont("calibri", TextSize)
DISPLAYSURF = pygame.display.set_mode((405, 450))
pygame.display.set_caption("Игра для интеллектов")



class Sudoku:

    mas = [[0 for x in range(9)] for y in range(9)]

    def __init__(self):
         self.Numbers = [[0 for x in range(9)] for y in range(9)]
         for i in range(9):
             for j in range(9):
                 self.Numbers[i][j] = 0

    def Menu(self):
        comp = 0
        DISPLAYSURF.fill(White)
        button1 = pygame.Rect(125, 100, 155, 50)
        button2 = pygame.Rect(125, 155, 155, 50)
        button3 = pygame.Rect(125, 210, 155, 50)
        button4 = pygame.Rect(125, 265, 155, 50)
        button5 = pygame.Rect(125, 320, 155, 50)
        TextSurf = NumberFont.render("Выберите сложность:", True, Black)
        DISPLAYSURF.blit(TextSurf, (85, 50))
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if button1.collidepoint(mouse_pos):
                        comp = 1
                        menu = False
                    if button2.collidepoint(mouse_pos):
                        comp = 2
                        menu = False
                    if button3.collidepoint(mouse_pos):
                        comp = 3
                        menu = False
                    if button4.collidepoint(mouse_pos):
                        comp = 4
                        menu = False
                    if button5.collidepoint(mouse_pos):
                        comp = 5
                        menu = False
                    return comp  # возвращает число, которое индетифицирует уровень сложности
            pygame.draw.rect(DISPLAYSURF, LightGrey, button1)  # draw button
            pygame.draw.rect(DISPLAYSURF, LightGrey, button2)
            pygame.draw.rect(DISPLAYSURF, LightGrey, button3)
            pygame.draw.rect(DISPLAYSURF, LightGrey, button4)
            pygame.draw.rect(DISPLAYSURF, LightGrey, button5)
            for i in range(5):
                TextSurf = NumberFont.render("*" + i * "*", True, Black)
                DISPLAYSURF.blit(TextSurf, (200 - i * 6, 120 + i * 55))

            pygame.display.update()

    def Complexity(self):
        comp = self.Menu(self)
        if (comp == 1):
            quantity = random.randrange(33, 35)
        if (comp == 2):
            quantity = random.randrange(31, 33)
        if (comp == 3):
            quantity = random.randrange(29, 31)
        if (comp == 4):
            quantity = random.randrange(27, 29)
        if (comp == 5):
            quantity = random.randrange(25, 27)
        return quantity

    def solve(self, arr):  # основная функция, которая ищет пути решения головоломки
        find = self.find_empty(self, arr)
        if not find:
            return True
        else:
            row, col = find

        for num in range(1, 10):
            if self.valid(self, arr, num, (row, col)):
                arr[row][col] = num

                if self.solve(self, arr):
                    return True

                arr[row][col] = 0

        return False

    def valid(self, arr, num, pos):  # функция проверяет число на повторения в столбцах, строках и секторах

        for i in range(len(arr[0])):
            if arr[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(len(arr)):
            if arr[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if arr[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self, arr): # функция ищет пустые поля для подстановки туда возможных значений
        for i in range(9):
            for j in range(9):
                if arr[i][j] == 0:
                    return i, j
        return None

    def Generation(self):
        quantity = self.Complexity(self)
        possible = False
        while not possible:
            possible = True
            for i in range(9):
                for j in range(9):
                    self.Numbers[i][j] = 0
            for i in range(quantity + 1):
                # choose random numbers
                row = random.randrange(9)
                col = random.randrange(9)
                num = random.randrange(1, 10)
                while (not self.valid(self, self.Numbers, num, (row, col)) or self.Numbers[row][col] != 0):
                    row = random.randrange(9)
                    col = random.randrange(9)
                    num = random.randrange(1, 10)
                self.Numbers[row][col] = num
            CopyOfGrid = deepcopy(self.Numbers)
            if not self.solve(self, CopyOfGrid):
                possible = False

    def drawField(self):  # Данная функция рисует поля самой игры
        for x in range(0, WindowWidth, int(CellSize)):  # создаёт маленькие поля для цифр
            pygame.draw.line(DISPLAYSURF, LightGrey, (x, 0), (x, WindowHeight))
        for y in range(0, WindowHeight, int(CellSize)):
            pygame.draw.line(DISPLAYSURF, LightGrey, (0, y), (WindowWidth, y))

        for x in range(0, WindowWidth, int(SquareSize)):  # разделяет поле на 9 секций по 9 клеток
            pygame.draw.line(DISPLAYSURF, Black, (x, 0), (x, 500))
        for y in range(0, WindowHeight, int(SquareSize)):
            pygame.draw.line(DISPLAYSURF, Black, (0, y), (WindowWidth, y))
        pygame.draw.line(DISPLAYSURF, Black, (0, 405), (WindowWidth, 405))

    def drawGrid(self):  # рисует числа головоломки на игровом поле
        x = 10
        y = 13
        for i in range(9):
            x = 15
            for j in range(9):
                if (self.Numbers[i][j] != 0):
                    NumberSurf = NumberFont.render(str(self.Numbers[i][j]), True, Black)
                    DISPLAYSURF.blit(NumberSurf, (x, y))
                    x += 45
                else:
                    x += 45
            y += 45

    def Conflict(self): #помечает числа черновика красным, если они конфликтуют с другими числами головоломки
        for i in range(9):
            for j in range(9):
                num = self.mas[i][j]
                pos = (i, j)
                x = j * 45 + 32
                y = i * 45 + 1
                if self.mas[i][j] != 0:
                    if not self.valid(self, self.Numbers, num , pos) or not self.valid(self, self.mas, num, pos):
                        MasSurf = NumberFont.render(str(self.mas[i][j]), True, Red)
                        DISPLAYSURF.blit(MasSurf, (x, y))

    def drawMas(self):  # рисует матрицу "черновик"
        y = 1
        for i in range(9):
            x = 32
            for j in range(9):
                if (self.mas[i][j] != 0):
                    MasSurf = NumberFont.render(str(self.mas[i][j]), True, Black)
                    DISPLAYSURF.blit(MasSurf, (x, y))
                    x += 45
                else:
                    x += 45
            y += 45

    def HelpFunction(self):  # функция "подсказка", приближает пользователя к решению головоломки
        CopyOfGrid = deepcopy(self.Numbers)
        CopyOfGrid2 = deepcopy(self.Numbers)
        for i in range(9):
            for j in range(9):
                if self.mas[i][j] != 0:
                    CopyOfGrid[i][j] = self.mas[i][j]  # добавляет числа с черновика, чтобы затем заполнить только пустую клетку
        self.solve(self, CopyOfGrid)  # решает головоломку на тестовой копии
        for i in range(9):
            for j in range(9):
                if self.mas[i][j] != 0:
                    CopyOfGrid2[i][j] = self.mas[i][j]
        i, j = self.find_empty(self, CopyOfGrid2)
        if self.solve(self, CopyOfGrid):
            self.Numbers[i][j] = CopyOfGrid[i][j]  # переносит одну цифру в основную матрицу головоломки
        return self

    def Check(self):
        CheckGrid = deepcopy(self.Numbers)
        for i in range(9):
            for j in range(9):
                if self.mas[i][j] != 0:
                    CheckGrid[i][j] = self.mas[i][j]
        if self.solve(self, CheckGrid):
            CheckColor = Green
        else:
            CheckColor = Red

    def Win(self):
        run = True
        while run:  # цикл выводит экран с поздравлениями, в случае победы
            DISPLAYSURF.fill(White)
            TextCong = TextFont.render("Congratulation", True, Black)
            DISPLAYSURF.blit(TextCong, (100, 200))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    def Game(self):
        self.Generation(self)  # создаёт случайную, но при этом решаемую головоломку, используя значение сложности из функции Menu
        DISPLAYSURF.fill(White)  # Следующие несколько функций нужны для отображения поля и работы кнопок
        self.drawField(self)
        run = True
        key_flag = False
        while run:  # цикл отвечающий за работу игры
            key = None
            DISPLAYSURF.fill(White)
            self.drawField(self)
            self.drawGrid(self)
            self.drawMas(self)
            self.Conflict(self)
            for event in pygame.event.get():  # Далее идёт интерактивная часть графического интерфейса
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.drawGrid(self)
                self.drawMas(self)
                self.Conflict(self)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if Quit.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

                    if Help.collidepoint(mouse_pos):
                        self.HelpFunction(self)
                        ColorCell = White

                    if Field.collidepoint(mouse_pos):
                        x, y = mouse_pos
                        col1 = x // 45
                        row1 = y // 45
                        posX = 0 + col1 * 45
                        posY = 0 + row1 * 45
                        ColorCell = LightGrey
                        key_flag = True
                if key_flag:
                    if event.type == pygame.KEYDOWN:
                        x, y = mouse_pos
                        col1 = x // 45
                        row1 = y // 45
                        if event.key == pygame.K_1:
                            key = 1
                        if event.key == pygame.K_2:
                            key = 2
                        if event.key == pygame.K_3:
                            key = 3
                        if event.key == pygame.K_4:
                            key = 4
                        if event.key == pygame.K_5:
                            key = 5
                        if event.key == pygame.K_6:
                            key = 6
                        if event.key == pygame.K_7:
                            key = 7
                        if event.key == pygame.K_8:
                            key = 8
                        if event.key == pygame.K_9:
                            key = 9
                        if event.key == pygame.K_DELETE:
                            key = 0
                        if event.key == pygame.K_BACKSPACE:
                            key = 0
                        if event.key == pygame.K_RETURN:
                            num = self.mas[row1][col1]
                            if self.valid(self, self.Numbers, num, (row1, col1)):
                                if self.Numbers[row1][col1] == 0:
                                    self.Numbers[row1][col1] = self.mas[row1][col1]
                                    self.mas[row1][col1] = 0
                        if event.key == pygame.K_SPACE:
                            num = self.mas[row1][col1]
                            if self.valid(self, self.Numbers, num, (row1, col1)):
                                if self.Numbers[row1][col1] == 0:
                                    self.Numbers[row1][col1] = self.mas[row1][col1]
                                    self.mas[row1][col1] = 0
                        ColorCell = White
                        key_flag = False
            if key != None:
                if row1 <= 8 and col1 <= 8:
                    if self.Numbers[row1][col1] == 0:
                        self.mas[row1][col1] = key
            pygame.draw.rect(DISPLAYSURF, White, Field)
            if key_flag:
                for i in range(9):
                    for j in range(9):
                        pygame.draw.rect(DISPLAYSURF, ColorCell, (posX, posY, 45, 45))

            CopyOfGrid = deepcopy(self.Numbers)
            if not self.find_empty(self, CopyOfGrid):
                run = False
                self.Win(self)

            pygame.draw.rect(DISPLAYSURF, White, Help)
            pygame.draw.rect(DISPLAYSURF, CheckColor, Check)
            pygame.draw.rect(DISPLAYSURF, White, Quit)
            self.drawField(self)
            self.drawGrid(self)
            self.drawMas(self)
            self.Conflict(self)
            TextHelp = NumberFont.render("Подсказка", True, Black)
            DISPLAYSURF.blit(TextHelp, (11, 417))
            TextCheck = NumberFont.render("Проверка", True, Black)
            DISPLAYSURF.blit(TextCheck, (150, 417))
            TextQuit = NumberFont.render("Выход", True, Black)
            DISPLAYSURF.blit(TextQuit, (301, 417))
            pygame.display.update()


def main():
    Grid = Sudoku
    Sudoku.__init__(Grid)
    Sudoku.Game(Grid)


main()
