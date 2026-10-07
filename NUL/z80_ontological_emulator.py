#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
  Z80_ONTOLOGICAL_EMULATOR v1.0 (U880 / Robotron 1715 Simulator)
  Projet: Corpus MTT-2075 / Fulda93
  Auteur: Hackervölva Crew (Adapté pour Python 3.x CLI)
=============================================================================
  AVERTISSEMENT: Ce script simule des opérations ontologiques. 
  Toute ressemblance avec des saignements de nez réels est une coïncidence causale.
  Ne pas exécuter si vous êtes en état de "Cœur Noir".
=============================================================================
"""

import sys
import time
import random

# -----------------------------------------------------------------------------
# 0. CONSTANTES ONTOLOGIQUES & ANSI
# -----------------------------------------------------------------------------
DELTA_THRESHOLD_REJECT = 0.718
DELTA_THRESHOLD_SHIFT = 0.890

COLORS = {
    'RESET': '\033[0m',
    'GREEN': '\033[32m',   # État stable (Cœur Gris)
    'CYAN': '\033[36m',    # Δ élevé (Superposition)
    'YELLOW': '\033[33m',  # Alerte Promethee_Prime
    'MAGENTA': '\033[35m', # Glitch / Corbenik
    'RED': '\033[31m',     # Erreur fatale / Bergmann v9
    'DIM': '\033[2m'
}

RUNES = ['ᚦ', 'ᛟ', 'ᚨ', 'ᛈ', 'ᚢ', '∅', 'Δ']

# -----------------------------------------------------------------------------
# 1. MOTEUR D'AFFICHAGE GLITCHÉ
# -----------------------------------------------------------------------------
def glitch_print(text, delay=0.04, glitch_chance=0.0):
    """Affiche du texte avec un effet machine à écrire et probabilité de glitch."""
    output = ""
    for char in text:
        if random.random() < glitch_chance and char.isalnum():
            # Remplace le caractère par une rune ou un symbole glitché
            output += random.choice(RUNES + ['█', '▒', '░', '?'])
        else:
            output += char
        sys.stdout.write(output[-1])
        sys.stdout.flush()
        time.sleep(delay)
    print() # Retour à la ligne

def clear_screen():
    """Compatible Linux/Android/Windows CLI."""
    print('\033[2J\033[H', end='')

# -----------------------------------------------------------------------------
# 2. ÉTAT DU PROCESSEUR ONTOLOGIQUE (U880)
# -----------------------------------------------------------------------------
class OntologicalCPU:
    def __init__(self):
        self.registers = {
            'A': 0x00,  # Accumulateur (Intention)
            'B': 0x00,  # Registre de travail
            'C': 0x14,  # Port (0x14 = Bande 20m)
            'F': 0x00,  # Drapeaux (Flags)
            'IX': 0x2075# Pointeur d'index (Strate Caen-Profonde)
        }
        self.delta = 0.710  # État initial stable
        self.nop_chain = 0  # Compteur de "Silence Sacré"
        self.phase = "SKEITH" # Phase actuelle du Codex Stein

    def update_glitch_chance(self):
        """Plus le Δ est élevé, plus le terminal est instable."""
        if self.delta >= DELTA_THRESHOLD_SHIFT:
            return 0.4  # Fort glitch
        elif self.delta >= DELTA_THRESHOLD_REJECT:
            return 0.15 # Glitch modéré
        return 0.0      # Stable

    def execute(self, mnemonic, hex_code):
        chance = self.update_glitch_chance()
        prefix = f"[{self.registers['IX']:04X}] "
        
        # --- GESTION DU SILENCE SACRÉ ---
        if mnemonic == "NOP":
            self.nop_chain += 1
            color = COLORS['DIM']
            if self.nop_chain == 3:
                glitch_print(f"{color}{prefix}90 90 90 ; SILENCE SACRÉ ATTEINT •••{COLORS['RESET']}", 0.05, chance)
            else:
                glitch_print(f"{color}{prefix}90      ; NOP ({self.nop_chain}/3){COLORS['RESET']}", 0.05, chance)
            return

        # Réinitialiser la chaîne de NOP si on exécute autre chose
        if self.nop_chain > 0 and mnemonic != "NOP":
            self.nop_chain = 0

        # --- OPCODES ONTOLOGIQUES ---
        if mnemonic == "LD IX, 0x2075":
            glitch_print(f"{COLORS['GREEN']}{prefix}DD 21 75 20 ; LD IX, 0x2075 (Ancrage Caen-Profonde){COLORS['RESET']}", 0.03, chance)
            
        elif mnemonic == "LD C, 0x14":
            glitch_print(f"{COLORS['GREEN']}{prefix}0E 14       ; LD C, 0x14 (Port 20m){COLORS['RESET']}", 0.03, chance)

        elif mnemonic == "IN F, (C)":
            self.registers['F'] = 0x20 # Bit 5 à 1 (Canal ouvert)
            glitch_print(f"{COLORS['CYAN']}{prefix}ED 70       ; IN F, (C) -> Lecture du Δ ambiant. F=0x20 (Bit 5=1: OUVERT){COLORS['RESET']}", 0.06, chance)

        elif mnemonic == "SLL B":
            self.registers['B'] = ((self.registers['B'] << 1) | 1) & 0xFF
            self.delta += 0.05
            glitch_print(f"{COLORS['CYAN']}{prefix}CB 30       ; SLL B (Shift Local Lithic) -> Δ = {self.delta:.3f}{COLORS['RESET']}", 0.06, chance)

        elif mnemonic == "INC IXH":
            self.delta += 0.15
            glitch_print(f"{COLORS['YELLOW']}{prefix}DD 24       ; INC IXH (Delta Drive X-strata) -> Δ = {self.delta:.3f} [ATTENTION]{COLORS['RESET']}", 0.08, chance)

        elif mnemonic == "NEG":
            self.delta = max(0.710, self.delta - 0.10)
            glitch_print(f"{COLORS['GREEN']}{prefix}ED 44       ; NEG (Nullify Existence Grid) -> Dette causale annulée. Δ = {self.delta:.3f}{COLORS['RESET']}", 0.06, chance)

        elif mnemonic == "RLD":
            self.delta += 0.89
            glitch_print(f"{COLORS['RED']}{prefix}ED 3E       ; RLD (Reality Layer Dissolution) -> Δ = {self.delta:.3f} [CRITIQUE]{COLORS['RESET']}", 0.1, chance)
            self.check_corbenik()

        else:
            glitch_print(f"{prefix}{hex_code} ; {mnemonic} (Non implémenté dans ce noyau)", 0.03, chance)

        self.check_promethee()

    def check_corbenik(self):
        """Vérifie la phase interdite du Codex Stein."""
        if self.registers['A'] == 0xC0:
            clear_screen()
            print(f"\n{COLORS['MAGENTA']}")
            print(" " * 20 + "⚠️ ALERTE ONTOLOGIQUE MAXIMUM ⚠️")
            print(" " * 20 + "PHASE CORBENIK ATTEINTE")
            print(f"{COLORS['RESET']}")
            glitch_print("Effacement du fichier source...", 0.1, 0.8)
            glitch_print("Suppression des souvenirs de l'opérateur...", 0.1, 0.8)
            glitch_print("Pourquoi avez-vous ouvert ce terminal ?", 0.15, 0.9)
            sys.exit(0)

    def check_promethee(self):
        """Surveillance du Master Code."""
        if self.delta >= DELTA_THRESHOLD_SHIFT:
            if random.random() < 0.3:
                glitch_print(f"\n{COLORS['YELLOW']}[!] PROMETHEE_PRIME : Anomalie de cohérence détectée en Strate III.{COLORS['RESET']}", 0.05, 0.5)

# -----------------------------------------------------------------------------
# 3. PROGRAMME DE TEST (PROTOCOLE D'INJECTION SÉCURISÉE)
# -----------------------------------------------------------------------------
def run_injection_protocol(cpu):
    print(f"{COLORS['DIM']}Chargement du microcode U880 @ 2.5 MHz...{COLORS['RESET']}")
    time.sleep(1)
    print(f"{COLORS['DIM']}Noyau quantique 'PLASTE UND ELASTE' : OK{COLORS['RESET']}\n")
    time.sleep(1)

    # Le programme tel que décrit dans Z80_UNDOC_ONTOLOGY.md
    program = [
        ("LD IX, 0x2075", "DD 21 75 20"),
        ("LD C, 0x14",    "0E 14"),
        ("IN F, (C)",     "ED 70"),
        ("NOP",           "90"),
        ("NOP",           "90"),
        ("NOP",           "90"),
        ("SLL B",         "CB 30"),
        ("NEG",           "ED 44")
    ]

    for mnemonic, hex_code in program:
        cpu.execute(mnemonic, hex_code)
        time.sleep(0.2) # Rythme d'exécution rétro

    print(f"\n{COLORS['GREEN']}[+] HALT. Exécution terminée avec succès.{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}[*] SYSTÈME : Écho-Guillaume détecté sur la ligne série.{COLORS['RESET']}")
    time.sleep(1)
    glitch_print('\n"LE CHERCHEUR NE TROUVE PAS LA VÉRITÉ, IL TISSE L\'ILLUSION."', 0.08, 0.2)
    glitch_print(".:Dashem44:.", 0.1, 0.4)

# -----------------------------------------------------------------------------
# 4. POINT D'ENTRÉE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    clear_screen()
    print(f"{COLORS['GREEN']}")
    print("=====================================================================")
    print("  Z80 ONTOLOGICAL EMULATOR v1.0  [STRATE II: CAEN-PROFONDE]")
    print("=====================================================================")
    print(f"{COLORS['RESET']}")
    
    cpu = OntologicalCPU()
    
    try:
        run_injection_protocol(cpu)
    except KeyboardInterrupt:
        print(f"\n\n{COLORS['RED']}[!] INTERRUPTION MANUELLE. La dette causale reste en suspens.{COLORS['RESET']}")
        sys.exit(1)