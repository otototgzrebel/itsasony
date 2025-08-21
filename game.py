import pygame
import sys
from game_logic import GameLogic
from renderer import Renderer

pygame.init()
pygame.mixer.init()

# 効果音作成
import numpy as np


def create_footstep_sound():
    duration = 0.1
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(200 * 2 * np.pi * t) * 0.3
    stereo_wave = np.column_stack((wave, wave))  # 左右チャンネルに複製
    sound = pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))
    return sound


def create_timer_sound():
    duration = 0.5
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(440 * 2 * np.pi * t) * 0.1  # 440Hz のタイマー音
    stereo_wave = np.column_stack((wave, wave))  # 左右チャンネルに複製
    sound = pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))
    return sound


def create_explosion_sound():
    duration = 0.6
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # ノイズベースの爆発音
    wave = np.random.uniform(-1, 1, t.shape) * np.exp(-5 * t)  # 減衰付きノイズ
    stereo_wave = np.column_stack((wave, wave))  # 左右チャンネルに複製

    sound = pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))
    return sound


def create_detection_sound():
    duration = 0.3
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(1000 * 2 * np.pi * t) * 0.3 * np.exp(-t * 2)  # 高周波＋減衰
    stereo_wave = np.column_stack((wave, wave))  # 左右チャンネルに複製
    sound = pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))
    return sound


footstep_sound = create_footstep_sound()
timer_sound = create_timer_sound()
explosion_sound = create_explosion_sound()
detection_sound = create_detection_sound()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("頑張れ！ソ〇ニータイマー君！")
clock = pygame.time.Clock()

# ゲームロジックと描画を初期化
game = GameLogic()
renderer = Renderer(screen)

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game.game_over:
                game.restart()
            elif event.key == pygame.K_SPACE and game.game_clear:
                game.game_clear = False

    # ゲームクリア時の自動進行
    if game.game_clear:
        pygame.time.wait(2000)
        game.game_clear = False

    if not game.game_clear and not game.game_over:
        # キー入力処理
        keys = pygame.key.get_pressed()
        key_input = {
            "left": keys[pygame.K_LEFT],
            "right": keys[pygame.K_RIGHT],
            "up": keys[pygame.K_UP],
            "down": keys[pygame.K_DOWN],
        }

        # ゲーム更新
        play_footstep = game.update_player(key_input)
        if play_footstep:
            footstep_sound.play()
        game.update_game()

        # 効果音再生
        for sound_event in game.sound_events:
            if sound_event == "timer_set":
                timer_sound.play()
            elif sound_event == "explosion":
                explosion_sound.play()
            elif sound_event == "detection":
                detection_sound.play()

    # 描画
    renderer.render_game(game)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
