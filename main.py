#!/usr/bin/env python3
"""
Bank Account System - Консольное банковское приложение
Главный модуль приложения

Автор: Иван Иванов
Дата создания: 2024
Версия: 1.0.0
"""

import sys  # Для системных операций (например, выход из программы)
from datetime import datetime  # Для работы с датами при фильтрации
from controllers.bank_controller import BankController  # Импорт контроллера
from views.console_view import ConsoleView  # Импорт представления
from utils.json_storage import JSONStorage  # Импорт хранилища JSON

class BankApplication:
    """
    Главный класс приложения
    Объединяет компоненты MVC и управляет основным циклом программы
    """
    
    def __init__(self):
        """
        Инициализация приложения
        Создает экземпляры контроллера, представления и хранилища
        """
        self.controller = BankController()  # Контроллер для бизнес-логики
        self.view = ConsoleView()           # Представление для UI
        self.storage = JSONStorage('data/bank_data.json')  # Хранилище данных
        self.load_data()  # Загружаем сохраненные данные при запуске
    
    def load_data(self):
        """
        Загрузка данных из JSON файла при запуске приложения
        """
        try:
            data = self.storage.load()  # Загружаем данные
            # Проверяем, есть ли данные для восстановления
            if data and (data.get('accounts') or data.get('queues')):
                self.controller = BankController.from_dict(data)  # Восстанавливаем состояние
                self.view.display_message("Данные успешно загружены")
        except Exception as e:
            self.view.display_message(f"Не удалось загрузить данные: {e}", error=True)
    
    def save_data(self):
        """
        Сохранение данных в JSON файл
        
        Возвращает:
        - bool: True если сохранение успешно, False в противном случае
        """
        try:
            data = self.controller.to_dict()  # Получаем данные из контроллера
            self.storage.save(data)           # Сохраняем в файл
            self.view.display_message("Данные успешно сохранены")
            return True
        except Exception as e:
            self.view.display_message(f"Не удалось сохранить данные: {e}", error=True)
            return False
    
    def run(self):
        """
        Главный цикл приложения
        Обрабатывает выбор пользователя и вызывает соответствующие методы
        """
        while True:
            try:
                # Показываем меню и получаем выбор пользователя
                self.view.display_menu()
                choice = self.view.get_input("Выберите действие: ")
                
                # Обработка выбранного действия
                if choice == '1':
                    self.create_account()
                elif choice == '2':
                    self.deposit_money()
                elif choice == '3':
                    self.withdraw_money()
                elif choice == '4':
                    self.transfer_money()
                elif choice == '5':
                    self.show_account_info()
                elif choice == '6':
                    self.show_transaction_history()
                elif choice == '7':
                    self.filter_transactions()
                elif choice == '8':
                    self.apply_interest()
                elif choice == '9':
                    self.show_all_accounts()
                elif choice == '0':
                    # Сохраняем данные и выходим
                    if self.save_data():
                        self.view.display_message("До свидания!")
                        break
                else:
                    self.view.display_message("Неверный выбор. Попробуйте снова.", error=True)
                    
            except ValueError as e:
                # Обработка ошибок валидации (некорректные числа, даты и т.д.)
                self.view.display_message(str(e), error=True)
            except Exception as e:
                # Обработка всех остальных ошибок
                self.view.display_message(f"Произошла ошибка: {e}", error=True)
    
    def create_account(self):
        """
        Создание нового счета
        Получает данные от пользователя и передает их в контроллер
        """
        account_type, acc_num, holder_name, balance = self.view.get_account_creation_info()
        account = self.controller.create_account(account_type, acc_num, holder_name, balance)
        self.view.display_message(f"Счет {acc_num} успешно создан! Баланс: {account.balance:.2f} ₽")
    
    def deposit_money(self):
        """
        Пополнение счета
        """
        acc_num = self.view.get_input("Введите номер счета: ")
        amount = float(self.view.get_input("Сумма пополнения: "))
        self.controller.deposit(acc_num, amount)
        self.view.display_message(f"Счет {acc_num} пополнен на {amount:.2f} ₽")
    
    def withdraw_money(self):
        """
        Снятие средств со счета
        """
        acc_num = self.view.get_input("Введите номер счета: ")
        amount = float(self.view.get_input("Сумма снятия: "))
        self.controller.withdraw(acc_num, amount)
        self.view.display_message(f"Со счета {acc_num} снято {amount:.2f} ₽")
    
    def transfer_money(self):
        """
        Перевод средств между счетами
        """
        from_acc, to_acc, amount = self.view.get_transfer_info()
        self.controller.transfer(from_acc, to_acc, amount)
        self.view.display_message(f"Переведено {amount:.2f} ₽ со счета {from_acc} на счет {to_acc}")
    
    def show_account_info(self):
        """
        Отображение информации о конкретном счете
        """
        acc_num = self.view.get_input("Введите номер счета: ")
        account = self.controller.get_account(acc_num)
        self.view.display_account_info(account)
    
    def show_transaction_history(self):
        """
        Отображение истории транзакций для счета
        """
        acc_num = self.view.get_input("Введите номер счета: ")
        transactions = self.controller.get_transaction_history(acc_num)
        self.view.display_transactions(transactions)
    
    def filter_transactions(self):
        """
        Фильтрация транзакций по дате или типу
        """
        acc_num = self.view.get_input("Введите номер счета: ")
        filter_choice, val1, val2 = self.view.get_transaction_filters()
        
        # Применяем выбранный фильтр
        if filter_choice == 'date':
            # Преобразуем строки дат в объекты datetime
            start_date = datetime.strptime(val1, '%Y-%m-%d')
            end_date = datetime.strptime(val2, '%Y-%m-%d')
            transactions = self.controller.filter_transactions(acc_num, 'date', (start_date, end_date))
        elif filter_choice == 'type':
            transactions = self.controller.filter_transactions(acc_num, 'type', val1)
        else:
            transactions = self.controller.filter_transactions(acc_num, 'all')
        
        self.view.display_transactions(transactions)
    
    def apply_interest(self):
        """
        Начисление процентов на сберегательный счет
        """
        acc_num = self.view.get_input("Введите номер сберегательного счета: ")
        interest = self.controller.apply_interest(acc_num)
        self.view.display_message(f"Начислены проценты: {interest:.2f} ₽")
    
    def show_all_accounts(self):
        """
        Отображение списка всех счетов в системе
        """
        accounts = self.controller.get_all_accounts()
        if not accounts:
            self.view.display_message("Нет открытых счетов")
            return
        
        # Выводим информацию о каждом счете в табличном формате
        print("\n" + "="*50)
        print("СПИСОК ВСЕХ СЧЕТОВ")
        print("="*50)
        for acc_num, account in accounts.items():
            print(f"{acc_num} | {account.holder_name} | {account.__class__.__name__} | {account.balance:.2f} ₽")
        print("="*50)

def main():
    """
    Главная функция программы
    Создает экземпляр приложения и запускает его
    """
    app = BankApplication()  # Создаем приложение
    app.run()                # Запускаем главный цикл

# Точка входа в программу
if __name__ == "__main__":
    main()



