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


def create_bgm():
    duration = 6.0  # ゆったりとした童話風のテンポ
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # 童話風のメロディー（Fメジャー、優しい進行）
    # "きらきら星"や"メリーさんの羊"のような親しみやすい音程
    melody_freq = [349, 392, 440, 392, 349, 293, 349, 392, 440, 523, 440, 392]  # F-G-A-G-F-D-F-G-A-C-A-G
    note_duration = duration / len(melody_freq)
    melody = np.zeros_like(t)

    for i, freq in enumerate(melody_freq):
        start_idx = int(i * note_duration * sample_rate)
        end_idx = int((i + 1) * note_duration * sample_rate)
        if end_idx > len(t): end_idx = len(t)
        note_t = t[start_idx:end_idx] - t[start_idx]

        # 童話らしい柔らかなエンベロープ（ゆっくりとしたアタックとリリース）
        envelope = (1 - np.exp(-note_t * 5)) * np.exp(-note_t * 1.2)

        # オルゴール風の純粋なサイン波に少し倍音を加える
        wave = (np.sin(freq * 2 * np.pi * note_t) * 0.8 +
                np.sin(freq * 4 * np.pi * note_t) * 0.15 +
                np.sin(freq * 6 * np.pi * note_t) * 0.05)

        melody[start_idx:end_idx] = wave * envelope * 0.08

    # 優しいベースライン（童話の伴奏らしく単純で安定）
    bass_freq = [174, 220, 174, 220, 146, 196, 174, 220, 174, 261, 220, 196]  # F-A-F-A-D-G-F-A-F-C-A-G (1オクターブ下)
    bass = np.zeros_like(t)

    for i, freq in enumerate(bass_freq):
        start_idx = int(i * note_duration * sample_rate)
        end_idx = int((i + 1) * note_duration * sample_rate)
        if end_idx > len(t): end_idx = len(t)
        note_t = t[start_idx:end_idx] - t[start_idx]

        # ゆったりとしたベース
        envelope = (1 - np.exp(-note_t * 3)) * np.exp(-note_t * 0.8)
        wave = np.sin(freq * 2 * np.pi * note_t)
        bass[start_idx:end_idx] = wave * envelope * 0.05

    # 魔法のようなキラキラ音（高音域でスパークル効果）
    sparkle_freq = [1047, 1175, 1319, 1175, 1047, 880, 1047, 1175, 1319, 1568, 1319, 1175]  # 高音域のキラキラ
    sparkle = np.zeros_like(t)

    for i, freq in enumerate(sparkle_freq):
        start_idx = int(i * note_duration * sample_rate)
        end_idx = int((i + 1) * note_duration * sample_rate)
        if end_idx > len(t): end_idx = len(t)
        note_t = t[start_idx:end_idx] - t[start_idx]

        # キラキラ効果（短いアタック、長いリリース）
        envelope = np.exp(-note_t * 0.8) * (1 - np.exp(-note_t * 12))
        # 三角波風でより柔らかく
        wave = np.sin(freq * 2 * np.pi * note_t) * (1 - 2 * np.abs(np.sin(freq * np.pi * note_t)))
        sparkle[start_idx:end_idx] = wave * envelope * 0.03

    # 温かいパッド（童話の背景音）
    pad_freq = [349, 392, 440, 392, 349, 293, 349, 392, 440, 523, 440, 392]  # メロディと同じ音程
    pad = np.zeros_like(t)

    for i, freq in enumerate(pad_freq):
        start_idx = int(i * note_duration * sample_rate)
        end_idx = int((i + 1) * note_duration * sample_rate)
        if end_idx > len(t): end_idx = len(t)
        note_t = t[start_idx:end_idx] - t[start_idx]

        # 非常にゆっくりとしたエンベロープで背景を作る
        envelope = (1 - np.exp(-note_t * 2)) * np.exp(-note_t * 0.4)
        # 複数のサイン波を重ねて温かみを演出
        wave = (np.sin(freq * 2 * np.pi * note_t) * 0.4 +
                np.sin(freq * 2 * np.pi * note_t + np.pi/4) * 0.3 +
                np.sin(freq * 2 * np.pi * note_t + np.pi/2) * 0.3)
        pad[start_idx:end_idx] = wave * envelope * 0.04

    # ミックス
    bgm_wave = melody + bass + sparkle + pad

    # 童話らしい長めのフェードイン・アウト
    fade_samples = int(0.5 * sample_rate)
    bgm_wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
    bgm_wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)

    # 軽いコンプレッション（童話らしく優しく）
    bgm_wave = np.tanh(bgm_wave * 1.1) * 0.7

    # ステレオ化（左右で少し位相をずらして広がりを演出）
    left_channel = bgm_wave
    right_channel = bgm_wave * 0.95  # 右チャンネルを少し小さく
    stereo_wave = np.column_stack((left_channel, right_channel))

    # Pygameサウンドオブジェクトに変換
    sound = pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))
    return sound

footstep_sound = create_footstep_sound()
timer_sound = create_timer_sound()
explosion_sound = create_explosion_sound()
detection_sound = create_detection_sound()
bgm_sound = create_bgm()

# BGM状態管理 (0: BGM2, 1: 無音)
bgm_state = 0

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("頑張れ！ソ〇ニータイマー君！")
clock = pygame.time.Clock()

# ゲームロジックと描画を初期化
game = GameLogic()
renderer = Renderer(screen)

# BGM開始 (初期状態はBGM2)
bgm_sound.play(-1)  # 無限ループ再生

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
                game.next_level()
            elif event.key == pygame.K_m:
                # BGM 2状態切り替え (BGM2 → 無音 → BGM2)
                pygame.mixer.stop()
                bgm_state = (bgm_state + 1) % 2
                if bgm_state == 0:
                    bgm_sound.play(-1)  # BGM2再生
                # bgm_state == 1 の場合は無音（何も再生しない）

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
