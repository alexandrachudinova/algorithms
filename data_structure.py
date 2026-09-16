  import pygame

# 1. Структура узла Двоичного дерева поиска (BST)
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.x = 0  # Координата X для визуализации
        self.y = 0  # Координата Y для визуализации

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root

# Расчет пространственных координат узлов на плоскости
def compute_positions(node, x, y, dx):
    if node is None:
        return
    node.x = x
    node.y = y
    compute_positions(node.left, x - dx, y + 70, dx / 2)
    compute_positions(node.right, x + dx, y + 70, dx / 2)

# Генератор шагов поиска по дереву для визуализации
def search_bst_visual(root, target):
    current = root
    path = []
    while current is not None:
        path.append(current)
        yield current, path, "checking"  # Шаг проверки узла
        if current.key == target:
            yield current, path, "found"  # Элемент найден
            return True
        elif target < current.key:
            current = current.left
        else:
            current = current.right
    yield None, path, "not_found"
    return False

# 2. Функция запуска графической анимации Pygame
def run_tree_search_visualization():
    pygame.init()
    width, height = 900, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Пространственная визуализация поиска в BST")
    
    # Создаем тестовое дерево ключей
    keys = [50, 30, 70, 20, 40, 60, 80, 35]
    root = None
    for k in keys:
        root = insert(root, k)
        
    compute_positions(root, width // 2, 60, 200)
    
    target_value = 35  длину поиска
    search_gen = search_bst_visual(root, target_value)
    
    clock = pygame.time.Clock()
    running = True
    current_node = None
    search_path = []
    status = "running"
    
    # Вспомогательная функция для рекурсивной отрисовки графа дерева
    def draw_tree(node):
        if node is None:
            return
        if node.left:
            pygame.draw.line(screen, (150, 150, 150), (node.x, node.y), (node.left.x, node.left.y), 2)
            draw_tree(node.left)
        if node.right:
            pygame.draw.line(screen, (150, 150, 150), (node.x, node.y), (node.right.x, node.right.y), 2)
            draw_tree(node.right)
            
        # Цветовая индикация состояния узла
        color = (100, 180, 255) # Стандартный синий
        if node in search_path:
            color = (255, 165, 0)   # Оранжевый (путь поиска)
        if node == current_node:
            color = (255, 69, 0)    # Ярко-красный (активный узел)
            if status == "found":
                color = (50, 205, 50) # Зеленый при успешном поиске
                
        pygame.draw.circle(screen, color, (int(node.x), int(node.y)), 25)
        
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(node.key), True, (255, 255, 255))
        screen.blit(text, (node.x - 10, node.y - 10))

    while running:
        screen.fill((20, 20, 30))  # Темный футуристичный фон
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        try:
            current_node, search_path, status = next(search_gen)
        except StopIteration:
            pass
            
        draw_tree(root)
        
        pygame.display.flip()
        clock.tick(1)  # Замедление шагов анимации для наглядности (1 кадр в секунду)
        
    pygame.quit()

if __name__ == "__main__":
    run_tree_search_visualization()
