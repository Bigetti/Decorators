import os
import datetime



def logger(old_function):

    func_name = old_function.__name__
    print(f"-------Была вызвана Функция {func_name} и для нее будет добавлена запись в лог, ")

    def new_function(*args, **kwargs):

        func_name = old_function.__name__
        print(f"Вызвана функция {func_name}")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Функция {func_name} была вызвана в {current_time}")

        args_str = ', '.join(map(str, args))
        kwargs_str = ', '.join(f'{k}={v!r}' for k, v in kwargs.items())

        with open('main.log', 'a') as f:
            f.write(f" была вызвана функция {func_name} в {current_time}\n")
            f.write(f'Аргументы: {args_str}, {kwargs_str}\n')

            result = old_function(*args, **kwargs)
            f.write(f'Результат: {result}\n')

        return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()