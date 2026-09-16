import pygame

# 1. Структура узла Двоичного дерева поиска (BST)
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root

# Расчет пространственных координат для широкого дерева
def compute_positions(node, x, y, dx):
    if node is None:
        return
    node.x = x
    node.y = y
    compute_positions(node.left, x - dx, y + 65, dx / 2)
    compute_positions(node.right, x + dx, y + 65, dx / 2)

# Генератор шагов поиска по разветвленному дереву
def search_bst_visual(root, target):
    current = root
    path = []
    while current is not None:
        path.append(current)
        yield current, path, "checking"
        if current.key == target:
            yield current, path, "found"
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
    width, height = 1100, 750  # Увеличена ширина для большего числа ветвей
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Многоуровневый поиск в разветвленном BST")
    
    # Расширенный набор ключей для создания глубокого ветвления
    keys = [50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 45, 55, 68, 81, 93]
    root = None
    for k in keys:
        root = insert(root, k)
        
    compute_positions(root, width // 2, 50, 260)
    
    target_value = 45  # Искомый ключ в глубине ветвей
    search_gen = search_bst_visual(root, target_value)
    
    clock = pygame.time.Clock()
    running = True
    current_node = None
    search_path = []
    status = "running"
    
    def draw_tree(node):
        if node is None:
            return
        if node.left:
            pygame.draw.line(screen, (120, 120, 140), (node.x, node.y), (node.left.x, node.left.y), 2)
            draw_tree(node.left)
        if node.right:
            pygame.draw.line(screen, (120, 120, 140), (node.x, node.y), (node.right.x, node.right.y), 2)
            draw_tree(node.right)
            
        color = (100, 180, 255) # Синий
        if node in search_path:
            color = (255, 165, 0)   # Оранжевый (пройденный путь)
        if node == current_node:
            color = (255, 69, 0)    # Красный (текущий узел)
            if status == "found":
                color = (50, 205, 50) # Зеленый (найдено)
                
        pygame.draw.circle(screen, color, (int(node.x), int(node.y)), 22)
        
        font = pygame.font.SysFont(None, 22)
        text = font.render(str(node.key), True, (255, 255, 255))
        screen.blit(text, (node.x - 11, node.y - 11))

    while running:
        screen.fill((15, 15, 25))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        try:
            current_node, search_path, status = next(search_gen)
        except StopIteration:
            pass
            
        draw_tree(root)
        
        pygame.display.flip()
        clock.tick(1)
        
    pygame.quit()

if __name__ == "__main__":
    run_tree_search_visualization()
