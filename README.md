# Crypto Signature Generator

Генератор криптографических подписей на основе гибридного ГПСЧ (Генератора Псевдослучайных Чисел), использующего комбинацию 48-битного LCG (Linear Congruential Generator) и 32-битного LFSR (Linear Feedback Shift Register) с динамическим взаимным влиянием.

## Архитектура

Проект использует модульную архитектуру, где каждый компонент выделен в отдельный файл:

- **`lcg.py`** - Реализация 48-битного LCG генератора
- **`lfsr.py`** - Реализация 32-битного LFSR генератора
- **`initialization.py`** - Модуль инициализации обоих генераторов
- **`signature_generator.py`** - Основной класс для генерации подписей
- **`example.py`** - Примеры использования

## Технические детали

### Параметры LCG
- Множитель: `0x5DEECE66D`
- Инкремент: `0xB`
- Модуль: `2^48 - 1`

### Параметры LFSR
- Длина: 32 бита
- Отводы: [32, 22, 2, 1] (1-индексация)
- Полином: `x³² + x²² + x² + x + 1`

### Алгоритм генерации

1. **Инициализация** - LCG и LFSR инициализируются из timestamp с использованием MD5 хеширования
2. **Взаимное влияние** - После инициализации применяется начальное взаимное влияние
3. **Прогрев** - Выполняется 32 шага обоих генераторов
4. **Генерация** - Каждая подпись генерируется с учетом динамического взаимного влияния между LCG и LFSR
5. **Нелинейное смешивание** - Применяется 3 раунда нелинейного преобразования
6. **Перестановка байтов** - Финальная перестановка байтов для усиления криптостойкости

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/crypto-signature.git
cd crypto-signature

# Установка зависимостей (если требуется)
pip install -r requirements.txt
```

## Использование

### Базовое использование

```python
from crypto_signature import CryptoSignatureGenerator

# Создание генератора (используется текущее время)
generator = CryptoSignatureGenerator()

# Генерация подписи
signature = generator.generate_signature()
print(signature)  # Выведет 16-символьную hex строку
```

### Использование с заданным timestamp

```python
# Создание генератора с конкретным timestamp
timestamp = 1234567890
generator = CryptoSignatureGenerator(timestamp)

# Генерация нескольких подписей
for i in range(10):
    signature = generator.generate_signature()
    print(f"Подпись {i+1}: {signature}")
```

### Сброс генератора

```python
# Сброс с новым timestamp
generator.reset()  # Используется текущее время
# или
generator.reset(1234567890)  # С заданным timestamp
```

## Запуск примера

```bash
python example.py
```

## Структура проекта

```
crypto_signature/
├── __init__.py              # Инициализация пакета
├── lcg.py                   # Модуль LCG
├── lfsr.py                  # Модуль LFSR
├── initialization.py        # Модуль инициализации
└── signature_generator.py   # Основной генератор подписей

example.py                   # Примеры использования
README.md                    # Документация
requirements.txt             # Зависимости
.gitignore                   # Git ignore файл
```

## Требования

- Python 3.7+
- Стандартная библиотека Python (hashlib, time)

## Лицензия

MIT License

## Автор

Разработчик криптоподписи
