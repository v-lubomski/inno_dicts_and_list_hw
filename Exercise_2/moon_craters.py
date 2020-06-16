"""Считывание и анализ матрицы данных из файла на предмет количества кратеров."""


def read_matrix(filename: str) -> list:
    """Функция чтения матрицы из файла и преобразование считанных значений в список списков.

    :filename(str) - название файла с матрицей, лежащего в той же папке, что и этот скрипт
    """
    processed_matrix = list()
    with open(filename) as file:
        for line in file.readlines():
            listed_line = list(line.strip())
            processed_matrix.append(listed_line)
    return processed_matrix


def calculate(matrix: list) -> int:
    """Принимает на вход матрицу данных и считает количество кратеров.

    Подсчёт идёт по правилу: одним кратером считается совокупность единиц, которые касаются друг друга
    какой либо из сторон (но не по диагонали). На выход подаётся число - количество кратеров.

    :matrix(list) - список списков, матрица данных из нолей и единиц
    """
    craters_counter = 0

    def recursion_finder(row: int, cell: int) -> None:
        """Функция рекурсивно проходит по элементам матрицы в поиске прилегающих единиц.

        Для того, чтобы избежать повторной обработки уже обработанных единиц, устанавливает им значение 0.

        :row(int) - индекс строки матрицы (списка)
        :cell(int) - индекс ячейки в строке матрицы
        """
        if matrix[row][cell] == "1":
            matrix[row][cell] = "0"
            if cell != 0:
                recursion_finder(row, cell - 1)
            if cell != len(matrix[row]) - 1:
                recursion_finder(row, cell + 1)
            if row != 0:
                recursion_finder(row - 1, cell)
            if row != len(matrix) - 1:
                recursion_finder(row + 1, cell)

    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == "1":
                recursion_finder(r, c)
                craters_counter += 1

    return craters_counter


if __name__ == '__main__':
    print(calculate(read_matrix('example_matrix.txt')))
