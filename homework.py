class InfoMessage:
    """
    Информационное сообщение о тренировке.
    training_type — имя класса тренировки;
    duration — длительность тренировки в часах;
    distance — дистанция в километрах, преодоленная тренировку;
    speed — средняя скорость, с которой двигался пользователь;
    calories — килокалори, израсходованные тренировку.
    """
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:

        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        """Вернуть строку сообщения."""
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """
    Cодержит все основные свойства и методы для тренировок.
    Каждый класс, описывающий определённый вид тренировки,
    будет дополнять и расширять базовый класс.
    """

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    TIME_IN_MINUTE: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:

        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result: float = self.action * self.LEN_STEP / self.M_IN_KM
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result: float = self.get_distance() / self.duration
        return result

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        result: InfoMessage = InfoMessage(self.__class__.__name__,
                                          self.duration,
                                          self.get_distance(),
                                          self.get_mean_speed(),
                                          self.get_spent_calories())
        return result


class Running(Training):
    """
    Все свойства и методы этого класса наследуются от базового класса.
    Исключение составляет только метод расчёта калорий.
    """

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:

        super().__init__(action, duration, weight)

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    ALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Расход калорий для бега рассчитывается данной формуле."""
        result: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                         * self.get_mean_speed()
                         + self.ALORIES_MEAN_SPEED_SHIFT)
                         * self.weight / self.M_IN_KM
                         * self.duration * self.TIME_IN_MINUTE)
        return result


class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.
    Конструктор этого класса принимает дополнительный
    параметр height — рост спортсмена.
    """
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: int = 2
    COEFF_CALORIE_3: float = 0.029
    COEFF_M_IN_S: float = 0.278
    CONST_M_IN_S: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)

        self.height: float = height

    def get_spent_calories(self) -> float:
        """Расчёт калорий для этого класса проводится по такой формуле."""
        speed_m_in_s_power_2: float = ((self.get_mean_speed()
                                       * self.COEFF_M_IN_S)
                                       ** self.COEFF_CALORIE_2)
        h_in_m: float = self.duration * self.TIME_IN_MINUTE
        height_in_m: float = self.height / self.CONST_M_IN_S

        result: float = ((self.COEFF_CALORIE_1 * self.weight
                          + (speed_m_in_s_power_2 / height_in_m)
                          * self.COEFF_CALORIE_3 * self.weight) * h_in_m)
        return result


class Swimming(Training):
    """
    Тренировка: плавание.
    Конструктор класса Swimming, кроме свойств базового класса,
    принимает ещё два параметра:
    length_pool — длина бассейна в метрах;
    count_pool — сколько раз пользователь переплыл бассейн.
    Нужно переопределить не только метод расчёта калорий get_spent_calories(),
    но и метод get_mean_speed(), который рассчитывает среднюю скорость.
    """
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:

        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def get_mean_speed(self) -> float:
        """Формула расчёта средней скорости при плавании."""
        result: float = (self.length_pool * self.count_pool
                         / self.M_IN_KM / self.duration)
        return result

    def get_spent_calories(self) -> float:
        """Формула для расчёта израсходованных калорий."""
        result: float = ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                         * self.COEFF_CALORIE_2 * self.weight * self.duration)
        return result


def read_package(workout_type: str, data: list) -> Training:
    """
    Прочитать данные полученные от датчиков.
    Код тренировки: 'SWM'.
    Элементы списка: количество гребков,
                     время в часах,
                     вес пользователя,
                     длина бассейна,
                     сколько раз пользователь переплыл бассейн.
    Код тренировки: 'RUN'.
    Элементы списка: количество шагов,
                     время тренировки в часах,
                     вес пользователя.
    Код тренировки: 'WLK'.
    Элементы списка: количество шагов,
                     время тренировки в часах,
                     вес пользователя,
                     рост пользователя.
    """

    dict_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    result: dict = dict_training[workout_type](*data)
    return result


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':

    packages: list[tuple[str, list]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
