"""
Модуль определения классов банковских счетов
Содержит абстрактный базовый класс и конкретные реализации счетов
"""

from abc import ABC, abstractmethod  # Для создания абстрактных классов и методов
from datetime import datetime  # Для работы с датой и временем

class Account(ABC):
    """
    Абстрактный базовый класс для всех типов банковских счетов
    Определяет общую структуру и методы для всех счетов
    """
    
    def __init__(self, account_number: str, holder_name: str, balance: float = 0.0):
        """
        Конструктор базового класса Account
        
        Параметры:
        - account_number: уникальный номер счета
        - holder_name: имя владельца счета
        - balance: начальный баланс (по умолчанию 0)
        """
        self.account_number = account_number  # Номер счета
        self.holder_name = holder_name        # Владелец счета
        self._balance = balance               # Баланс (защищенный атрибут)
        self.created_at = datetime.now()      # Дата создания счета
    
    @property
    def balance(self):
        """
        Геттер для баланса (property decorator)
        Обеспечивает контролируемый доступ к приватному полю _balance
        """
        return self._balance
    
    @abstractmethod
    def deposit(self, amount: float) -> bool:
        """
        Абстрактный метод пополнения счета
        Должен быть реализован в дочерних классах
        
        Параметры:
        - amount: сумма пополнения
        
        Возвращает:
        - bool: успешность операции
        """
        if amount <= 0:
            raise ValueError("Сумма депозита должна быть положительной")
        self._balance += amount
        return True
    
    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """
        Абстрактный метод снятия средств
        Должен быть реализован в дочерних классах
        
        Параметры:
        - amount: сумма снятия
        
        Возвращает:
        - bool: успешность операции
        """
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount
        return True
    
    def to_dict(self) -> dict:
        """
        Сериализация объекта счета в словарь для JSON
        
        Возвращает:
        - dict: словарь с данными счета
        """
        return {
            'type': self.__class__.__name__,  # Сохраняем тип счета для восстановления
            'account_number': self.account_number,
            'holder_name': self.holder_name,
            'balance': self._balance,
            'created_at': self.created_at.isoformat()  # Преобразуем datetime в строку
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Десериализация объекта счета из словаря
        
        Параметры:
        - data: словарь с данными счета
        
        Возвращает:
        - Account: восстановленный объект счета
        """
        # Определяем тип счета и создаем соответствующий объект
        account_type = data['type']
        if account_type == 'CheckingAccount':
            account = CheckingAccount(data['account_number'], data['holder_name'], data['balance'])
        elif account_type == 'SavingsAccount':
            account = SavingsAccount(data['account_number'], data['holder_name'], data['balance'])
        elif account_type == 'CreditAccount':
            account = CreditAccount(data['account_number'], data['holder_name'], data['balance'])
        else:
            # По умолчанию создаем текущий счет
            account = CheckingAccount(data['account_number'], data['holder_name'], data['balance'])
        
        # Восстанавливаем дату создания из строки
        account.created_at = datetime.fromisoformat(data['created_at'])
        return account

class CheckingAccount(Account):
    """
    Класс текущего (расчетного) счета
    Наследуется от Account, может иметь комиссии за операции
    """
    
    def __init__(self, account_number: str, holder_name: str, balance: float = 0.0):
        """
        Конструктор текущего счета
        """
        super().__init__(account_number, holder_name, balance)
        self.transaction_fee = 0.0  # Комиссия за транзакции (0 - без комиссии)
    
    def withdraw(self, amount: float) -> bool:
        """
        Переопределенный метод снятия средств
        Учитывает комиссию при снятии
        
        Параметры:
        - amount: сумма снятия
        
        Возвращает:
        - bool: успешность операции
        """
        total_amount = amount + self.transaction_fee  # Сумма с учетом комиссии
        return super().withdraw(total_amount)  # Вызов метода родительского класса

class SavingsAccount(Account):
    """
    Класс сберегательного счета
    Поддерживает начисление процентов на остаток
    """
    
    def __init__(self, account_number: str, holder_name: str, balance: float = 0.0):
        """
        Конструктор сберегательного счета
        """
        super().__init__(account_number, holder_name, balance)
        self.interest_rate = 0.02  # Процентная ставка (2% годовых)
    
    def apply_interest(self):
        """
        Начисление процентов на текущий баланс
        Метод специфичный только для сберегательного счета
        
        Возвращает:
        - float: сумма начисленных процентов
        """
        interest = self._balance * self.interest_rate  # Расчет процентов
        self._balance += interest  # Добавление процентов к балансу
        return interest

class CreditAccount(Account):
    """
    Класс кредитного счета
    Поддерживает отрицательный баланс в пределах кредитного лимита
    """
    
    def __init__(self, account_number: str, holder_name: str, balance: float = 0.0):
        """
        Конструктор кредитного счета
        """
        super().__init__(account_number, holder_name, balance)
        self.credit_limit = 1000.0    # Кредитный лимит
        self.interest_rate = 0.15     # Процентная ставка по кредиту (15% годовых)
    
    def withdraw(self, amount: float) -> bool:
        """
        Переопределенный метод снятия средств
        Учитывает кредитный лимит (баланс может стать отрицательным)
        
        Параметры:
        - amount: сумма снятия
        
        Возвращает:
        - bool: успешность операции
        """
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        # Проверяем, не превышает ли снятие кредитный лимит
        if amount > self._balance + self.credit_limit:
            raise ValueError("Превышен кредитный лимит")
        self._balance -= amount  # Баланс может стать отрицательным
        return True

