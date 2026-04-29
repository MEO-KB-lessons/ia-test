"""
Модуль очереди транзакций
Реализует историю операций с использованием структуры данных очередь
"""

from collections import deque  # Двусторонняя очередь с ограничением размера
from typing import List, Optional  # Аннотации типов
from datetime import datetime  # Для работы с датами
from .transaction import Transaction, TransactionType  # Импорт классов транзакций

class TransactionHistoryQueue:
    """
    Класс очереди истории транзакций
    Использует deque для эффективного хранения с ограничением максимального размера
    """
    
    def __init__(self, max_size: int = 100):
        """
        Конструктор очереди транзакций
        
        Параметры:
        - max_size: максимальное количество хранимых транзакций (по умолчанию 100)
        """
        self.queue = deque(maxlen=max_size)  # Создаем очередь с ограничением размера
    
    def add_transaction(self, transaction: Transaction):
        """
        Добавление транзакции в очередь
        При превышении max_size автоматически удаляется самая старая
        
        Параметры:
        - transaction: объект транзакции для добавления
        """
        self.queue.append(transaction)  # Добавляем в конец очереди
    
    def get_all_transactions(self) -> List[Transaction]:
        """
        Получение всех транзакций из очереди
        
        Возвращает:
        - List[Transaction]: список всех транзакций (от старых к новым)
        """
        return list(self.queue)  # Преобразуем deque в список
    
    def filter_by_date(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        """
        Фильтрация транзакций по диапазону дат
        
        Параметры:
        - start_date: начальная дата
        - end_date: конечная дата
        
        Возвращает:
        - List[Transaction]: отфильтрованный список транзакций
        """
        filtered = []  # Список для отфильтрованных транзакций
        for transaction in self.queue:
            # Проверяем, попадает ли транзакция в диапазон дат
            if start_date <= transaction.timestamp <= end_date:
                filtered.append(transaction)
        return filtered
    
    def filter_by_type(self, transaction_type: TransactionType) -> List[Transaction]:
        """
        Фильтрация транзакций по типу
        
        Параметры:
        - transaction_type: тип транзакции для фильтрации
        
        Возвращает:
        - List[Transaction]: отфильтрованный список транзакций
        """
        # List comprehension: возвращаем только транзакции нужного типа
        return [t for t in self.queue if t.type == transaction_type]
    
    def clear(self):
        """
        Очистка очереди (удаление всех транзакций)
        """
        self.queue.clear()
    
    def to_dict(self) -> list:
        """
        Сериализация всей очереди в список словарей
        
        Возвращает:
        - list: список словарей с данными транзакций
        """
        return [t.to_dict() for t in self.queue]
    
    @classmethod
    def from_dict(cls, data: list):
        """
        Десериализация очереди из списка словарей
        
        Параметры:
        - data: список словарей с данными транзакций
        
        Возвращает:
        - TransactionHistoryQueue: восстановленная очередь
        """
        queue = cls()  # Создаем новую пустую очередь
        # Добавляем каждую транзакцию из данных
        for transaction_data in data:
            queue.add_transaction(Transaction.from_dict(transaction_data))
        return queue
    
    def __len__(self):
        """
        Магический метод для получения длины очереди
        
        Возвращает:
        - int: количество транзакций в очереди
        """
        return len(self.queue)

