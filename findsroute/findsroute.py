#!/usr/bin/env python3
#
# Поиск кратчайшего пути
# Имеется квадратное поле размером 10x10 с размеченными препятствиями. 
# Реализовать любой из алгоритмов поиска кратчайшего пути из заданной точки до целевой.
# На вход программе подается массив с разметкой поля, начальной и конечной точки. Пример вывода:
#.  .   .   .   X
#.  #   #   #   *
#.  *   *   *   *
#.  *   .   #   .
#.  О   .   .   .
# A script for searching shortest route between two points on the 10x10 square
#
# Copyright (C) 2018 dx-77 <d.x77@yandex.ru>.
# GitHub : https://github.com/dx-77
#
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import csv


SQUARE_FILENAME = 'square.tcv'
ANSWER_FILENAME = 'answer.tcv'
SQUARE_SIZE = 10


def load_square(filename=SQUARE_FILENAME):
    try:
        square = {}
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in enumerate(reader):
                square[row[0]] = row[1]
    except Exception as e:
        print('Error loading file "%s" !' % filename)
        print(e)
        return
    return square


def format_square(square, size=SQUARE_SIZE):
    first_point, end_point, asterisk, dot_sharp = 0, 0, 0, 0
    first_xy, end_xy = (-1, -1), (-1, -1)
    for row in square:
        if 'O' in square[row]:
            first_xy = (row, square[row].index('O'))
            first_point += square[row].count('O')
        if 'X' in square[row]:
            end_xy = (row, square[row].index('X'))
            end_point += square[row].count('X')
        asterisk += square[row].count('*')
        dot_sharp += square[row].count('.') + square[row].count('#')
        if len(square[row]) != size:
            return False

    if (first_point == 1 and end_point == 1 and not asterisk 
        and dot_sharp == size * size - 2):
        f_square = []
        for row in square:
            f_square.append([-2 if i == '#' else -1 for i in square[row]])
        return [first_xy, end_xy, f_square]

    return False


def save_answer(answer, filename=ANSWER_FILENAME):
    if not answer:
        return
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            for row in answer:
                writer.writerow(square[row])
    except Exception as e:
        print(e)
        return
    return True


def find_route(f_square, first_xy, end_xy):
    # Uses https://ru.wikipedia.org/wiki/Алгоритм_Ли
    # Соседние ячейки классифицируются в смысле окрестности фон Неймана 
    # Ищется кратчайший ортогональный путь
    def mark_neighbours(x, y, d):
        d_coords = [(x, y, d)]
        while d_coords:
            if f_square[end_xy[0]][end_xy[1]] != -1:
                break

            x, y, d = d_coords.pop(0)

            if x > 0 and f_square[x - 1][y] == -1:
                f_square[x - 1][y] = d
                d_coords.append((x - 1, y, d + 1))
                        
            if x < len(f_square) - 1 and f_square[x + 1][y] == -1:
                f_square[x + 1][y] = d
                d_coords.append((x + 1, y, d + 1))
                         
            if y > 0 and f_square[x][y - 1] == -1:
                f_square[x][y - 1] = d
                d_coords.append((x, y - 1, d + 1))
                        
            if y < len(f_square) - 1 and f_square[x][y + 1] == -1:
                f_square[x][y + 1] = d
                d_coords.append((x, y + 1, d + 1))
       

    def restore_root(x, y, d):
        if d == 1:
            return
     
        if x > 0 and f_square[x - 1][y] == d - 1:
            route.append((x - 1, y))
            restore_root(x - 1, y, d - 1)
            return
      
        if x < len(f_square) - 1 and f_square[x + 1][y] == d - 1:
            route.append((x + 1, y))
            restore_root(x + 1, y, d - 1)
            return
     
        if y > 0 and f_square[x][y - 1] == d - 1:
            route.append((x, y - 1))
            restore_root(x, y - 1, d - 1)
            return
      
        if y < len(f_square) - 1 and f_square[x][y + 1] == d - 1:
            route.append((x, y + 1))
            restore_root(x, y + 1, d - 1)
            return
    
    
    f_square[first_xy[0]][first_xy[1]] = 0
    
    mark_neighbours(*first_xy, 1)
   
    d = f_square[end_xy[0]][end_xy[1]]

    if d == -1:
        return False

    route = []
    restore_root(*end_xy, d)
    for r in route:
        square[r[0]][r[1]] = '*'
    return True


if __name__ == '__main__':
    for filename in ('square.tcv', 'square1.tcv', 'square2.tcv'):
        square = load_square(filename)
        if square:
            print('Square:')
            for row in square:
                for el in square[row]:
                    print(el, end='\t')
                print()

            f_square = format_square(square)
            if f_square:
                answer = find_route(f_square[2], f_square[0], f_square[1])
                if answer:
                    print('Shortest route:')
                    for row in square:
                        for el in square[row]:
                            print(el, end='\t')
                        print()
                    save_answer(square, 'answer_' + filename)
                else:
                    print('There is no route!')
            else:
                print('Square must be %d x %d and contain one only'
                      ' "О" (big EN letter), one "X" (big EN letter), zero "*",'
                      ' "." and "#" symbols'
                      % (SQUARE_SIZE, SQUARE_SIZE))
