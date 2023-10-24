import os
import datetime



def logger(path):

    def __logger(old_function):

        def new_function(*args, **kwargs):

            func_name = old_function.__name__
            print(f"Обрабатываем функцию с именем {func_name}")
            current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f" Дата и время обработки {current_date_time}")

            args_str = ', '.join(map(str, args))
            kwargs_str = ', '.join(f'{k}={v!r}' for k, v in kwargs.items())

            with open(path, 'a') as f:
                f.write(f" Была вызвана функция {func_name} в {current_date_time}\n")
                f.write(f" Аргументы : {args_str}, {kwargs_str}\n")

                result = old_function(*args, **kwargs)
                f.write(f" Результат: {result}\n")
                print(f"Результат: {result}")

            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
