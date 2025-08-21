import pygame
import sys
from game_logic import GameLogic
from renderer import Renderer
from audio import toggle_bgm, play_sound_effect, footstep_sound

# Initialize pygame
pygame.init()
pygame.joystick.init()

# BGM状態管理 (0: BGM on, 1: silent)
bgm_state = 0

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("頑張れ！ソ〇ニータイマー君！")
clock = pygame.time.Clock()

# ゲームロジックと描画を初期化
game = GameLogic()
renderer = Renderer(screen)

# Gamepad setup (use the first detected joystick)
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# BGM starts ON by default (auto-started in audio.py on import)

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle hot-plugging of gamepads
        if event.type == pygame.JOYDEVICEADDED and joystick is None:
            try:
                joystick = pygame.joystick.Joystick(event.device_index)
                joystick.init()
            except Exception:
                joystick = None
        if event.type == pygame.JOYDEVICEREMOVED and joystick is not None:
            if event.instance_id == joystick.get_instance_id():
                joystick = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Qキーで終了
                running = False
            elif event.key == pygame.K_r and game.game_over:
                game.restart()
            elif event.key == pygame.K_SPACE and game.game_clear:
                game.next_level()
            elif event.key == pygame.K_SPACE and game.game_over:
                game.restart()
            elif event.key == pygame.K_m:
                # Toggle BGM (on/off)
                bgm_state = toggle_bgm()
        # Gamepad buttons
        if event.type == pygame.JOYBUTTONDOWN and joystick is not None:
            # Common Xbox layout: 0=A,1=B,2=X,3=Y,7=Start
            if event.button == 1:  # B -> quit
                running = False
            elif event.button == 0:
                if game.game_over:
                    game.restart()  # A -> restart when game over
                elif game.game_clear:
                    game.next_level()  # A -> next level when clear
            elif event.button == 3:  # Y -> toggle BGM
                bgm_state = toggle_bgm()

    # ゲームクリア時の処理は手動で行う（スペースキー）

    if not game.game_clear and not game.game_over:
        # キー入力処理 + ゲームパッド
        keys = pygame.key.get_pressed()
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        up = keys[pygame.K_UP]
        down = keys[pygame.K_DOWN]

        # Read gamepad axes/hat if available
        if joystick is not None:
            deadzone = 0.3
            try:
                ax_x = joystick.get_axis(0) if joystick.get_numaxes() > 0 else 0.0
                ax_y = joystick.get_axis(1) if joystick.get_numaxes() > 1 else 0.0
            except Exception:
                ax_x, ax_y = 0.0, 0.0
            hat_x, hat_y = 0, 0
            if joystick.get_numhats() > 0:
                hat = joystick.get_hat(0)
                hat_x, hat_y = hat[0], hat[1]

            # Axis mapping with deadzone
            left = left or (ax_x < -deadzone) or (hat_x < 0)
            right = right or (ax_x > deadzone) or (hat_x > 0)
            up = up or (ax_y < -deadzone) or (hat_y > 0)
            down = down or (ax_y > deadzone) or (hat_y < 0)

        key_input = {
            "left": left,
            "right": right,
            "up": up,
            "down": down,
        }

        # Update game state
        play_footstep = game.update_player(key_input)
        if play_footstep:
            play_sound_effect("footstep")
        
        game.update_game()
        
        # Play sound effects
        for sound_event in game.sound_events:
            play_sound_effect(sound_event)

    # 描画
    renderer.render_game(game)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
