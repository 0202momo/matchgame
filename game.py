import pyxel
import random

pyxel.init(200, 200)
pyxel.mouse(True)

# 統合された画像ファイルをロード
pyxel.load("my_resource.pyxres")

image_size = 32  # 画像のサイズ（32px x 32px）
cursor_x = 90
cursor_y = 175
rect_size = 20
rect_color = 14

circles = []
is_space_pressed = False

# 初期画像の位置と座標
initial_image_coords = random.choice([(0, 0), (0, 32), (32, 0), (32, 32)])
initial_image_position = (85, 5)

# 画像の状態を保持する変数
displayed_image = None
score = 0
clicked_images = []

def is_duplicate(x, y):
    for circle in circles:
        if circle[0] == x and circle[1] == y:
            return True
    return False

# 現在選択されている画像
selected_image = None

def check_click():
    global score, circles, displayed_image, selected_image, initial_image_coords
    for circle in circles:
        x, y, coords = circle
        if (x - image_size // 2 <= pyxel.mouse_x <= x + image_size // 2 and 
            y - image_size // 2 <= pyxel.mouse_y <= y + image_size // 2 and
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and coords == initial_image_coords):

            # 新しい画像を選択
            if selected_image is None:
                selected_image = circle
            # 既に選択されている画像がある場合
            elif selected_image == circle:
                # 同じ画像をクリックした場合は選択解除
                selected_image = None
            else:
                # 異なる画像をクリックした場合、ペアをチェック
                if selected_image[2] == circle[2]:
                    score += 1
                    circles.remove(selected_image)
                    circles.remove(circle)
                    selected_image = None
                    initial_image_coords = random.choice([(0, 0), (0, 32), (32, 0), (32, 32)])  # 初期画像の更新
                    displayed_image = None  # 表示中の画像をリセット

def update():
    global is_space_pressed, displayed_image
    is_space_pressed = pyxel.btnp(pyxel.KEY_SPACE)

    # マウスのクリックをチェック
    check_click()

def draw():
    pyxel.cls(0)
    pyxel.rect(80, 5, 40, 40, 7)
    pyxel.rect(90, 175, 20, 20, 14)
    pyxel.line(40, 50, 160, 50, 4)
    pyxel.line(40, 90, 160, 90, 4)
    pyxel.line(40, 130, 160, 130, 4)
    pyxel.line(40, 170, 160, 170, 4)
    pyxel.line(40, 50, 40, 170, 4)
    pyxel.line(80, 50, 80, 170, 4)
    pyxel.line(120, 50, 120, 170, 4)
    pyxel.line(160, 50, 160, 170, 4)
    
    # 初期画像または更新された画像を描画
    image_coords = initial_image_coords
    pyxel.blt(initial_image_position[0], initial_image_position[1], 0, image_coords[0], image_coords[1], image_size, image_size, 0)

    # 画像を描画する部分
    if (
        90 <= pyxel.mouse_x <= 110
        and 175 <= pyxel.mouse_y <= 195
        and is_space_pressed
    ):
        max_attempts = 10
        for _ in range(max_attempts):
            x = random.choice([60, 100, 140])
            y = random.choice([70, 110, 150])
            image_coords = random.choice([(0, 0), (0, 32), (32, 0), (32, 32)])  # 画像の座標をランダムに選択

            if not is_duplicate(x, y):
                circles.append((x, y, image_coords))
                break

    for circle in circles:
        pyxel.blt(circle[0] - image_size // 2, circle[1] - image_size // 2, 0, circle[2][0], circle[2][1], image_size, image_size, 0)

    # スコアの描画
    pyxel.text(5, 5, f"Score: {score}", 7)

pyxel.run(update, draw)
