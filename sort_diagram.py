mport random
import pygame

# 1. Шаг алгоритма сортировки с использованием генератора (Инструкция 1)
def insertion_sort_visual(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        yield arr, i, j  # Возвращаем кадр для подсветки активных элементов

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, i, j  # Кадр после сдвига

        arr[j + 1] = key
        yield arr, i, j + 1

# 2. Настройка графической визуализации на Pygame
def run_visualization():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Визуализация алгоритма сортировки (Инструкция 1)")
    
    # Генерация случайного массива данных
    data = [random.randint(10, 500) for _ in range(50)]
    sorting_gen = insertion_sort_visual(data)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill((30, 30, 30))  # Темный фон
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        try:
            # Получаем следующий шаг сортировки от генератора
            arr, active_i, active_j = next(sorting_gen)
        except StopIteration:
            # Сортировка завершена
            active_i, active_j = -1, -1

        # Отрисовка элементов массива в виде столбцов
        bar_width = width / len(data)
        for idx, val in enumerate(data):
            color = (100, 200, 255)  # Базовый цвет столбца
            if idx == active_i:
                color = (255, 100, 100)  # Активный элемент (key) — красный
            elif idx == active_j:
                color = (255, 255, 100)  # Сравниваемый элемент — желтый
                
            pygame.draw.rect(screen, color, (idx * bar_width, height - val, bar_width - 2, val))
            
        pygame.display.flip()
        clock.tick(30)  # Ограничение кадров в секунду для плавной анимации
        
    pygame.quit()

if __name__ == "__main__":
    run_visualization()
