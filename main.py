from random import randint, choice
import matplotlib.pyplot as plt
import numpy as np

# Константи
TRACKS = 500
SECTORS_PER_TRACK = 100
MAX_SEEK_TIME = 130  # ms
TRACK_SEEK_TIME = 10  # ms
ROTATIONAL_LATENCY = 8  # ms

CACHE_SIZE = 250
WRITEBACK_TIME = 30  # seconds

MAX_REQUESTS = 20

READ = "READ"
WRITE = "WRITE"


# Додано параметри для генерації запитів
EXPONENTIAL_LAMBDA = 0.1
UNIFORM_MIN_REQUESTS = 2
UNIFORM_MAX_REQUESTS = 5

# Клас жорсткого диска
class HardDrive:
    def __init__(self):
        self.tracks = TRACKS
        self.position = 0

    def seek(self, track):
        diff = abs(self.position - track)
        seek_time = diff * TRACK_SEEK_TIME
        if diff == self.tracks - 1:
            seek_time = MAX_SEEK_TIME

        self.position = track

        return seek_time

    def read(self, track):
        seek_time = self.seek(track)
        rotation_time = ROTATIONAL_LATENCY
        return seek_time + rotation_time

    def write(self, track, data):
        seek_time = self.seek(track)
        rotation_time = ROTATIONAL_LATENCY
        # Запис даних
        return seek_time + rotation_time


# Кеш

# Базовий клас планувальника
class IOScheduler:
    def __init__(self):
        self.requests = []

    def add_request(self, request):
        # Додати запит в чергу
        self.requests.append(request)

    def dispatch_request(self):
        # Виконати запит
        if self.requests:
            return self.requests.pop(0)


# Планувальник FCFS
class FCFSScheduler(IOScheduler):
    def fcfs_schedule(self):
        # FCFS алгоритм
        return self.dispatch_request()


# Планувальник SSTF
class SSTFScheduler(IOScheduler):
    def sstf_schedule(self):
        # SSTF алгоритм
        current_track = 0  # Поточне положення головки
        min_distance = float('inf')
        selected_request = None

        for request in self.requests:
            distance = abs(request.block_num - current_track)
            if distance < min_distance:
                min_distance = distance
                selected_request = request

        self.requests.remove(selected_request)
        return selected_request


# Планувальник C-LOOK
class CLOOKScheduler(IOScheduler):
    def clook_schedule(self):
        # C-LOOK алгоритм
        current_track = 0  # Поточне положення головки
        sorted_requests = sorted(self.requests, key=lambda x: x.block_num)

        for request in sorted_requests:
            if request.block_num >= current_track:
                self.requests.remove(request)
                return request

        # Якщо дійшли до кінця диска, повертаємо перший запит
        selected_request = sorted_requests[0]
        self.requests.remove(selected_request)
        return selected_request


# Процес
class Process:
    def __init__(self, pid):
        self.pid = pid
        # Файл процесу
        pass

    def generate_request(self):
        # Генерувати запити
        operation = choice([READ, WRITE])
        block_num = randint(0, TRACKS * SECTORS_PER_TRACK - 1)
        return IORequest(self.pid, operation, block_num)


# Запит
class IORequest:
    def __init__(self, pid, operation, block_num):
        self.pid = pid
        self.operation = operation
        self.block_num = block_num


# Функція моделювання
# Функція моделювання
def simulate(scheduler):
    hard_drive = HardDrive()
    processes = [Process(pid) for pid in range(3)]  # Додайте більше процесів, якщо потрібно
    results = []
    last_completion_time = 0  # Додайте цю змінну

    for _ in range(MAX_REQUESTS):
        for process in processes:
            # Додано генерацію кількості запитів з експоненціальним розподілом
            num_requests = np.random.exponential(EXPONENTIAL_LAMBDA) + UNIFORM_MIN_REQUESTS
            for _ in range(int(num_requests)):
                request = process.generate_request()
                scheduler.add_request(request)

        while scheduler.requests:
            request = scheduler.dispatch_request()
            start_time = last_completion_time  # Використовуйте час завершення попереднього запиту як час початку поточного

            # Блок відсутній в кеші, читаємо з жорсткого диска
            seek_time = hard_drive.read(request.block_num)
            # Якщо цей блок не є модифікованим, додаємо його до кешу
            if request.operation == READ:
                # Логіка для читання, якщо потрібно
                pass
            elif request.operation == WRITE:
                # Логіка для запису, якщо потрібно
                pass

            # Записуємо результат запиту для подальшого аналізу
            end_time = start_time + seek_time  # Змінена логіка розрахунку часу
            completion_time = end_time - start_time
            results.append({'completion_time': completion_time})
            last_completion_time = end_time  # Оновлюємо час останнього завершення

    # Записуємо результати для подальшого аналізу
    return results



# Побудова графіків
def analyze_results(results, scheduler_name, max_requests):
    # Додано код для обробки результатів та побудови графіка
    completion_times = []
    for result in results:
        completion_times.append(result['completion_time'])

    # Побудова графіка з ідентифікатором планувальника та максимальною кількістю запитів
    plt.plot(completion_times, label=f'{scheduler_name} - {max_requests} Requests')
    plt.xlabel('Request Number')
    plt.ylabel('Time (ms)')
    plt.legend()



if __name__ == "__main__":
    max_requests_list = [10, 20, 30, 40, 50]

    for max_requests in max_requests_list:
        fcfs_scheduler = FCFSScheduler()
        sstf_scheduler = SSTFScheduler()
        clook_scheduler = CLOOKScheduler()

        fcfs_results = simulate(fcfs_scheduler)
        analyze_results(fcfs_results, 'FCFS', max_requests)

        sstf_results = simulate(sstf_scheduler)
        analyze_results(sstf_results, 'SSTF', max_requests)

        clook_results = simulate(clook_scheduler)
        analyze_results(clook_results, 'C-LOOK', max_requests)

        plt.xlabel('Request Number')
        plt.ylabel('Time (ms)')
        plt.legend()
        plt.show()  # Відображення графіків для кожного алгоритму та максимальної кількості запитів
