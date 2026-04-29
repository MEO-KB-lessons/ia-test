"""
Модуль консольного представления
Отвечает за взаимодействие с пользователем через консоль
"""

class ConsoleView:
    """
    Класс для работы с консольным интерфейсом
    Содержит статические методы для вывода меню и ввода данных
    """
    
    @staticmethod
    def display_menu():
        """
        Отображение главного меню программы
        Статический метод, не требует создания экземпляра
        """
        print("\n" + "="*50)
        print("         BANK ACCOUNT SYSTEM")
        print("="*50)
        print("1. Создать новый счет")
        print("2. Пополнить счет")
        print("3. Снять средства")
        print("4. Перевести средства")
        print("5. Показать информацию о счете")
        print("6. Показать историю транзакций")
        print("7. Фильтровать транзакции")
        print("8. Применить проценты (сберегательный счет)")
        print("9. Показать все счета")
        print("0. Сохранить и выйти")
        print("-"*50)
    
    @staticmethod
    def get_input(prompt: str) -> str:
        """
        Получение ввода от пользователя
        
        Параметры:
        - prompt: текст-приглашение для ввода
        
        Возвращает:
        - str: введенная пользователем строка
        """
        return input(prompt)
    
    @staticmethod
    def display_message(message: str, error: bool = False):
        """
        Отображение сообщения пользователю
        
        Параметры:
        - message: текст сообщения
        - error: флаг ошибки (True - сообщение об ошибке)
        """
        if error:
            print(f"\n❌ ОШИБКА: {message}")  # Красный крестик для ошибок
        else:
            print(f"\n✓ {message}")  # Галочка для успешных операций
    
    @staticmethod
    def display_account_info(account):
        """
        Отображение информации о счете
        
        Параметры:
        - account: объект счета для отображения
        """
        if account:
            print(f"\n📋 ИНФОРМАЦИЯ О СЧЕТЕ")
            print(f"  Номер счета: {account.account_number}")
            print(f"  Владелец: {account.holder_name}")
            print(f"  Баланс: {account.balance:.2f} ₽")
            print(f"  Тип счета: {account.__class__.__name__}")
            print(f"  Дата создания: {account.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("Счет не найден")
    
    @staticmethod
    def display_transactions(transactions):
        """
        Отображение списка транзакций
        
        Параметры:
        - transactions: список объектов Transaction
        """
        if not transactions:
            print("\n📭 Транзакции не найдены")
            return
        
        print(f"\n📜 ИСТОРИЯ ТРАНЗАКЦИЙ ({len(transactions)} записей)")
        print("-"*60)
        # Выводим каждую транзакцию на отдельной строке
        for transaction in transactions:
            print(transaction)
        print("-"*60)
    
    @staticmethod
    def get_account_creation_info():
        """
        Сбор данных для создания нового счета
        
        Возвращает:
        - tuple: (тип_счета, номер_счета, имя_владельца, начальный_баланс)
        """
        print("\n🆕 СОЗДАНИЕ НОВОГО СЧЕТА")
        account_type = input("Тип счета (1 - Текущий, 2 - Сберегательный, 3 - Кредитный): ")
        account_number = input("Номер счета: ")
        holder_name = input("Имя владельца: ")
        # Если пользователь ничего не ввел, начальный баланс = 0
        initial_balance = float(input("Начальный баланс (0 по умолчанию): ") or 0)
        
        return account_type, account_number, holder_name, initial_balance
    
    @staticmethod
    def get_transfer_info():
        """
        Сбор данных для перевода средств
        
        Возвращает:
        - tuple: (счет_отправителя, счет_получателя, сумма)
        """
        print("\n💸 ПЕРЕВОД СРЕДСТВ")
        from_account = input("Счет отправителя: ")
        to_account = input("Счет получателя: ")
        amount = float(input("Сумма перевода: "))
        return from_account, to_account, amount
    
    @staticmethod
    def get_transaction_filters():
        """
        Получение параметров фильтрации транзакций
        
        Возвращает:
        - tuple: (тип_фильтра, значение1, значение2)
        """
        print("\n🔍 ФИЛЬТРАЦИЯ ТРАНЗАКЦИЙ")
        print("1. Фильтр по дате")
        print("2. Фильтр по типу")
        print("3. Показать все")
        
        choice = input("Выберите опцию: ")
        
        if choice == '1':
            # Фильтр по дате
            start_date = input("Начальная дата (YYYY-MM-DD): ")
            end_date = input("Конечная дата (YYYY-MM-DD): ")
            return 'date', start_date, end_date
        elif choice == '2':
            # Фильтр по типу
            print("Типы транзакций: deposit, withdraw, transfer, interest")
            trans_type = input("Введите тип: ")
            return 'type', trans_type, None
        else:
            # Показать все (без фильтрации)
            return 'all', None, None

