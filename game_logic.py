import time
import random
import math

class GameLogic:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.player_x, self.player_y = 50, 50
        self.player_size = 30
        self.player_speed = 3
        self.player_direction = 'down'
        self.walk_frame = 0
        self.walk_timer = 0
        self.is_moving = False
        
        self.game_clear = False
        self.game_over = False
        self.score = 0
        self.level = 1
        self.speed_multiplier = 1.0
        
        self.sound_events = []
        
        self.walls = self.generate_maze()
        self.appliance_positions = self.generate_appliance_positions(self.walls)
        self.enemy_positions = self.generate_enemy_positions(self.walls)
        self.appliances = self.create_appliances()
        self.servicemen = self.create_servicemen()
    
    def generate_maze(self):
        walls = [(0, 0, 800, 20), (0, 0, 20, 600), (780, 0, 20, 600), (0, 580, 800, 20)]
        for _ in range(8):
            if random.choice([True, False]):
                x = random.randint(50, 600)
                y = random.randint(50, 550)
                w = random.randint(80, 200)
                walls.append((x, y, w, 20))
            else:
                x = random.randint(50, 750)
                y = random.randint(50, 400)
                h = random.randint(80, 200)
                walls.append((x, y, 20, h))
        return walls
    
    def generate_appliance_positions(self, walls):
        positions = []
        attempts = 0
        while len(positions) < 5 and attempts < 100:
            x = random.randint(50, 720)
            y = random.randint(50, 520)
            
            valid = True
            for wall in walls:
                if (x < wall[0] + wall[2] and x + 30 > wall[0] and
                    y < wall[1] + wall[3] and y + 30 > wall[1]):
                    valid = False
                    break
            
            if valid:
                for px, py in positions:
                    if abs(x - px) < 80 or abs(y - py) < 80:
                        valid = False
                        break
            
            if valid:
                positions.append((x, y))
            attempts += 1
        
        return positions
    
    def generate_enemy_positions(self, walls):
        positions = []
        attempts = 0
        while len(positions) < 4 and attempts < 500:
            x = random.randint(80, 680)
            y = random.randint(80, 480)
            
            valid = True
            for wall in walls:
                if (x < wall[0] + wall[2] and x + 30 > wall[0] and
                    y < wall[1] + wall[3] and y + 30 > wall[1]):
                    valid = False
                    break
            
            if valid:
                for px, py in self.appliance_positions:
                    if abs(x - px) < 50 or abs(y - py) < 50:
                        valid = False
                        break
                
                if valid:
                    for px, py in positions:
                        if abs(x - px) < 50 or abs(y - py) < 50:
                            valid = False
                            break
            
            if valid:
                positions.append((x, y))
            attempts += 1
        
        # 位置が不足の場合、最低限の数を確保
        if len(positions) == 0:
            positions = [(150, 200), (550, 200), (150, 400), (550, 400)]
        elif len(positions) < 4:
            safe_spots = [(150, 200), (550, 200), (150, 400), (550, 400)]
            for spot in safe_spots:
                if len(positions) >= 4:
                    break
                if spot not in positions:
                    positions.append(spot)
        
        return positions
    
    def create_appliances(self):
        appliances = []
        appliance_types = ['tv', 'radio', 'camera', 'walkman']
        for i, (x, y) in enumerate(self.appliance_positions):
            appliance_type = appliance_types[i % len(appliance_types)]
            appliances.append({'x': x, 'y': y, 'timer': 0, 'exploded': False, 'explode_time': 0, 'type': appliance_type})
        return appliances
    
    def create_servicemen(self):
        servicemen = []
        enemy_count = min(self.level, 4) if self.level % 4 != 0 else 4
        if self.level > 4:
            enemy_count = ((self.level - 1) % 4) + 1
        
        for i in range(enemy_count):
            if i < len(self.enemy_positions):
                x, y = self.enemy_positions[i]
                dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
                servicemen.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'alive': True, 'chasing': False})
        return servicemen
    
    def spawn_new_enemy(self):
        # 新しい敵を既存のポジションから選んで生成
        if self.enemy_positions:
            x, y = random.choice(self.enemy_positions)
            dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
            self.servicemen.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'alive': True, 'chasing': False})
    
    def check_collision(self, x, y, size):
        for wall in self.walls:
            if (x < wall[0] + wall[2] and x + size > wall[0] and
                y < wall[1] + wall[3] and y + size > wall[1]):
                return True
        return False
    
    def update_player(self, keys):
        new_x, new_y = self.player_x, self.player_y
        self.is_moving = False
        
        if keys['left']:
            new_x -= self.player_speed
            self.player_direction = 'left'
            self.is_moving = True
        if keys['right']:
            new_x += self.player_speed
            self.player_direction = 'right'
            self.is_moving = True
        if keys['up']:
            new_y -= self.player_speed
            self.player_direction = 'up'
            self.is_moving = True
        if keys['down']:
            new_y += self.player_speed
            self.player_direction = 'down'
            self.is_moving = True
        
        if not self.check_collision(new_x, self.player_y, self.player_size):
            self.player_x = new_x
        if not self.check_collision(self.player_x, new_y, self.player_size):
            self.player_y = new_y
        
        if self.is_moving:
            self.walk_timer += 1
            if self.walk_timer > 10:
                self.walk_frame = 1 if self.walk_frame == 0 else 0
                self.walk_timer = 0
                return True  # 足音再生フラグ
        else:
            self.walk_frame = 0
        return False
    
    def update_game(self):
        current_time = time.time()
        self.sound_events = []
        
        self.check_appliance_touch()
        self.move_servicemen()
        self.check_serviceman_appliance()
        
        for appliance in self.appliances:
            if appliance['timer'] > 0 and current_time - appliance['timer'] > 3 and not appliance['exploded']:
                appliance['exploded'] = True
                appliance['explode_time'] = current_time
                self.score += 100
                self.sound_events.append('explosion')
        
        self.check_explosion_damage()
        self.check_player_caught()
        
        # Check for level completion - all appliances must be exploded
        if all(a['exploded'] for a in self.appliances) and not self.game_clear:
            self.game_clear = True
        
        # Reset exploded appliances after game clear is processed
        for appliance in self.appliances:
            if appliance['exploded'] and current_time - appliance['explode_time'] > 5:
                appliance['exploded'] = False
    
    def check_appliance_touch(self):
        for appliance in self.appliances:
            if (not appliance['exploded'] and appliance['timer'] == 0 and
                self.player_x < appliance['x'] + 30 and self.player_x + self.player_size > appliance['x'] and
                self.player_y < appliance['y'] + 30 and self.player_y + self.player_size > appliance['y']):
                appliance['timer'] = time.time()
                self.sound_events.append('timer_set')
    
    def move_servicemen(self):
        detection_range = 120
        
        for sm in self.servicemen:
            if not sm['alive']:
                continue
            
            # 近くのタイマー付き家電を探す
            nearest_timer_appliance = None
            min_timer_distance = float('inf')
            
            for appliance in self.appliances:
                if appliance['timer'] > 0 and not appliance['exploded']:
                    distance = math.sqrt((sm['x'] - appliance['x'])**2 + (sm['y'] - appliance['y'])**2)
                    if distance < 150 and distance < min_timer_distance:
                        min_timer_distance = distance
                        nearest_timer_appliance = appliance
            
            # プレイヤーを発見したかチェック
            distance_to_player = math.sqrt((sm['x'] - self.player_x)**2 + (sm['y'] - self.player_y)**2)
            if distance_to_player < detection_range and not sm['chasing']:
                sm['chasing'] = True
                self.sound_events.append('detection')
            
            # 行動優先度: タイマー付き家電 > プレイヤー追跡
            if nearest_timer_appliance and random.random() < 0.7:  # 70%の確率でタイマーを優先
                dx = nearest_timer_appliance['x'] - sm['x']
                dy = nearest_timer_appliance['y'] - sm['y']
                if abs(dx) > abs(dy):
                    sm['dx'] = 1 if dx > 0 else -1
                    sm['dy'] = 0
                else:
                    sm['dx'] = 0
                    sm['dy'] = 1 if dy > 0 else -1
            elif sm['chasing']:
                dx = self.player_x - sm['x']
                dy = self.player_y - sm['y']
                if abs(dx) > abs(dy):
                    sm['dx'] = 1 if dx > 0 else -1
                    sm['dy'] = 0
                else:
                    sm['dx'] = 0
                    sm['dy'] = 1 if dy > 0 else -1
            
            move_speed = int(2 * self.speed_multiplier)
            new_x = sm['x'] + sm['dx'] * move_speed
            new_y = sm['y'] + sm['dy'] * move_speed
            
            explosion_blocked = False
            for appliance in self.appliances:
                if (appliance['exploded'] and
                    new_x < appliance['x'] + 60 and new_x + 20 > appliance['x'] - 30 and
                    new_y < appliance['y'] + 60 and new_y + 20 > appliance['y'] - 30):
                    explosion_blocked = True
                    break
            
            if (self.check_collision(new_x, sm['y'], 30) or new_x < 20 or new_x > 750 or explosion_blocked):
                if sm['chasing']:
                    sm['chasing'] = False
                sm['dx'] *= -1
            else:
                sm['x'] = new_x
                
            if (self.check_collision(sm['x'], new_y, 30) or new_y < 20 or new_y > 550 or explosion_blocked):
                if sm['chasing']:
                    sm['chasing'] = False
                sm['dy'] *= -1
            else:
                sm['y'] = new_y
    
    def check_serviceman_appliance(self):
        for sm in self.servicemen:
            if not sm['alive']:
                continue
            for appliance in self.appliances:
                if (appliance['timer'] > 0 and not appliance['exploded'] and
                    sm['x'] < appliance['x'] + 30 and sm['x'] + 30 > appliance['x'] and
                    sm['y'] < appliance['y'] + 30 and sm['y'] + 30 > appliance['y']):
                    appliance['timer'] = 0
    
    def check_explosion_damage(self):
        for appliance in self.appliances:
            if appliance['exploded']:
                for sm in self.servicemen:
                    if (sm['alive'] and
                        math.sqrt((sm['x']+10-appliance['x']-15)**2 + (sm['y']+10-appliance['y']-15)**2) < 60):
                        sm['alive'] = False
                        self.score += 500
                
                if (math.sqrt((self.player_x+10-appliance['x']-15)**2 + (self.player_y+10-appliance['y']-15)**2) < 60):
                    self.game_over = True
    
    def check_player_caught(self):
        for sm in self.servicemen:
            if (sm['alive'] and
                self.player_x < sm['x'] + 30 and self.player_x + self.player_size > sm['x'] and
                self.player_y < sm['y'] + 30 and self.player_y + self.player_size > sm['y']):
                self.game_over = True
    
    def next_level(self):
        self.level += 1
        self.score += 1000
        
        if self.level % 4 == 1 and self.level > 1:
            self.speed_multiplier += 0.5
        
        self.player_x, self.player_y = 50, 50
        self.player_direction = 'down'
        self.walk_frame = 0
        self.walk_timer = 0
        self.is_moving = False
        self.game_clear = False
        
        self.walls = self.generate_maze()
        self.appliance_positions = self.generate_appliance_positions(self.walls)
        self.enemy_positions = self.generate_enemy_positions(self.walls)
        self.appliances = self.create_appliances()
        self.servicemen = self.create_servicemen()
    
    def restart(self):
        self.player_x, self.player_y = 50, 50
        self.player_direction = 'down'
        self.walk_frame = 0
        self.walk_timer = 0
        self.is_moving = False
        self.game_clear = self.game_over = False
        self.score = 0
        self.level = 1
        self.speed_multiplier = 1.0
        
        self.walls = self.generate_maze()
        self.appliance_positions = self.generate_appliance_positions(self.walls)
        self.enemy_positions = self.generate_enemy_positions(self.walls)
        self.appliances = self.create_appliances()
        self.servicemen = self.create_servicemen()