"""Main module."""
class Calculator:
    """
    Prosta klasa reprezentująca kalkulator.

    Metody:
    - add(x, y): Dodaje dwie liczby.
    - subtract(x, y): Odejmuje drugą liczbę od pierwszej.
    - multiply(x, y): Mnoży dwie liczby.
    - divide(x, y): Dzieli pierwszą liczbę przez drugą.
    """

    def add(self, x, y):
        """
        Dodaje dwie liczby.

        :param x: Pierwsza liczba.
        :param y: Druga liczba.
        :return: Wynik dodawania.
        """
        return x + y

    def subtract(self, x, y):
        """
        Odejmuje drugą liczbę od pierwszej.

        :param x: Pierwsza liczba.
        :param y: Druga liczba.
        :return: Wynik odejmowania.
        """
        return x - y

    def multiply(self, x, y):
        """
        Mnoży dwie liczby.

        :param x: Pierwsza liczba.
        :param y: Druga liczba.
        :return: Wynik mnożenia.
        """
        return x * y

    def divide(self, x, y):
        """
        Dzieli pierwszą liczbę przez drugą.

        :param x: Liczba dzielona.
        :param y: Liczba dzieląca (nie może być zero).
        :return: Wynik dzielenia.
        :raise ValueError: Wyjątek w przypadku próby dzielenia przez zero.
        """
        if y == 0:
            raise ValueError("Nie można dzielić przez zero.")
        return x / y
    
    def sdsad(self, x: int, y):
        """
        _summary_

        Args:
            x (int): _description_
            y (_type_): _description_
        """