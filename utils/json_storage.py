"""
Модуль для работы с JSON хранилищем
Обеспечивает сохранение и загрузку данных в формате JSON
"""

import json  # Для работы с JSON форматом
import os    # Для работы с файловой системой (проверка существования файлов, создание директорий)
from typing import Any  # Для аннотации типов

class JSONStorage:
    """
    Класс для сохранения и загрузки данных в JSON файлы
    """
    
    def __init__(self, filename: str):
        """
        Конструктор хранилища
        
        Параметры:
        - filename: путь к файлу для сохранения данных
        """
        self.filename = filename  # Сохраняем имя файла
    
    def save(self, data: Any):
        """
        Сохранение данных в JSON файл
        
        Параметры:
        - data: данные для сохранения (любого типа, который поддерживает JSON)
        
        Исключения:
        - IOError: при ошибке записи в файл
        """
        try:
            # Создаем директорию, если она не существует
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            
            # Открываем файл для записи с UTF-8 кодировкой
            with open(self.filename, 'w', encoding='utf-8') as f:
                # Сохраняем данные в JSON с отступами для читаемости
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            raise IOError(f"Ошибка при сохранении данных: {e}")
    
    def load(self) -> dict:
        """
        Загрузка данных из JSON файла
        
        Возвращает:
        - dict: загруженные данные
        
        Исключения:
        - IOError: при ошибке чтения файла
        """
        try:
            # Проверяем, существует ли файл
            if not os.path.exists(self.filename):
                # Если файла нет, возвращаем пустую структуру
                return {'accounts': {}, 'queues': {}}
            
            # Открываем файл для чтения с UTF-8 кодировкой
            with open(self.filename, 'r', encoding='utf-8') as f:
                # Загружаем данные из JSON
                return json.load(f)
        except Exception as e:
            raise IOError(f"Ошибка при загрузке данных: {e}")

