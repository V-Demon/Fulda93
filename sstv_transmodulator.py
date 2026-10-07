#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
TRANSMODULATEUR SSTV v1.0 "ECHO-GUILLAUME"
Générateur de signal audio Martin M1 pour le Corpus MTT-2075
---------------------------------------------------------------------
Auteur      : @CyberNomad (d'après les specs du Ministère de la Cohérence)
Machine     : Tout terminal Python 3 (Recommandé: Robotron 1715 avec émulateur)
Usage       : python3 sstv_transmodulator.py <image.png> <output.wav>
Dépendance  : pip install Pillow
=====================================================================
NOTE : Ce script génère un signal SSTV Martin M1 valide. 
Le fichier WAV résultant peut être décodé par MMSSTV, RX-SSTV, QSSTV.
Fréquence porteuse simulée : 14.250 MHz (transposée en bande audio).
"""

import sys
import math
import wave
import struct
import array
from PIL import Image

# ---------------------------------------------------------------------
# 0. CONSTANTES DU PROTOCOLE MARTIN M1
# ---------------------------------------------------------------------
SAMPLE_RATE = 22050  # 22.05 kHz, standard rétro pour le SSTV
VIS_CODE = 44        # 44 = Martin M1 (320x256, couleur séquentielle)

# Durées en millisecondes
DUR_SYNC = 4.862
DUR_PORCH = 0.572
DUR_PIXEL = 0.4576
DUR_VIS_BIT = 30.0

# Fréquences en Hz
FREQ_SYNC = 1200
FREQ_PORCH = 1500
FREQ_VIS_START_STOP = 1900
FREQ_BIT_0 = 1300
FREQ_BIT_1 = 1100
FREQ_BLACK = 1500
FREQ_WHITE = 2300

# ---------------------------------------------------------------------
# 1. GÉNÉRATEUR DE TONS (Oscillateur sinusoïdal pur)
# ---------------------------------------------------------------------
def generate_tone(freq, duration_ms, sample_rate=SAMPLE_RATE):
    """Génère un tableau d'échantillons PCM 16-bit pour une fréquence donnée."""
    n_samples = int(sample_rate * (duration_ms / 1000.0))
    # Utilisation d'un array pour la performance
    samples = array.array('h', [0] * n_samples)
    for i in range(n_samples):
        # Phase simple, suffisante pour les décodeurs SSTV
        val = 32000.0 * math.sin(2.0 * math.pi * freq * (i / sample_rate))
        samples[i] = int(val)
    return samples

def generate_color_channel(pixels, sample_rate=SAMPLE_RATE):
    """Encode un canal de couleur (0-255) en fréquences 1500-2300 Hz."""
    n_samples_per_pixel = int(sample_rate * (DUR_PIXEL / 1000.0))
    # Taille totale du canal
    total_samples = len(pixels) * n_samples_per_pixel
    channel_samples = array.array('h', [0] * total_samples)
    
    idx = 0
    for p in pixels:
        # Mapping linéaire : 0 (noir) -> 1500Hz, 255 (blanc) -> 2300Hz
        freq = FREQ_BLACK + (p / 255.0) * (FREQ_WHITE - FREQ_BLACK)
        for i in range(n_samples_per_pixel):
            val = 32000.0 * math.sin(2.0 * math.pi * freq * (i / sample_rate))
            channel_samples[idx] = int(val)
            idx += 1
    return channel_samples

# ---------------------------------------------------------------------
# 2. EN-TÊTE VIS (Vertical Interval Signaling)
# ---------------------------------------------------------------------
def generate_vis_code(vis_code=VIS_CODE):
    """Génère le code VIS Martin M1."""
    samples = array.array('h')
    
    # Bit de start (1900 Hz)
    samples.extend(generate_tone(FREQ_VIS_START_STOP, DUR_VIS_BIT))
    
    # 8 bits de données (LSB en premier)
    for i in range(8):
        bit = (vis_code >> i) & 1
        freq = FREQ_BIT_1 if bit else FREQ_BIT_0
        samples.extend(generate_tone(freq, DUR_VIS_BIT))
        
    # Bit de parité (paire)
    parity = bin(vis_code).count('1') % 2
    freq = FREQ_BIT_1 if parity else FREQ_BIT_0
    samples.extend(generate_tone(freq, DUR_VIS_BIT))
    
    # Bit de stop (1900 Hz)
    samples.extend(generate_tone(FREQ_VIS_START_STOP, DUR_VIS_BIT))
    
    return samples

# ---------------------------------------------------------------------
# 3. GÉNÉRATION D'UNE LIGNE MARTIN M1
# ---------------------------------------------------------------------
def generate_line(green_pixels, blue_pixels, red_pixels):
    """Assemble une ligne complète : Sync + Porch + G + Porch + B + Porch + R + Porch."""
    line_samples = array.array('h')
    
    # Sync pulse
    line_samples.extend(generate_tone(FREQ_SYNC, DUR_SYNC))
    
    # Porch avant chaque couleur
    porch = generate_tone(FREQ_PORCH, DUR_PORCH)
    
    # Canal VERT
    line_samples.extend(porch)
    line_samples.extend(generate_color_channel(green_pixels))
    
    # Canal BLEU
    line_samples.extend(porch)
    line_samples.extend(generate_color_channel(blue_pixels))
    
    # Canal ROUGE
    line_samples.extend(porch)
    line_samples.extend(generate_color_channel(red_pixels))
    
    # Porch final de la ligne
    line_samples.extend(porch)
    
    return line_samples

# ---------------------------------------------------------------------
# 4. POINT D'ENTRÉE : ENCODAGE DE L'IMAGE
# ---------------------------------------------------------------------
def encode_sstv(image_path, output_path):
    print(f"[+] Chargement de l'image : {image_path}")
    img = Image.open(image_path).convert('RGB')
    
    # Martin M1 exige une résolution de 320x256
    print("[+] Redimensionnement vers 320x256 (Standard Martin M1)...")
    img = img.resize((320, 256), Image.Resampling.LANCZOS)
    
    width, height = img.size
    pixels = list(img.getdata())
    
    print("[+] Génération du code VIS (Martin M1)...")
    full_signal = generate_vis_code()
    
    print(f"[+] Encodage de {height} lignes... (Cela peut prendre quelques secondes)")
    for y in range(height):
        # Extraction des pixels de la ligne y
        line_pixels = pixels[y * width : (y + 1) * width]
        
        # Séparation des canaux (Martin M1 envoie dans l'ordre : Vert, Bleu, Rouge)
        green = [p[1] for p in line_pixels]
        blue  = [p[2] for p in line_pixels]
        red   = [p[0] for p in line_pixels]
        
        full_signal.extend(generate_line(green, blue, red))
        
        # Petite barre de progression "hacker"
        if (y + 1) % 32 == 0:
            pct = int(((y + 1) / height) * 100)
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            sys.stdout.write(f"\r    [{bar}] {pct}%")
            sys.stdout.flush()
    print("\n[+] Encodage terminé.")
    
    # Écriture du fichier WAV
    print(f"[+] Écriture du signal audio dans : {output_path}")
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(1)          # Mono
        wav_file.setsampwidth(2)          # 16-bit (2 bytes)
        wav_file.setframerate(SAMPLE_RATE)
        # Conversion en bytes pour le fichier WAV
        wav_file.writeframes(full_signal.tobytes())
        
    print(f"[+] SUCCÈS : Signal SSTV prêt pour transmission sur 14.250 MHz.")
    print("[+] Décodeurs recommandés : MMSSTV, RX-SSTV, QSSTV, Robot36.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 sstv_transmodulator.py <input_image.png> <output.wav>")
        print("Exemple: python3 sstv_transmodulator.py sstv_fulda_1993.png transmission_fulda.wav")
        sys.exit(1)
        
    encode_sstv(sys.argv[1], sys.argv[2])