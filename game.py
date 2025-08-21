import pygame
import sys
from game_logic import GameLogic
from renderer import Renderer
from audio import toggle_bgm, play_sound_effect, footstep_sound

# Initialize pygame
pygame.init()

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

# Start BGM (initially on)
toggle_bgm()  # This will start the BGM

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Qキーで終了
                running = False
            elif event.key == pygame.K_r and game.game_over:
                game.restart()
            elif event.key == pygame.K_SPACE and game.game_clear:
                game.next_level()
            elif event.key == pygame.K_m:
                # Toggle BGM (on/off)
                bgm_state = toggle_bgm()

    # ゲームクリア時の処理は手動で行う（スペースキー）

    if not game.game_clear and not game.game_over:
        # キー入力処理
        keys = pygame.key.get_pressed()
        key_input = {
            "left": keys[pygame.K_LEFT],
            "right": keys[pygame.K_RIGHT],
            "up": keys[pygame.K_UP],
            "down": keys[pygame.K_DOWN],
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
