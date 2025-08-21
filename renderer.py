import pygame

# 色定義
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
    
    def draw_player(self, x, y, direction, frame):
        # 人の形を描画（大きめ）
        # 頭
        pygame.draw.circle(self.screen, BLUE, (x + 15, y + 8), 6)
        
        # 体
        pygame.draw.rect(self.screen, BLUE, (x + 10, y + 14, 10, 12))
        
        # 手と足のアニメーション
        if direction == 'left':
            # 手
            pygame.draw.line(self.screen, BLUE, (x + 10, y + 17), (x + 5, y + 20 + frame), 3)
            pygame.draw.line(self.screen, BLUE, (x + 20, y + 17), (x + 25, y + 20 - frame), 3)
            # 足
            pygame.draw.line(self.screen, BLUE, (x + 12, y + 26), (x + 8, y + 30 + frame), 3)
            pygame.draw.line(self.screen, BLUE, (x + 18, y + 26), (x + 22, y + 30 - frame), 3)
        elif direction == 'right':
            # 手
            pygame.draw.line(self.screen, BLUE, (x + 10, y + 17), (x + 5, y + 20 - frame), 3)
            pygame.draw.line(self.screen, BLUE, (x + 20, y + 17), (x + 25, y + 20 + frame), 3)
            # 足
            pygame.draw.line(self.screen, BLUE, (x + 12, y + 26), (x + 8, y + 30 - frame), 3)
            pygame.draw.line(self.screen, BLUE, (x + 18, y + 26), (x + 22, y + 30 + frame), 3)
        elif direction == 'up':
            # 手
            pygame.draw.line(self.screen, BLUE, (x + 10, y + 17), (x + 8 + frame, y + 21), 3)
            pygame.draw.line(self.screen, BLUE, (x + 20, y + 17), (x + 22 - frame, y + 21), 3)
            # 足
            pygame.draw.line(self.screen, BLUE, (x + 12, y + 26), (x + 10 + frame, y + 30), 3)
            pygame.draw.line(self.screen, BLUE, (x + 18, y + 26), (x + 20 - frame, y + 30), 3)
        else:  # down
            # 手
            pygame.draw.line(self.screen, BLUE, (x + 10, y + 17), (x + 8 - frame, y + 21), 3)
            pygame.draw.line(self.screen, BLUE, (x + 20, y + 17), (x + 22 + frame, y + 21), 3)
            # 足
            pygame.draw.line(self.screen, BLUE, (x + 12, y + 26), (x + 10 - frame, y + 30), 3)
            pygame.draw.line(self.screen, BLUE, (x + 18, y + 26), (x + 20 + frame, y + 30), 3)
    
    def draw_serviceman(self, x, y):
        # サービスマンの人型（紫色）
        # 頭
        pygame.draw.circle(self.screen, PURPLE, (x + 15, y + 8), 6)
        
        # 体
        pygame.draw.rect(self.screen, PURPLE, (x + 10, y + 14, 10, 12))
        
        # 手（スパナを持っている）
        pygame.draw.line(self.screen, PURPLE, (x + 10, y + 17), (x + 5, y + 21), 3)
        pygame.draw.line(self.screen, PURPLE, (x + 20, y + 17), (x + 25, y + 21), 3)
        
        # スパナ（右手に）
        pygame.draw.line(self.screen, GRAY, (x + 25, y + 21), (x + 28, y + 18), 2)
        pygame.draw.circle(self.screen, GRAY, (x + 28, y + 18), 2)
        
        # 足
        pygame.draw.line(self.screen, PURPLE, (x + 12, y + 26), (x + 10, y + 30), 3)
        pygame.draw.line(self.screen, PURPLE, (x + 18, y + 26), (x + 20, y + 30), 3)
    
    def draw_appliance(self, appliance):
        x, y = appliance['x'], appliance['y']
        
        if appliance['exploded']:
            # 大きな爆発エフェクト
            pygame.draw.circle(self.screen, RED, (x+15, y+15), 60)
            pygame.draw.circle(self.screen, YELLOW, (x+15, y+15), 40)
            return
        
        # タイマー付きの場合は黄色で点滅
        timer_color = YELLOW if appliance['timer'] > 0 else None
        
        if appliance['type'] == 'tv':
            # テレビ
            pygame.draw.rect(self.screen, BLACK, (x, y, 30, 25))
            pygame.draw.rect(self.screen, GRAY if not timer_color else timer_color, (x+2, y+2, 26, 18))
            pygame.draw.rect(self.screen, BLACK, (x+12, y+20, 6, 5))
        elif appliance['type'] == 'radio':
            # ラジカセ
            pygame.draw.rect(self.screen, BLACK, (x, y, 30, 20))
            pygame.draw.rect(self.screen, GRAY if not timer_color else timer_color, (x+2, y+2, 26, 16))
            pygame.draw.circle(self.screen, BLACK, (x+8, y+10), 3)
            pygame.draw.circle(self.screen, BLACK, (x+22, y+10), 3)
        elif appliance['type'] == 'camera':
            # カメラ
            pygame.draw.rect(self.screen, BLACK, (x, y+5, 30, 20))
            pygame.draw.rect(self.screen, GRAY if not timer_color else timer_color, (x+2, y+7, 26, 16))
            pygame.draw.circle(self.screen, BLACK, (x+15, y+15), 6)
            pygame.draw.circle(self.screen, GRAY, (x+15, y+15), 4)
        elif appliance['type'] == 'walkman':
            # ウォークマン
            pygame.draw.rect(self.screen, BLACK, (x+5, y, 20, 25))
            pygame.draw.rect(self.screen, GRAY if not timer_color else timer_color, (x+7, y+2, 16, 21))
            pygame.draw.rect(self.screen, BLACK, (x+10, y+5, 10, 8))
            pygame.draw.circle(self.screen, BLACK, (x+12, y+18), 2)
            pygame.draw.circle(self.screen, BLACK, (x+18, y+18), 2)
    
    def draw_aibo(self, aibo):
        if not aibo or aibo.get('caught'):
            return
        x, y = aibo['x'], aibo['y']
        # Silver dachshund (metallic look)
        silver = (192, 192, 192)
        dark_silver = (140, 140, 140)
        highlight = (230, 230, 230)
        outline = (70, 70, 70)

        # Base body (long and low)
        body_rect = (x-4, y+6, 34, 12)
        pygame.draw.ellipse(self.screen, silver, body_rect)
        # Shading on body
        pygame.draw.ellipse(self.screen, dark_silver, (body_rect[0]+4, body_rect[1]+4, body_rect[2]-8, body_rect[3]-6))
        # Highlight on body
        pygame.draw.ellipse(self.screen, highlight, (body_rect[0]+6, body_rect[1]+2, body_rect[2]-20, 4))
        # Outline
        pygame.draw.ellipse(self.screen, outline, body_rect, 1)

        # Head (with long snout)
        head_center = (x+4, y+9)
        pygame.draw.circle(self.screen, silver, head_center, 6)
        pygame.draw.circle(self.screen, outline, head_center, 6, 1)
        # Snout
        pygame.draw.ellipse(self.screen, dark_silver, (x+6, y+9, 8, 4))
        pygame.draw.ellipse(self.screen, outline, (x+6, y+9, 8, 4), 1)
        # Nose
        pygame.draw.circle(self.screen, outline, (x+14, y+11), 2)
        # Eye
        pygame.draw.circle(self.screen, (20, 20, 20), (x+2, y+8), 1)

        # Floppy ear
        pygame.draw.polygon(self.screen, dark_silver, [(x+1, y+5), (x+4, y+8), (x+0, y+10)])
        pygame.draw.polygon(self.screen, outline, [(x+1, y+5), (x+4, y+8), (x+0, y+10)], 1)

        # Short legs
        leg_w, leg_h = 4, 4
        for lx in (x+2, x+12, x+22, x+30):
            pygame.draw.rect(self.screen, dark_silver, (lx, y+16, leg_w, leg_h))
            pygame.draw.rect(self.screen, outline, (lx, y+16, leg_w, leg_h), 1)

        # Thin tail
        pygame.draw.line(self.screen, outline, (x+30, y+12), (x+36, y+8), 2)

    def draw_puddle(self, puddle):
        x, y = puddle['x'], puddle['y']
        pee_color = (255, 215, 0)  # Gold
        pygame.draw.ellipse(self.screen, pee_color, (x-8, y-4, 16, 8))
    
    def render_game(self, game_logic):
        # 画面全体を緑色で塗りつぶし
        self.screen.fill((0, 128, 0))  # 緑色の背景
        
        # もこもこの草を画面全体に描画
        grass_height = 40
        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width()
        
        # 草の密度を上げるために間隔を狭く
        for y in range(0, screen_height, 20):  # 縦方向にも草を配置
            for x in range(-20, screen_width + 20, 8):  # 横方向の間隔をさらに狭く
                # 草の高さをランダムに変化させて自然な見た目に
                height_variation = y / screen_height * 0.5 + 0.5  # 下に行くほど高く
                current_height = int(grass_height * height_variation)
                
                # 草の色を少しずつ変化させて立体感を出す
                green_shade = max(0, min(255, 50 + y // 2))
                pygame.draw.arc(self.screen, (0, green_shade, 0), 
                              (x - 10, y - current_height//2, 30, current_height * 2), 
                              3.14, 6.28, 2)
        
        # 壁描画
        for wall in game_logic.walls:
            pygame.draw.rect(self.screen, (139, 69, 19), wall)  # 茶色の壁
        
        # しみ（おしっこ）描画
        for puddle in getattr(game_logic, 'puddles', []):
            self.draw_puddle(puddle)

        # 家電描画
        for appliance in game_logic.appliances:
            self.draw_appliance(appliance)
        
        # アイボ描画（複数対応）
        if hasattr(game_logic, 'aibos'):
            for a in game_logic.aibos:
                self.draw_aibo(a)
        else:
            self.draw_aibo(getattr(game_logic, 'aibo', None))
        
        # サービスマン描画
        for sm in game_logic.servicemen:
            if sm['alive']:
                self.draw_serviceman(sm['x'], sm['y'])
        
        # プレイヤー描画
        if not game_logic.game_over:
            self.draw_player(game_logic.player_x, game_logic.player_y, 
                           game_logic.player_direction, game_logic.walk_frame)
        
        # スコア表示
        score_text = self.font.render(f"Score: {game_logic.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # レベル表示
        level_text = self.font.render(f"Level: {game_logic.level}", True, BLACK)
        self.screen.blit(level_text, (10, 50))
        
        # BGM操作説明
        bgm_text = self.font.render("Press M to toggle BGM", True, BLACK)
        self.screen.blit(bgm_text, (10, 90))
        
        # ゲーム結果表示
        if game_logic.game_clear:
            text = self.big_font.render("CLEAR!", True, GREEN)
            self.screen.blit(text, (400-100, 300-36))
            restart_text = self.font.render("Press SPACE for Next Level", True, BLACK)
            self.screen.blit(restart_text, (400-150, 300+50))
        elif game_logic.game_over:
            text = self.big_font.render("GAME OVER", True, RED)
            self.screen.blit(text, (400-150, 300-36))
            restart_text = self.font.render("Press R to Restart", True, BLACK)
            self.screen.blit(restart_text, (400-150, 300+50))