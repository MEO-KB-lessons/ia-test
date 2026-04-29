"""
Модуль определения транзакций
Содержит класс Transaction и перечисление типов транзакций
"""

from datetime import datetime  # Для временных меток транзакций
from enum import Enum  # Для создания перечислений

class TransactionType(Enum):
    """
    Перечисление возможных типов транзакций
    Используем Enum для ограничения возможных значений
    """
    DEPOSIT = "deposit"      # Пополнение счета
    WITHDRAW = "withdraw"    # Снятие средств
    TRANSFER = "transfer"    # Перевод между счетами
    INTEREST = "interest"    # Начисление процентов

class Transaction:
    """
    Класс, представляющий одну банковскую транзакцию
    Содержит всю информацию о проведенной операции
    """
    
    def __init__(self, transaction_type: TransactionType, amount: float, 
                 from_account: str = None, to_account: str = None):
        """
        Конструктор транзакции
        
        Параметры:
        - transaction_type: тип транзакции (из перечисления)
        - amount: сумма транзакции
        - from_account: счет-отправитель (опционально)
        - to_account: счет-получатель (опционально)
        """
        self.id = id(self)  # Уникальный идентификатор (на основе адреса в памяти)
        self.type = transaction_type  # Тип транзакции
        self.amount = amount          # Сумма
        self.from_account = from_account  # Отправитель
        self.to_account = to_account      # Получатель
        self.timestamp = datetime.now()   # Время совершения
        self.description = self._generate_description()  # Текстовое описание
    
    def _generate_description(self) -> str:
        """
        Генерация текстового описания транзакции
        Внутренний метод, вызывается при создании
        
        Возвращает:
        - str: описание транзакции на русском языке
        """
        if self.type == TransactionType.DEPOSIT:
            return f"Пополнение на сумму {self.amount}"
        elif self.type == TransactionType.WITHDRAW:
            return f"Снятие суммы {self.amount}"
        elif self.type == TransactionType.TRANSFER:
            return f"Перевод {self.amount} со счета {self.from_account} на счет {self.to_account}"
        elif self.type == TransactionType.INTEREST:
            return f"Начисление процентов: {self.amount}"
        return "Транзакция"  # Дефолтное описание
    
    def to_dict(self) -> dict:
        """
        Сериализация транзакции в словарь для JSON
        
        Возвращает:
        - dict: словарь с данными транзакции
        """
        return {
            'id': self.id,
            'type': self.type.value,  # Берем значение из Enum
            'amount': self.amount,
            'from_account': self.from_account,
            'to_account': self.to_account,
            'timestamp': self.timestamp.isoformat(),  # Преобразуем datetime в строку
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Десериализация транзакции из словаря
        
        Параметры:
        - data: словарь с данными транзакции
        
        Возвращает:
        - Transaction: восстановленный объект транзакции
        """
        # Создаем новую транзакцию с данными из словаря
        transaction = cls(
            TransactionType(data['type']),  # Преобразуем строку обратно в Enum
            data['amount'],
            data['from_account'],
            data['to_account']
        )
        # Восстанавливаем ID и временную метку
        transaction.id = data['id']
        transaction.timestamp = datetime.fromisoformat(data['timestamp'])
        transaction.description = data['description']
        return transaction
    
    def __str__(self):
        """
        Строковое представление транзакции для отображения пользователю
        """
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.description}"

