import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import math


def show_function_menu():
    # Меню вибору функцій
    print("Оберіть функція для інтегрування:")
    print("1. f(x) = x²")
    print("2. f(x) = sin(x)")
    print("3. f(x) = e^x")
    print("4. f(x) = 1/x")
    print("5. f(x) = cos(x)")
    print("6. Ввести власну функцію")
    print("=" * 50)


def get_function_choice():
# Вибір користувача
    while True:
        try:
            choice = int(input("Ваш вибір (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Будь ласка, введіть число від 1 до 6")
        except ValueError:
            print("Будь ласка, введіть ціле число")


def get_integration_limits():
# Межі інтегрування
    while True:
        try:
            a = float(input("Введіть нижню межу інтегрування a: "))
            b = float(input("Введіть верхню межу інтегрування b: "))

            if a >= b:
                print("Помилка: a повинно бути менше за b")
                continue

            return a, b
        except ValueError:
            print("Будь ласка, введіть числові значення")


def get_function(choice):
# Повертає обрану функцію та її аналітичний інтеграл
    functions = {
        1: {
            'func': lambda x: x ** 2,
            'integral': lambda x: x ** 3 / 3,
            'name': 'x²'
        },
        2: {
            'func': lambda x: np.sin(x),
            'integral': lambda x: -np.cos(x),
            'name': 'sin(x)'
        },
        3: {
            'func': lambda x: np.exp(x),
            'integral': lambda x: np.exp(x),
            'name': 'e^x'
        },
        4: {
            'func': lambda x: 1 / x,
            'integral': lambda x: np.log(abs(x)),
            'name': '1/x'
        },
        5: {
            'func': lambda x: np.cos(x),
            'integral': lambda x: np.sin(x),
            'name': 'cos(x)'
        }
    }

    if choice == 6:
        return get_custom_function()
    else:
        return functions[choice]

def get_custom_function():
# Функція користувача
    print("\nВведення власної функції")
    print("Приклад: для f(x) = x**2 + 2*x + 1 введіть: x**2 + 2*x + 1")

    while True:
        try:
            func_str = input("Введіть функцію f(x): ")
            # Створюємо функцію з введеного рядка
            func = lambda x: eval(func_str)

            # Тестуємо функцію
            test_value = 1.0
            result = func(test_value)

            print(f"Функція прийнята f(1) = {result}")

            return {
                'func': func,
                'integral': None,  # Аналітичний інтеграл невідомий
                'name': func_str
            }

        except Exception as e:
            print(f"Помилка у функції: {e}")
            print("Спробуйте ще раз")


def show_method_menu():
# меню вибору методу інтегрування
    print("\n" + "=" * 40)
    print("Оберіть метод інтегрування:")
    print("1. quad (адаптивний метод)")
    print("2. fixed_quad (фіксований порядок)")
    print("3. trapezoid (метод трапецій)")
    print("4. simpson (метод Сімпсона)")
    print("=" * 40)


def get_method_choice():
#Отримує вибір методу від користувача
    while True:
        try:
            choice = int(input("Ваш вибір (1-4): "))
            if 1 <= choice <= 4:
                return choice
            else:
                print("Будь ласка, введіть число від 1 до 4")
        except ValueError:
            print("Будь ласка, введіть ціле число")


def calculate_integral(func, a, b, method_choice):
# Обчислення інтеграла обраним методом
    methods = {
        1: lambda f, a, b: integrate.quad(f, a, b),
        2: lambda f, a, b: (integrate.fixed_quad(f, a, b, n=10)[0], 0),
        3: lambda f, a, b: (integrate.trapezoid(f, np.linspace(a, b, 1000)), 0),
        4: lambda f, a, b: (integrate.simpson(f, np.linspace(a, b, 1000)), 0)
    }

    method_names = {
        1: "quad (адаптивний)",
        2: "fixed_quad (фіксований порядок)",
        3: "trapezoid (трапеції)",
        4: "simpson (Сімпсона)"
    }

    try:
        result, error = methods[method_choice](func, a, b)
        return result, error, method_names[method_choice]
    except Exception as e:
        print(f"Помилка при обчисленні інтегралу: {e}")
        return None, None, None


def calculate_analytical_integral(integral_func, a, b):
# Обчислення аналітичного значення інтеграла
    try:
        if integral_func is None:
            return None
        return integral_func(b) - integral_func(a)
    except Exception as e:
        print(f"Не вдалося обчислити аналітичний інтеграл: {e}")
        return None


def plot_function(func, a, b, integral_value, func_name):
# Графік функції та заштриховує площу під кривою
    x = np.linspace(a, b, 1000)
    y = func(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {func_name}')
    plt.fill_between(x, y, alpha=0.3, color='blue',
                     label=f'Площа = {integral_value:.6f}')

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Графік функції f(x) = {func_name} та площа під кривою')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Межі інтегрування
    plt.axvline(a, color='red', linestyle='--', alpha=0.7, label=f'a = {a}')
    plt.axvline(b, color='green', linestyle='--', alpha=0.7, label=f'b = {b}')

    plt.tight_layout()
    return plt


def save_results(func_name, a, b, numerical_result, analytical_result, error, method_name):
# Збереження результату у текстовий файл
    filename = f"integral_results_{func_name.replace(' ', '_')}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Результат обчислення інтеграла\n")
        f.write("=" * 50 + "\n")
        f.write(f"Функція: f(x) = {func_name}\n")
        f.write(f"Межі інтегрування: [{a}, {b}]\n")
        f.write(f"Метод: {method_name}\n")
        f.write("-" * 50 + "\n")
        f.write(f"Чисельне значення: {numerical_result:.10f}\n")

        if analytical_result is not None:
            f.write(f"Аналітичне значення: {analytical_result:.10f}\n")
            f.write(f"Похибка: {error:.10f}\n")
            f.write(f"Відносна похибка: {abs(error / analytical_result) * 100:.6f}%\n")
        else:
            f.write("Аналітичне значення: не доступне\n")

        f.write("=" * 50 + "\n")

    print(f"\nРезультати збережено у файл: {filename}")


def main():
# Основна функція програми
    print("Програма для обчислення інтегралів")
    print("Використовує бібліотеку SciPy для чисельного інтегрування")

    try:
        # Вибір функції
        show_function_menu()
        func_choice = get_function_choice()
        func_data = get_function(func_choice)

        # Введення меж інтегрування
        print("\nВведіть межі інтегрування:")
        a, b = get_integration_limits()

        # Вибір методу
        show_method_menu()
        method_choice = get_method_choice()

        # Обчислення інтеграла
        print("\nОбчислення інтеграла")
        numerical_result, error_estimate, method_name = calculate_integral(
            func_data['func'], a, b, method_choice
        )

        if numerical_result is None:
            print("Не вдалося обчислити інтеграл")
            return

        # Обчислення аналітичного значення
        analytical_result = calculate_analytical_integral(func_data['integral'], a, b)

        # Обчислення похибки
        if analytical_result is not None:
            error = abs(numerical_result - analytical_result)
        else:
            error = None

        # Вивід результатів
        print("\n" + "=" * 60)
        print("Результати:")
        print("=" * 60)
        print(f"Функція: f(x) = {func_data['name']}")
        print(f"Інтеграл від {a} до {b}")
        print(f"Метод: {method_name}")
        print(f"Чисельне значення: {numerical_result:.8f}")

        if analytical_result is not None:
            print(f"Аналітичне значення: {analytical_result:.8f}")
            print(f"Похибка: {error:.8f}")
            print(f"Відносна похибка: {abs(error / analytical_result) * 100:.4f}%")
        else:
            print("Аналітичне значення: не доступне")

        # Побудова графіка
        print("\nГрафік")
        plt = plot_function(func_data['func'], a, b, numerical_result, func_data['name'])

        # Збереження результатів
        save_results(func_data['name'], a, b, numerical_result,
                     analytical_result, error, method_name)

        # Показ графіка
        plt.show()

        print("\nПрограма завершена")

    except KeyboardInterrupt:
        print("\n\nПрограму перервано користувачем")
    except Exception as e:
        print(f"\n\nСталася помилка: {e}")


if __name__ == "__main__":
    main()