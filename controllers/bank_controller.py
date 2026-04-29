"""
Модуль контроллера банковской системы
Содержит бизнес-логику приложения
"""

from typing import Dict, Optional, List  # Аннотации типов
from datetime import datetime  # Для работы с датами
from models import (
    Account, CheckingAccount, SavingsAccount, CreditAccount,
    Transaction, TransactionType, TransactionHistoryQueue
)

class BankController:
    """
    Контроллер банковской системы
    Управляет счетами, транзакциями и бизнес-логикой
    Реализует паттерн MVC как посредник между Model и View
    """
    
    def __init__(self):
        """
        Инициализация контроллера
        Создает словари для хранения счетов и очередей транзакций
        """
        self.accounts: Dict[str, Account] = {}  # Словарь счетов (ключ - номер счета)
        self.transaction_queues: Dict[str, TransactionHistoryQueue] = {}  # Очереди транзакций по счетам
    
    def create_account(self, account_type: str, account_number: str, 
                      holder_name: str, initial_balance: float = 0.0) -> Account:
        """
        Создание нового счета
        
        Параметры:
        - account_type: тип счета ('1' - текущий, '2' - сберегательный, '3' - кредитный)
        - account_number: номер счета
        - holder_name: имя владельца
        - initial_balance: начальный баланс
        
        Возвращает:
        - Account: созданный объект счета
        """
        # Проверяем, не существует ли уже счет с таким номером
        if account_number in self.accounts:
            raise ValueError("Счет с таким номером уже существует")
        
        # Создаем счет нужного типа
        if account_type == '1':
            account = CheckingAccount(account_number, holder_name, initial_balance)
        elif account_type == '2':
            account = SavingsAccount(account_number, holder_name, initial_balance)
        elif account_type == '3':
            account = CreditAccount(account_number, holder_name, initial_balance)
        else:
            raise ValueError("Неверный тип счета")
        
        # Сохраняем счет и создаем для него очередь транзакций
        self.accounts[account_number] = account
        self.transaction_queues[account_number] = TransactionHistoryQueue()
        
        # Если начальный баланс > 0, создаем транзакцию пополнения
        if initial_balance > 0:
            self.deposit(account_number, initial_balance)
        
        return account
    
    def deposit(self, account_number: str, amount: float) -> bool:
        """
        Пополнение счета
        
        Параметры:
        - account_number: номер счета для пополнения
        - amount: сумма пополнения
        
        Возвращает:
        - bool: успешность операции
        """
        account = self._get_account(account_number)  # Получаем счет
        account.deposit(amount)  # Выполняем операцию пополнения
        
        # Создаем и сохраняем транзакцию
        transaction = Transaction(TransactionType.DEPOSIT, amount, to_account=account_number)
        self.transaction_queues[account_number].add_transaction(transaction)
        return True
    
    def withdraw(self, account_number: str, amount: float) -> bool:
        """
        Снятие средств со счета
        
        Параметры:
        - account_number: номер счета для снятия
        - amount: сумма снятия
        
        Возвращает:
        - bool: успешность операции
        """
        account = self._get_account(account_number)  # Получаем счет
        account.withdraw(amount)  # Выполняем операцию снятия
        
        # Создаем и сохраняем транзакцию
        transaction = Transaction(TransactionType.WITHDRAW, amount, from_account=account_number)
        self.transaction_queues[account_number].add_transaction(transaction)
        return True
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> bool:
        """
        Перевод средств между счетами
        
        Параметры:
        - from_account: счет-отправитель
        - to_account: счет-получатель
        - amount: сумма перевода
        
        Возвращает:
        - bool: успешность операции
        """
        # Проверяем, что это разные счета
        if from_account == to_account:
            raise ValueError("Нельзя перевести средства на тот же счет")
        
        # Получаем оба счета
        account_from = self._get_account(from_account)
        account_to = self._get_account(to_account)
        
        # Выполняем перевод
        account_from.withdraw(amount)  # Снимаем с одного счета
        account_to.deposit(amount)      # Зачисляем на другой
        
        # Создаем одну транзакцию для обоих счетов
        transaction = Transaction(TransactionType.TRANSFER, amount, from_account, to_account)
        self.transaction_queues[from_account].add_transaction(transaction)
        self.transaction_queues[to_account].add_transaction(transaction)
        
        return True
    
    def apply_interest(self, account_number: str) -> float:
        """
        Начисление процентов на сберегательный счет
        
        Параметры:
        - account_number: номер сберегательного счета
        
        Возвращает:
        - float: сумма начисленных процентов
        """
        account = self._get_account(account_number)  # Получаем счет
        
        # Проверяем, что счет является сберегательным
        if not isinstance(account, SavingsAccount):
            raise ValueError("Проценты можно начислить только на сберегательный счет")
        
        interest = account.apply_interest()  # Начисляем проценты
        
        # Создаем и сохраняем транзакцию
        transaction = Transaction(TransactionType.INTEREST, interest, to_account=account_number)
        self.transaction_queues[account_number].add_transaction(transaction)
        
        return interest
    
    def get_account(self, account_number: str) -> Optional[Account]:
        """
        Получение счета по номеру
        
        Параметры:
        - account_number: номер счета
        
        Возвращает:
        - Optional[Account]: объект счета или None, если не найден
        """
        return self.accounts.get(account_number)
    
    def get_transaction_history(self, account_number: str) -> List[Transaction]:
        """
        Получение истории транзакций для счета
        
        Параметры:
        - account_number: номер счета
        
        Возвращает:
        - List[Transaction]: список транзакций
        """
        queue = self.transaction_queues.get(account_number)
        if queue:
            return queue.get_all_transactions()
        return []  # Возвращаем пустой список, если очередь не найдена
    
    def filter_transactions(self, account_number: str, filter_type: str, 
                           filter_value=None) -> List[Transaction]:
        """
        Фильтрация транзакций по различным критериям
        
        Параметры:
        - account_number: номер счета
        - filter_type: тип фильтрации ('date', 'type', 'all')
        - filter_value: значение для фильтрации
        
        Возвращает:
        - List[Transaction]: отфильтрованный список транзакций
        """
        queue = self.transaction_queues.get(account_number)
        if not queue:
            return []
        
        # Применяем нужный фильтр
        if filter_type == 'date' and filter_value:
            start_date, end_date = filter_value
            return queue.filter_by_date(start_date, end_date)
        elif filter_type == 'type' and filter_value:
            try:
                trans_type = TransactionType(filter_value)
                return queue.filter_by_type(trans_type)
            except ValueError:
                raise ValueError("Неверный тип транзакции")
        else:
            # Без фильтрации - возвращаем все транзакции
            return queue.get_all_transactions()
    
    def get_all_accounts(self) -> Dict[str, Account]:
        """
        Получение всех счетов
        
        Возвращает:
        - Dict[str, Account]: словарь всех счетов
        """
        return self.accounts
    
    def _get_account(self, account_number: str) -> Account:
        """
        Внутренний метод для получения счета с проверкой существования
        
        Параметры:
        - account_number: номер счета
        
        Возвращает:
        - Account: объект счета
        
        Исключения:
        - ValueError: если счет не найден
        """
        if account_number not in self.accounts:
            raise ValueError(f"Счет {account_number} не найден")
        return self.accounts[account_number]
    
    def to_dict(self) -> dict:
        """
        Сериализация всех данных контроллера в словарь
        
        Возвращает:
        - dict: словарь со всеми счетами и транзакциями
        """
        # Сериализуем все счета
        accounts_data = {num: acc.to_dict() for num, acc in self.accounts.items()}
        # Сериализуем все очереди транзакций
        queues_data = {num: queue.to_dict() for num, queue in self.transaction_queues.items()}
        
        return {
            'accounts': accounts_data,
            'queues': queues_data
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Десериализация контроллера из словаря
        
        Параметры:
        - data: словарь с данными
        
        Возвращает:
        - BankController: восстановленный контроллер
        """
        controller = cls()  # Создаем новый контроллер
        
        # Восстанавливаем счета
        for acc_num, acc_data in data['accounts'].items():
            account = Account.from_dict(acc_data)
            controller.accounts[acc_num] = account
        
        # Восстанавливаем очереди транзакций
        for acc_num, queue_data in data['queues'].items():
            controller.transaction_queues[acc_num] = TransactionHistoryQueue.from_dict(queue_data)
        
        return controller

