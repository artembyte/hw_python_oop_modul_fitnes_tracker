class InfoMessage:
    """Информационное сообщение о тренировке."""
    # принимает 1 текстовое и 4 численных значения и выдает с ними сообщение
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories
    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
# принимает 3 численных значения, а выдает обьект класса InfoMessage с 1 текстовым 
# и 4 численными параметрами
    def __init__(self, action, duration, weight):
        self.action = action
        self.duration = duration
        self.weight = weight
    LEN_STEP = 0.65
    M_IN_KM = 1000
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration 

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self):
        return InfoMessage(self.__class__.__name__, self.duration, 
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())

# далее 3 подкласса принимают доп. параметры и корректируют свои функции 
# для подсчета правильных значений для InfoMessage
class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self):
        return ((18 * self.get_mean_speed() - 20) * 
                self.weight / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height
    def get_spent_calories(self):
        return ((0.035 * self.weight + (self.get_mean_speed() ** 2 // self.height) 
                 * 0.029 * self.weight) * self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    LEN_STEP = 1.38

    def get_mean_speed(self):
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration
    
    def get_spent_calories(self):
        return (self.get_mean_speed() + 1.1) * 2 * self.weight

# далее функция чтения данных, принимает 2 параметра: 1 текстовое и список с данными.
# выдает обьект одного из 3х подклассов с данными в параметрах.
# при ненайдении кода подкласса выдает ошибку и выполнение программы прерывается.
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_codes = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type in workout_codes:
        return workout_codes[workout_type](*data)
    raise ValueError(f'Тип тренировки {workout_type} пока не поддерживается')

def main(training: Training) -> None:
    """Главная функция."""
# принимает в параметре обьект одного из 3х подклассов,
# преобразует в обьект класса InfoMessage
# печатает результат функции по созданию сообщения в InfoMessage
    info = training.show_training_info()
    print(info.get_message())


# Проверка

if __name__ == '__main__':
# список с данными от датчиков
    packages = [
        ('RUN', [6200, 0.5, 75]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('SWM', [720, 1, 80, 25, 40])
    ]
# итерируем этот список, разделяя элемент списка на 2 обьекта из которых он состоит,
# и передавая их в функцию чтения данных read_package.
# далее полученный обьект подкласса передается в основную функцию main по созданию 
# и печати информационного сообщения. Потом следущий элемент списка данных так же.
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)