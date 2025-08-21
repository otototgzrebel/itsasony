import pygame
import numpy as np

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Sound effects
def create_footstep_sound():
    duration = 0.1
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(200 * 2 * np.pi * t) * 0.3
    stereo_wave = np.column_stack((wave, wave))  # Duplicate for stereo
    return pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))

def create_timer_sound():
    duration = 0.5
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(440 * 2 * np.pi * t) * 0.1  # 440Hz timer sound
    stereo_wave = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))

def create_explosion_sound():
    duration = 0.6
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.random.uniform(-1, 1, t.shape) * np.exp(-5 * t)  # Decaying noise
    stereo_wave = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))

def create_detection_sound():
    duration = 0.3
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(1000 * 2 * np.pi * t) * 0.3 * np.exp(-t * 2)  # High frequency + decay
    stereo_wave = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))

def create_bgm():
    duration = 6.0  # Gentle fairy tale tempo
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Melody (fairy tale-like)
    melody_notes = [523, 587, 659, 698, 784, 880, 784, 698, 659, 587, 523, 440]  # C5-D5-E5-F5-G5-A5-G5-F5-E5-D5-C5-A4
    melody = np.zeros_like(t)
    note_duration = duration / len(melody_notes)
    
    for i, freq in enumerate(melody_notes):
        start_idx = int(i * note_duration * sample_rate)
        end_idx = int((i + 1) * note_duration * sample_rate)
        if end_idx > len(t):
            end_idx = len(t)
        note_t = t[start_idx:end_idx] - t[start_idx]
        
        # Soft envelope for fairy tale feel
        envelope = (1 - np.exp(-note_t * 5)) * np.exp(-note_t * 1.5)
        wave = np.sin(freq * 2 * np.pi * note_t)
        melody[start_idx:end_idx] = wave * envelope * 0.1
    
    # Bass
    bass_notes = [130.8, 146.8, 164.8, 174.6, 196.0, 220.0, 196.0, 174.6, 164.8, 146.8, 130.8, 110.0]  # C3-D3-E3-F3-G3-A3-G3-F3-E3-D3-C3-A2
    bass = np.zeros_like(t)
    
    for i, freq in enumerate(bass_notes):
        start_idx = int(i * note_duration * sample_rate)
        end_idx = int((i + 1) * note_duration * sample_rate)
        if end_idx > len(t):
            end_idx = len(t)
        note_t = t[start_idx:end_idx] - t[start_idx]
        
        envelope = (1 - np.exp(-note_t * 3)) * np.exp(-note_t * 0.8)
        wave = np.sin(freq * 2 * np.pi * note_t)
        bass[start_idx:end_idx] = wave * envelope * 0.05
    
    # Sparkle effect (high frequencies)
    sparkle_freq = [1047, 1175, 1319, 1175, 1047, 880, 1047, 1175, 1319, 1568, 1319, 1175]
    sparkle = np.zeros_like(t)
    
    for i, freq in enumerate(sparkle_freq):
        start_idx = int(i * note_duration * sample_rate)
        end_idx = int((i + 1) * note_duration * sample_rate)
        if end_idx > len(t):
            end_idx = len(t)
        note_t = t[start_idx:end_idx] - t[start_idx]
        
        envelope = np.exp(-note_t * 0.8) * (1 - np.exp(-note_t * 12))
        wave = np.sin(freq * 2 * np.pi * note_t) * (1 - 2 * np.abs(np.sin(freq * np.pi * note_t)))
        sparkle[start_idx:end_idx] = wave * envelope * 0.03
    
    # Warm pad (background)
    pad_freq = [349, 392, 440, 392, 349, 293, 349, 392, 440, 523, 440, 392]
    pad = np.zeros_like(t)
    
    for i, freq in enumerate(pad_freq):
        start_idx = int(i * note_duration * sample_rate)
        end_idx = int((i + 1) * note_duration * sample_rate)
        if end_idx > len(t):
            end_idx = len(t)
        note_t = t[start_idx:end_idx] - t[start_idx]
        
        envelope = (1 - np.exp(-note_t * 2)) * np.exp(-note_t * 0.4)
        wave = (np.sin(freq * 2 * np.pi * note_t) * 0.4 +
                np.sin(freq * 2 * np.pi * note_t + np.pi/4) * 0.3 +
                np.sin(freq * 2 * np.pi * note_t + np.pi/2) * 0.3)
        pad[start_idx:end_idx] = wave * envelope * 0.04
    
    # Mix all layers
    bgm_wave = melody + bass + sparkle + pad
    
    # Fade in/out
    fade_samples = int(0.5 * sample_rate)
    bgm_wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
    bgm_wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    # Light compression
    bgm_wave = np.tanh(bgm_wave * 1.1) * 0.7
    
    # Create stereo effect
    left_channel = bgm_wave
    right_channel = bgm_wave * 0.95  # Slightly quieter in right channel
    stereo_wave = np.column_stack((left_channel, right_channel))
    
    return pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))

# Initialize sounds
footstep_sound = create_footstep_sound()
timer_sound = create_timer_sound()
explosion_sound = create_explosion_sound()
detection_sound = create_detection_sound()
bgm_sound = create_bgm()

# BGM state (0: BGM on, 1: silent)
bgm_state = 0

def toggle_bgm():
    """Toggle BGM on/off"""
    global bgm_state
    pygame.mixer.stop()
    bgm_state = (bgm_state + 1) % 2
    if bgm_state == 0:
        bgm_sound.play(-1)  # Loop BGM
    return bgm_state

def play_sound_effect(event):
    """Play sound effect based on event type"""
    if event == "timer_set":
        timer_sound.play()
    elif event == "explosion":
        explosion_sound.play()
    elif event == "detection":
        detection_sound.play()
    elif event == "footstep":
        footstep_sound.play()
