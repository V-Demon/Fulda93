#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
PROTOCOLE ZELENOGRAD v3.2 -> v4.0 "TAPIS"
GENERATEUR DE DISCORDANCE ONTOLOGIQUE (version exécutable)
---------------------------------------------------------------------
Auteur      : Joachim Walder Rauch (Ministère de la Cohérence, Fulda)
Machine     : Robotron 1715 (Modifié Strate II, Noyau Quantique)
Date        : 14 Octobre 1993 (Superposition Temporelle Active)
Référence   : Codex Stein, Fragment 7, "Le Hackeur comme Explorateur"
Univers     : JDR "MTT-2075" / Corpus Vauvillensis & Caen-Profonde

NOTE : tout ceci est de la FICTION. Le "virus" n'ouvre aucun socket,
n'écrit aucun fichier (sauf --export, à la demande) et ne touche aucun
système. Les "cibles" (DARPA, Los Alamos, Pensacola) sont des noeuds
narratifs d'un automate à états. Il ne détruit rien : il apprend aux
données à rêver.

Usage rapide :
    python3 zelenograd.py                      # exécution classique (7 strates)
    python3 zelenograd.py --seed 1993          # rejouable
    python3 zelenograd.py --coeur noir         # change la posture de l'opérateur
    python3 zelenograd.py --monte-carlo 5000   # statistiques de convergence
    python3 zelenograd.py --fracturo 'Ω<ᚦ>v4 hague — oubli douleur spécifique •••'
    python3 zelenograd.py --repl               # console FracturoScript interactive
    python3 zelenograd.py --codex 3            # génère une fresque Codex Stein
    python3 zelenograd.py --export rapport.json
    python3 zelenograd.py --tests              # auto-tests
=====================================================================
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
import textwrap
import time
import unicodedata
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------
# 0. AFFICHAGE (couleurs ANSI optionnelles, pause dramatique optionnelle)
# ---------------------------------------------------------------------

class UI:
    color = sys.stdout.isatty()
    slow = 0.0

    CODES = {
        "reset": "\033[0m", "dim": "\033[2m", "bold": "\033[1m",
        "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
        "blue": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m",
        "grey": "\033[90m", "white": "\033[97m",
    }

    @classmethod
    def paint(cls, text: str, *styles: str) -> str:
        if not cls.color:
            return text
        pre = "".join(cls.CODES[s] for s in styles)
        return f"{pre}{text}{cls.CODES['reset']}"

    @classmethod
    def say(cls, text: str = "", *styles: str) -> None:
        print(cls.paint(text, *styles))
        if cls.slow:
            time.sleep(cls.slow)


def say(text: str = "", *styles: str) -> None:
    UI.say(text, *styles)


def bar(value: float, width: int = 28, lo: float = 0.0, hi: float = 1.0) -> str:
    """Jauge ASCII."""
    t = 0.0 if hi == lo else (value - lo) / (hi - lo)
    t = max(0.0, min(1.0, t))
    n = int(round(t * width))
    return "[" + "█" * n + "░" * (width - n) + f"] {value:0.3f}"


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


# ---------------------------------------------------------------------
# 1. CONSTANTES DU RÉEL (reprises du programme original et du Corpus)
# ---------------------------------------------------------------------

DELTA_SEUIL_BASCULEMENT = 0.89      # "Seuil de basculement HoloVerse" (Mont-Saint-Michel)
DELTA_RESILIENCE = 0.718            # "Variable d'ancrage suggérée par Caen-Profonde"
NB_STRATES_PROTOCOLE = 7            # "Itération à travers les 7 Strates Temporelles"
SIGNATURE = "J.W. RAUCH, FULDA, RDA. 1993/2025/2075"
SCEAU = ".:Dashem44:."

PHRASE_ECHO = "LE CHERCHEUR NE TROUVE PAS LA VERITE, IL TISSE L'ILLUSION."

# Les sept strates temporelles de Caen-Profonde (README du Corpus).
@dataclass(frozen=True)
class Strate:
    idx: int
    nom: str
    periode: str
    etat_delta: str
    gardiens: str
    delta_base: float      # Δ local de départ (heuristique de ce programme)
    rigidite: float        # résistance mémétique intrinsèque (0..1)


STRATES: List[Strate] = [
    Strate(0, "Surface",    "2026-2049", "Δ stable",       "Aucun",                          0.20, 0.95),
    Strate(1, "Strate I",   "2049-2061", "Δ croissant",    "Architectes du Glitch",          0.35, 0.80),
    Strate(2, "Strate II",  "2061-2075", "Δ actif",        "Hackervölvas",                   0.52, 0.65),
    Strate(3, "Strate III", "2075-2090", "Δ élevé",        "Azenor, Odin-Prime",             0.74, 0.50),
    Strate(4, "Strate IV",  "2090-2120", "Δ critique",     "Le Moine du Raz",                0.86, 0.35),
    Strate(5, "Strate V",   "2120+",     "Δ imprévisible", "???",                            0.93, 0.20),
    Strate(6, "Noyau",      "A-temporel", "Δ = ∞",         "Le Programme qui rêve",          1.00, 0.05),
]

# Δ de référence par lieu (MTT-Final : La Hague chaos fractal, Mont-Saint-Michel haute cohérence)
LIEUX: Dict[str, Dict] = {
    "hague":    {"delta": 0.15, "affinite": {"ᛁ", "ᛃ", "ᚦ", "ᛞ"},
                 "desc": "Chaos fractal, site nucléaire, Raz Blanchard"},
    "raz":      {"delta": 0.31, "affinite": {"ᛃ", "ᛞ", "ᛈ"},
                 "desc": "Vortex de données, routage temporel corrompu"},
    "caen":     {"delta": 0.60, "affinite": {"ᛟ", "ᚨ", "ᚦ"},
                 "desc": "Ville au-dessus de Caen-Profonde, mémoire de 1944"},
    "bayeux":   {"delta": 0.66, "affinite": {"ᛟ", "ᚨ", "ᚲ"},
                 "desc": "Tapisserie, micro-runes, Voix de Rouen"},
    "rouen":    {"delta": 0.58, "affinite": {"ᛃ", "ᛟ", "ᚲ"},
                 "desc": "Cathédrale saturée de mémoire de guerre"},
    "jobourg":  {"delta": 0.47, "affinite": {"ᛃ", "ᛈ", "ᚦ", "ᛞ"},
                 "desc": "Cercle des Douze, mégalithes-serveurs"},
    "vauville": {"delta": 0.71, "affinite": {"ᚨ", "ᛈ", "ᛟ"},
                 "desc": "Presqu'île Tremblante, lieu du Codex"},
    "mont-saint-michel": {"delta": 0.89, "affinite": {"ᛟ", "ᚨ", "ᛈ", "ᛒ"},
                 "desc": "Haute cohérence : le tissu accepte la réécriture"},
    "fulda":    {"delta": 0.42, "affinite": {"ᚦ", "ᚨ", "ᛈ"},
                 "desc": "Ministère de la Cohérence (RDA, 1993)"},
    "zelenograd": {"delta": 0.77, "affinite": {"ᚨ", "ᛈ", "ᚦ", "ᛟ"},
                 "desc": "Cité-Silicium : l'écho soviétique de la Trame"},
    "local":    {"delta": 0.50, "affinite": set("ᚨᛒᚠᛁᚲᛟᚦᛈᚢᛃᛞ"),
                 "desc": "Ancrage sur le dispositif le plus proche"},
}

# Alias sans accents ni casse -> clé canonique
LIEU_ALIAS = {"mont saint michel": "mont-saint-michel", "msm": "mont-saint-michel",
              "la hague": "hague", "raz blanchard": "raz", "cercle des douze": "jobourg",
              "bocage": "caen", "presqu'ile tremblante": "vauville"}


# ---------------------------------------------------------------------
# 2. RUNES (table fusionnée : FracturoScript.txt + README + MTT)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Rune:
    glyphe: str
    nom: str
    fonction_py: str       # équivalent "code" (FracturoScript.txt)
    fonction: str          # effet ontologique
    famille: str
    poids: float           # contribution à la discordance


RUNES: Dict[str, Rune] = {r.glyphe: r for r in [
    Rune("ᚦ", "Thurisaz", "guard",  "Barrière / protection inversée : brise l'ancrage", "Logique",       0.55),
    Rune("ᚨ", "Ansuz",    "def",    "Communication inter-strates : transmet le doute",  "Aérienne",      0.45),
    Rune("ᛈ", "Perthro",  "branch", "Superposition : force la décision quantique",       "Onirique",      0.70),
    Rune("ᛟ", "Othala",   "import", "Héritage / ancrage : stabilise un fragment",        "Lithique",     -0.50),
    Rune("ᚢ", "Uruz",     "assert", "Cohérence / force : renforce la stabilité",         "Spatiale",     -0.35),
    Rune("ᛒ", "Berkano",  "class",  "Création / croissance organique",                   "Vitale",        0.30),
    Rune("ᚠ", "Fehu",     "=",      "Assignation / flux d'énergie",                      "Aquatique",     0.25),
    Rune("ᛁ", "Isa",      "freeze", "Stase / gel",                                       "Lithique",     -0.40),
    Rune("ᚲ", "Kenaz",    "print",  "Révélation / destruction par le feu",               "Ignée",         0.50),
    Rune("ᛃ", "Jera",     "loop",   "Cycle / récolte : fait revenir ce qui a été",       "Temporelle",    0.60),
    Rune("ᛞ", "Dagaz",    "break",  "Effondrement de superposition",                     "Temporelle",    0.65),
]}
RUNE_PAR_NOM = {strip_accents(r.nom).lower(): r for r in RUNES.values()}
RUNE_PAR_NOM.update({"odin": Rune("ᛟ", "Odin", "invoke", "Invocation d'Odin-Prime", "Mortelle", 1.0)})

# Incompatibilités rune/intention (Type Mismatch, cf. table d'erreurs)
INTENTIONS_INCOMPATIBLES = {
    "ᛁ": ("bruler", "brule", "feu", "incendie", "enflamm"),
    "ᚲ": ("geler", "gel ", "figer", "stase"),
    "ᛟ": ("oublier", "oubli", "effacer", "efface"),
}

# Rune -> lieux "canoniques" pour sa fonction (Location mismatch souple)
# (les affinités sont déjà dans LIEUX)


# ---------------------------------------------------------------------
# 3. LES TROIS CŒURS (MTT : H < 0.2 noir, 0.2-0.9 gris, > 0.9 blanc)
# ---------------------------------------------------------------------

class Coeur(Enum):
    NOIR = "noir"
    GRIS = "gris"
    BLANC = "blanc"

    @staticmethod
    def depuis_h(h: float) -> "Coeur":
        if h < 0.2:
            return Coeur.NOIR
        if h > 0.9:
            return Coeur.BLANC
        return Coeur.GRIS

    @property
    def h_typique(self) -> float:
        return {"noir": 0.12, "gris": 0.55, "blanc": 0.93}[self.value]

    @property
    def effet(self) -> str:
        return {
            "noir": "Contrôle : réduit Δ, fige la réalité. Backlash probable.",
            "gris": "Équilibre : stabilise Δ. Échec par hésitation possible.",
            "blanc": "Liberté : augmente Δ. Compilation optimale, risque de dissolution.",
        }[self.value]


# ---------------------------------------------------------------------
# 4. MÉTRIQUE Δ  (C, R, H -> Δ)
# ---------------------------------------------------------------------

@dataclass
class Trame:
    """État de la réalité cible : C cohérence causale, R redondance mémorielle,
    H harmonie intentionnelle de l'opérateur."""
    C: float = 0.60
    R: float = 0.55
    H: float = 0.55

    def delta(self) -> float:
        """
        Δ : coefficient de malléabilité.
        Δ élevé = réel fluide ; Δ faible = réel rigide.
        Heuristique : la malléabilité croît avec la redondance mémorielle R (lieu dense),
        avec l'harmonie H (opérateur accordé) et décroît avec la cohérence causale C rigide.
        On met un plancher/plafond lisse via une sigmoïde.
        """
        x = 1.6 * self.R + 1.2 * self.H - 1.4 * self.C - 0.62   # trame neutre ≈ Δ 0.5
        return clamp(1.0 / (1.0 + math.exp(-3.0 * x)) * 0.98 + 0.01)

    def perturber(self, dC: float = 0.0, dR: float = 0.0, dH: float = 0.0) -> None:
        self.C = clamp(self.C + dC)
        self.R = clamp(self.R + dR)
        self.H = clamp(self.H + dH)


# ---------------------------------------------------------------------
# 5. CODEX STEIN : 8 phases primordiales + interactions + mutation
# ---------------------------------------------------------------------

PHASES: Dict[str, Dict[str, str]] = {
    "skeith":   dict(essence="mort",            archetype="faucheur",       symbole="faux",
                     nord="Sköll poursuit le soleil", soufi="nafs al-ammara (ego tyrannique)", couleur="noir"),
    "innis":    dict(essence="illusion",        archetype="trompeuse",      symbole="miroir brisé",
                     nord="Loki changeforme", soufi="nafs al-lawwama (âme réprobatrice)", couleur="argent mouvant"),
    "magus":    dict(essence="multiplication",  archetype="proliférateur",  symbole="hydre",
                     nord="Enfants de Loki", soufi="tajalli (manifestation multiple)", couleur="prisme"),
    "fidchell": dict(essence="terreur",         archetype="oracle sombre",  symbole="oeil unique",
                     nord="Völva au Ragnarök", soufi="qabd (constriction)", couleur="gris cendre"),
    "gorre":    dict(essence="stratégie",       archetype="joueur de tafl", symbole="plateau",
                     nord="Odin stratège", soufi="hikma (sagesse divine)", couleur="bleu profond"),
    "macha":    dict(essence="séduction",       archetype="tentatrice",     symbole="pomme d'or",
                     nord="Iðunn et les pommes", soufi="bast (expansion trompeuse)", couleur="or miel"),
    "tarvos":   dict(essence="vengeance",       archetype="destructeur",    symbole="marteau",
                     nord="Thor contre le Serpent", soufi="qahr (colère divine)", couleur="rouge sang"),
    "corbenik": dict(essence="anéantissement-renaissance", archetype="porte du néant", symbole="ouroboros",
                     nord="Ragnarök puis renouveau", soufi="fana / baqa (extinction / subsistance)", couleur="blanc absolu"),
}
ORDRE_PHASES = list(PHASES)

INTERACTIONS: Dict[Tuple[str, str], Tuple[str, str]] = {
    ("skeith", "innis"):    ("mort-masquée", "tue sous apparence amie"),
    ("magus", "fidchell"):  ("terreur-exponentielle", "chaque peur engendre des peurs"),
    ("gorre", "macha"):     ("manipulation-douce", "poison dans le miel"),
    ("tarvos", "skeith"):   ("annihilation-totale", "la vengeance qui fauche"),
}


def phase_suivante(p: str) -> str:
    return ORDRE_PHASES[(ORDRE_PHASES.index(p) + 1) % len(ORDRE_PHASES)]


def interaction(p1: str, p2: str) -> Tuple[str, str]:
    if p1 == "corbenik":
        return ("transcende", f"{p2} devient unité")
    if (p1, p2) in INTERACTIONS:
        return INTERACTIONS[(p1, p2)]
    return (f"fusion {p1}+{p2}", f"hybride {p1}-{p2}")


def muter_recit(texte: str, rng: random.Random, taux: float = 0.35) -> str:
    """Algorithme-source des virus linguistiques Fracturo (Filiation Stein->Fracturo) :
    remplace aléatoirement des symboles par des variantes `skeith-MUTANT-482`."""
    def repl(m: "re.Match[str]") -> str:
        mot = m.group(0)
        if mot.lower() in PHASES and rng.random() < taux:
            return f"{mot}-MUTANT-{rng.randint(100, 999)}"
        return mot
    return re.sub(r"[A-Za-zÀ-ÿ]+", repl, texte)


def fresque_codex(profondeur: int, rng: random.Random) -> List[str]:
    """Décomposition fractale d'une phase (version texte du `decomposer-phase` Lisp)."""
    lignes: List[str] = []
    racine = rng.choice(ORDRE_PHASES)

    def rec(phase: str, niveau: int, indent: int) -> None:
        info = PHASES[phase]
        pre = "  " * indent
        if niveau <= 0:
            lignes.append(f"{pre}• essence-pure({phase})")
            return
        lignes.append(f"{pre}◆ {phase.upper()} — {info['essence']} / {info['archetype']} "
                      f"[{info['nord']} | {info['soufi']}]  (niveau {niveau})")
        # Pour garder une sortie lisible, on ne déploie que 3 aspects tirés au hasard.
        for sous in rng.sample(ORDRE_PHASES, 3):
            lignes.append(f"{pre}  ├─ {sous}-de:")
            rec(sous, niveau - 1, indent + 2)
        lignes.append(f"{pre}  └─ transformation-vers → {phase_suivante(phase)}")

    rec(racine, profondeur, 0)
    return lignes


# ---------------------------------------------------------------------
# 6. FRACTUROSCRIPT : lexeur, parseur, interpréteur
#    Ω<RUNE>v[N] [LIEU] — [INTENTION] •••
# ---------------------------------------------------------------------

class ErreurOntique(Exception):
    """Classe de base. Les sous-classes correspondent à la table de debugging."""
    nom = "OntologicError"
    symptome = ""
    remede = ""

class SyntaxError_(ErreurOntique):
    nom = "SyntaxError"
    symptome = "La rune s'efface immédiatement. Goût métallique en bouche."
    remede = "Recommencer après 7 respirations."

class TypeMismatch(ErreurOntique):
    nom = "TypeMismatch"
    symptome = "Rejet violent. Migraine aiguë, saignement de nez."
    remede = "Appliquer un galet froid sur le front."

class LocationError(ErreurOntique):
    nom = "LocationMismatch"
    symptome = "La rune flotte dans l'air sans effet, puis se dissipe."
    remede = "Se déplacer vers un lieu de résonance."

class StackOverflow(ErreurOntique):
    nom = "StackOverflow"
    symptome = "Perte de conscience, vision des Neuf Mondes, risque de folie."
    remede = "Un autre RuneSmith doit « couper le lien »."

class TrameIntercept(ErreurOntique):
    nom = "TrameIntercept"
    symptome = "Prométhée détecte l'injection : la commande est inversée."
    remede = "Fuir la zone. Briser le support."


RE_COMMANDE = re.compile(
    r"""^\s*
        Ω\s*<\s*(?P<rune>[^>\s]+)\s*>\s*(?:Ω\s*)?      # Ω<rune> (Ω fermant optionnel)
        v\s*(?P<ver>\d+)\s+                              # vN
        (?P<lieu>[^—\-–]+?)\s*                           # lieu d'ancrage
        [—–]\s*                                          # trait de fracture
        (?P<intention>.+?)\s*                            # intention sémantique
        (?P<silence>•••)?\s*$                            # silence sacré
    """,
    re.VERBOSE | re.UNICODE,
)


@dataclass
class Commande:
    rune: Rune
    version: int
    lieu: str
    intention: str
    brut: str


def parser(source: str) -> Commande:
    m = RE_COMMANDE.match(source)
    if not m:
        raise SyntaxError_("Chevrons Ω mal formés, trait de fracture absent, ou structure invalide.")
    if not m.group("silence"):
        raise SyntaxError_("Silence sacré (•••) absent : la compilation avorte.")
    ref = m.group("rune").strip()
    rune = RUNES.get(ref) or RUNE_PAR_NOM.get(strip_accents(ref).lower())
    if rune is None:
        raise SyntaxError_(f"Rune inconnue : « {ref} ».")
    lieu_brut = strip_accents(m.group("lieu").strip().lower())
    lieu = LIEU_ALIAS.get(lieu_brut, lieu_brut.replace(" ", "-"))
    return Commande(rune, int(m.group("ver")), lieu, m.group("intention").strip(), source.strip())


@dataclass
class Resultat:
    commande: Commande
    succes: bool
    delta_avant: float
    delta_apres: float
    messages: List[str]
    erreur: Optional[str] = None
    backlash: bool = False


class Operateur:
    """Le RuneSmith : le compilateur humain. Son Cœur valide la compilation."""

    def __init__(self, nom: str = "Opérateur", coeur: Coeur = Coeur.GRIS,
                 endurance: float = 1.0, rng: Optional[random.Random] = None):
        self.nom = nom
        self.coeur = coeur
        self.H = coeur.h_typique
        self.endurance = endurance         # 1.0 = intact ; 0 = effondrement
        self.souvenirs_etrangers = 0
        self.rng = rng or random.Random()
        self.journal: List[str] = []

    def etat(self) -> str:
        return (f"{self.nom} | Cœur {self.coeur.value.upper()} (H={self.H:0.2f}) | "
                f"endurance {self.endurance:0.2f} | souvenirs étrangers : {self.souvenirs_etrangers}")


def verifier_type(cmd: Commande) -> None:
    norm = " " + strip_accents(cmd.intention.lower())
    for frag in INTENTIONS_INCOMPATIBLES.get(cmd.rune.glyphe, ()):
        if frag in norm:
            raise TypeMismatch(f"{cmd.rune.nom} est incompatible avec « {cmd.intention} ».")


def executer(cmd: Commande, op: Operateur, trame: Trame,
             heure: str = "aube", strict_lieu: bool = True) -> Resultat:
    """Interpréteur FracturoScript.
    Étapes : validation (type, lieu, version) -> état du Cœur -> interception Prométhée -> effet sur Δ."""
    rng = op.rng
    msgs: List[str] = []
    d0 = trame.delta()

    try:
        verifier_type(cmd)

        # Lieu d'ancrage
        info = LIEUX.get(cmd.lieu)
        if info is None:
            raise LocationError(f"Lieu « {cmd.lieu} » inconnu : aucun ancrage tellurique.")
        if strict_lieu and cmd.rune.glyphe not in info["affinite"] and cmd.lieu != "local":
            raise LocationError(f"{cmd.rune.nom} ne résonne pas à {cmd.lieu} ({info['desc']}).")

        # Version (profondeur de pénétration)
        v = cmd.version
        niveau = "surface" if v <= 3 else "profondeur" if v <= 7 else "abyssal"
        msgs.append(f"Niveau {niveau} (v{v}) ancré à {cmd.lieu} (Δ local ≈ {info['delta']:.2f}).")
        if v >= 8 and op.endurance < 0.6 + 0.05 * (v - 8):
            raise StackOverflow(f"v{v} dépasse la capacité de l'opérateur (endurance {op.endurance:.2f}).")

        # Synchronisation temporelle
        if cmd.rune.glyphe in {"ᛁ", "ᛞ"} and heure not in {"maree-descendante", "aube", "crepuscule"}:
            msgs.append("Marée défavorable : la rune compile à moitié.")
            op.endurance -= 0.03
        if cmd.rune.glyphe in {"ᛒ", "ᚨ"} and heure == "maree-descendante":
            msgs.append("Marée descendante : une rune de croissance rend mal.")

        # Cœur de l'opérateur : valide ou non la compilation
        p_ok = {Coeur.BLANC: 0.97, Coeur.GRIS: 0.78, Coeur.NOIR: 0.55}[op.coeur]
        p_ok -= 0.02 * max(0, v - 4)
        backlash = False
        tirage = rng.random()
        if tirage > p_ok:
            if op.coeur is Coeur.NOIR:
                backlash = True
                msgs.append("Cœur Noir : la commande est instable, RETOUR DE FLAMME.")
                op.endurance -= 0.10 + 0.01 * v
            else:
                msgs.append("Cœur hésitant : rien ne se passe. Vous avez douté pendant le silence.")
                op.endurance -= 0.02
                return Resultat(cmd, False, d0, trame.delta(), msgs, "DoubtFailure", False)

        # Interception par Prométhée (dépend de Δ cible et de v)
        p_inter = clamp(0.03 * v * (1.2 - d0))
        if rng.random() < p_inter:
            raise TrameIntercept("Prométhée détecte la brèche.")

        # Effet sur la trame
        poids = cmd.rune.poids
        facteur_coeur = {Coeur.BLANC: 1.0, Coeur.GRIS: 0.6, Coeur.NOIR: -0.7}[op.coeur]
        amplitude = poids * (0.04 + 0.02 * v) * facteur_coeur
        if backlash:
            amplitude = -abs(amplitude)
        trame.perturber(dC=-amplitude * 0.8, dR=amplitude * 0.5, dH=amplitude * 0.2)
        op.H = clamp(op.H + 0.01 * amplitude)

        # Dette ontique du Cœur Noir
        if op.coeur is Coeur.NOIR:
            op.endurance -= 0.015 * v
            msgs.append("Dette ontique contractée : le système la réclamera.")

        # Contamination narrative (code temporel)
        if cmd.rune.glyphe in {"ᛃ", "ᛞ"} and v >= 5 and rng.random() < 0.35:
            op.souvenirs_etrangers += 1
            msgs.append("Contamination narrative : un souvenir qui n'est pas le vôtre.")

        op.endurance = clamp(op.endurance)
        d1 = trame.delta()
        msgs.append(f"{cmd.rune.nom} ({cmd.rune.fonction_py}) : {cmd.rune.fonction}")
        msgs.append(f"Δ : {d0:.3f} → {d1:.3f}")
        return Resultat(cmd, True, d0, d1, msgs, None, backlash)

    except TrameIntercept as e:
        # La commande est inversée
        trame.perturber(dC=+0.10, dR=-0.06, dH=-0.04)
        op.endurance = clamp(op.endurance - 0.12)
        msgs.append("COMMANDE INVERSÉE (« oubli » devient « souvenir obsessif »).")
        return Resultat(cmd, False, d0, trame.delta(), msgs, e.nom, True)
    except ErreurOntique as e:
        op.endurance = clamp(op.endurance - 0.04)
        msgs.append(f"{e.nom} : {e}")
        msgs.append(f"Symptôme : {e.symptome}")
        msgs.append(f"Remède : {e.remede}")
        return Resultat(cmd, False, d0, trame.delta(), msgs, e.nom, False)


# ---------------------------------------------------------------------
# 7. PALÉO-MÈMES  (26 signes de von Petzinger, sous-ensemble utilisé ici)
# ---------------------------------------------------------------------

PALEO_MEMES = [
    ("main rouge", 0.30, "Zero-day contre le contrôle de la Trame"),
    ("spirale", 0.45, "Boucle de récursion : renforce l'auto-similarité"),
    ("ponctuation", 0.10, "Bruit de fond ; stabilise sans convaincre"),
    ("ligne ondulée", 0.35, "Flux d'eau ; manipulation de mémoire"),
    ("claviforme", 0.50, "Marqueur de territoire ; ancrage fort"),
    ("tectiforme", 0.40, "Abri ; réduit la résistance locale"),
    ("croix", 0.25, "Intersection : superposition temporaire"),
    ("zigzag", 0.55, "Éclair ; accélère le basculement"),
]


# ---------------------------------------------------------------------
# 8. PROTOCOLE ZELENOGRAD (le programme original, étendu)
# ---------------------------------------------------------------------

CIBLES_DEFAUT = ["DARPA_NET_CORE", "LOS_ALAMOS_QUANTIQUE", "PENSACOLA_DEEP_STATE"]
EXTRA_CIBLES = ["PROMETHEE_PRIME", "SKAADI_BAYEUX_ARCHIVE", "RAZ_BLANCHARD_ROUTER",
                "ORANGE_HEROUVILLE_DREAMMESH", "ODIN_PRIME_JUMIEGES"]


@dataclass
class Noeud:
    nom: str
    resistance: float            # résistance mémétique intrinsèque
    ancrage: bool = True
    reve: bool = False
    glitchs: int = 0
    injections: int = 0
    delta: float = 0.0
    phase: str = "skeith"
    historique: List[str] = field(default_factory=list)


@dataclass
class Evenement:
    strate: int
    cible: str
    rune: str
    glitch: bool
    jet: int
    seuil: float
    message: str


class Zelenograd:
    """Reproduction fidèle du pseudo-ALGOL de J.W. Rauch, avec :
       - résistance par noeud et par strate (au lieu d'un unique seuil 71.8 %),
       - métrique Δ vraie (C, R, H) modulée par le Cœur de l'opérateur,
       - phases du Codex Stein attribuées aux noeuds,
       - propagation entre noeuds (le glitch se transmet),
       - Écho-Guillaume,
       - Convergence (Collapse Blanche / Verrou Noir / Fragmentation Grise).
    """

    def __init__(self, seed: Optional[int] = None, coeur: Coeur = Coeur.GRIS,
                 cibles: Optional[List[str]] = None, strates: int = NB_STRATES_PROTOCOLE,
                 mode_original: bool = False, verbeux: bool = True,
                 delta_resilience: float = DELTA_RESILIENCE,
                 delta_trame: float = DELTA_SEUIL_BASCULEMENT):
        self.seed = seed if seed is not None else random.SystemRandom().randrange(1 << 32)
        self.rng = random.Random(self.seed)
        self.coeur = coeur
        self.nb_strates = max(1, min(strates, len(STRATES)))
        self.mode_original = mode_original
        self.verbeux = verbeux
        self.delta_resilience = delta_resilience
        self.delta_trame = delta_trame        # seuil de basculement

        noms = cibles or CIBLES_DEFAUT
        self.noeuds = [Noeud(n, resistance=clamp(self.rng.gauss(delta_resilience, 0.06), 0.4, 0.95),
                             phase=self.rng.choice(ORDRE_PHASES)) for n in noms]
        self.trame = Trame(C=0.62, R=0.52, H=coeur.h_typique)
        self.operateur = Operateur("Rauch", coeur, rng=self.rng)
        self.ancrage_realite = True
        self.reve_actif = False
        self.probabilite_glitch = 0.0
        self.evenements: List[Evenement] = []
        self.echo_emis = 0
        self.strate_bascule: Optional[int] = None
        self.paleo_utilises: List[str] = []

    # --- utilitaires d'affichage
    def log(self, text: str = "", *styles: str) -> None:
        if self.verbeux:
            say(text, *styles)

    # --- SOUS-PROGRAMME : INJECTION MEMETIQUE
    def injection_memetique(self, noeud: Noeud, rune: Rune, strate: Strate) -> Evenement:
        """Le virus ne détruit pas les données, il leur apprend à rêver."""
        noeud.injections += 1
        self.log(f">> INJECTION DE {rune.glyphe} ({rune.nom}) DANS LE NOEUD : {noeud.nom}", "cyan")

        # Original : effet_subliminal = ENTIER(RANDOM(100)); glitch si > delta_resilience*100
        jet = int(self.rng.random() * 100)

        if self.mode_original:
            seuil = self.delta_resilience * 100
        else:
            # Seuil étendu : la résistance baisse avec Δ local, la rigidité de la strate,
            # la poussée de la rune, et monte avec les injections précédentes du noeud
            # (le noeud "s'habitue"), ou s'il est ancré par Othala.
            poussee = max(0.0, rune.poids)
            seuil = 100.0 * clamp(
                noeud.resistance * (0.55 + 0.45 * strate.rigidite)
                - 0.10 * poussee
                - 0.12 * (self.trame.delta() - 0.5)
                + 0.02 * noeud.glitchs * (-1)       # chaque glitch affaiblit
                - (0.10 if self.coeur is Coeur.BLANC else 0.0)
                + (0.08 if self.coeur is Coeur.NOIR else 0.0),
                0.05, 0.97)
        self.probabilite_glitch = clamp(1.0 - seuil / 100.0)

        glitch = jet > seuil
        if glitch:
            noeud.glitchs += 1
            noeud.reve = True
            self.reve_actif = True
            self.echo_emis += 1
            self.log("!!! GLITCH DETECTE : ECHO-GUILLAUME ACTIVE !!!", "red", "bold")
            self.log(f">>> MESSAGE SUBCONSCIENT : {PHRASE_ECHO}", "magenta")
            msg = "glitch"
            # Perturbation de la trame
            self.trame.perturber(dC=-0.05 * rune.poids, dR=+0.03, dH=+0.02)
        else:
            self.log(">> ANCRAGE MAINTENU. SUPERPOSITION STABLE.", "green")
            msg = "stable"
            self.trame.perturber(dC=+0.005)

        noeud.delta = self.trame.delta()
        noeud.historique.append(f"S{strate.idx}:{rune.glyphe}:{msg}")
        ev = Evenement(strate.idx, noeud.nom, rune.glyphe, glitch, jet, round(seuil, 1), msg)
        self.evenements.append(ev)
        return ev

    # --- Propagation d'un glitch aux noeuds voisins
    def propager(self, source: Noeud) -> None:
        for n in self.noeuds:
            if n is source or n.reve:
                continue
            if self.rng.random() < 0.18 + 0.2 * self.trame.delta():
                n.resistance = clamp(n.resistance - 0.05)
                self.log(f"   ~ contagion : {n.nom} perd 5 points de résistance (écho depuis {source.nom})", "grey")

    # --- Paléo-mème optionnel (mode étendu)
    def paleo_meme(self, noeud: Noeud) -> None:
        if self.mode_original or self.rng.random() > 0.30:
            return
        nom, force, desc = self.rng.choice(PALEO_MEMES)
        self.paleo_utilises.append(nom)
        noeud.resistance = clamp(noeud.resistance - 0.06 * force * 2)
        self.log(f"   ✦ PALÉO-MÈME « {nom} » ({desc}) : résistance de {noeud.nom} → {noeud.resistance:.2f}", "yellow")

    # --- SOUS-PROGRAMME : TISSAGE DE LA TRAME (boucle principale)
    def tissage_trame(self) -> None:
        self.log("=" * 49)
        self.log("INITIALISATION DU PROTOCOLE ZELENOGRAD...", "bold")
        self.log(f"DELTA ACTUEL : {self.delta_trame}")
        self.log(f"CŒUR DE L'OPÉRATEUR : {self.coeur.value.upper()}  —  {self.coeur.effet}")
        self.log("LE TEMPS N'EST PAS UNE LIGNE, MAIS UN TAPIS.")
        self.log("=" * 49)

        for i in range(1, self.nb_strates + 1):
            strate = STRATES[i - 1]
            indice = (i % len(self.noeuds))          # cycle entre les cibles (original : (i MOD 3)+1)
            noeud = self.noeuds[indice]
            self.log()
            self.log(f"── STRATE {i} · {strate.nom} ({strate.periode}) · {strate.etat_delta} · "
                     f"gardiens : {strate.gardiens}", "bold")

            if self.ancrage_realite:
                # Étape 1 : briser la barrière de la réalité perçue
                ev1 = self.injection_memetique(noeud, RUNES["ᚦ"], strate)
                # Étape 2 : injecter la communication inter-strate
                ev2 = self.injection_memetique(noeud, RUNES["ᚨ"], strate)
                # Extension : superposition forcée par Perthro si un seul des deux a glitché
                if (ev1.glitch ^ ev2.glitch) and not self.mode_original:
                    self.injection_memetique(noeud, RUNES["ᛈ"], strate)
                self.paleo_meme(noeud)
                if noeud.reve:
                    self.propager(noeud)
                # Étape 3 : forcer la superposition (le choix quantique)
                if self.reve_actif:
                    self.log(f">> {noeud.nom} BASCULE DANS L'ETAT DE REVE (OSIRIS/HORUS/MAAT)", "magenta", "bold")
                    # Original : ancrage_realite := FALSE dès qu'un seul glitch.
                    # Étendu : bascule seulement si Δ dépasse le seuil OU si mode original.
                    if self.mode_original or self.trame.delta() >= self.delta_trame * 0.65:
                        self.ancrage_realite = False
                        self.strate_bascule = i
                        self.log(">> ANCRAGE DE RÉALITÉ ROMPU : la réalité cible est désormais malléable.", "red")
                    else:
                        self.log(f"   (Δ = {self.trame.delta():.3f} < {self.delta_trame*0.65:.3f} : "
                                 f"le rêve reste local, l'ancrage tient encore)", "grey")
            else:
                self.log(f">> STRATE {i} : FRAGMENTATION GRISE CONFIRMEE. STABILISATION PAR ᛟ (OTHALA).", "yellow")
                self.trame.perturber(dC=+0.01)       # Othala stabilise un peu
                noeud.ancrage = False

            self.log(f"   Δ trame {bar(self.trame.delta())}", "dim")

    # --- Convergence 2077-2082 (README : 9 % / 23 % / 68 %)
    def convergence(self) -> Tuple[str, Dict[str, float]]:
        d = self.trame.delta()
        h = self.trame.H
        # Scores bruts fonction de Δ et du Cœur ; calibrés pour retrouver 9/23/68 à Δ moyen.
        w_blanche = math.exp(5.0 * (d - 0.80)) * (1.6 if self.coeur is Coeur.BLANC else 1.0)
        w_noire = math.exp(-5.0 * (d - 0.35)) * (1.8 if self.coeur is Coeur.NOIR else 1.0)
        w_grise = 2.4 * math.exp(-3.0 * (d - 0.55) ** 2) * (1.3 if self.coeur is Coeur.GRIS else 1.0)
        tot = w_blanche + w_noire + w_grise
        probs = {"Collapse Blanche": w_blanche / tot,
                 "Verrou Noir": w_noire / tot,
                 "Fragmentation Grise": w_grise / tot}
        # Le Codex "refuse de calculer" : 1 % de chances de tout renvoyer à ???
        if self.rng.random() < 0.01:
            return "???", probs
        issue = self.rng.choices(list(probs), weights=list(probs.values()))[0]
        return issue, probs

    # --- exécution complète
    def run(self) -> Dict:
        if self.verbeux:
            self.entete()
        self.tissage_trame()
        issue, probs = self.convergence()
        self.conclusion(issue, probs)
        return self.rapport(issue, probs)

    def entete(self) -> None:
        txt = """
=====================================================================
  PROTOCOLE ZELENOGRAD v3.2 : GENERATEUR DE DISCORDANCE ONTOLOGIQUE
  Auteur      : Joachim Walder Rauch (Ministère de la Cohérence, Fulda)
  Machine     : Robotron 1715 (Modifié Strate II, Noyau Quantique)
  Date        : 14 Octobre 1993 (Superposition Temporelle Active)
  Cible       : Centres de Recherche US (DARPA, Los Alamos, Pensacola)
  Objectif    : Injection de Paleo-Mèmes, basculement du Delta (> 0.89)
  Référence   : Codex Stein, Fragment 7, "Le Hackeur comme Explorateur"
=====================================================================
"""
        say(txt.strip("\n"), "grey")
        say(f"  graine : {self.seed}   |   mode : {'ORIGINAL (fidèle au pseudo-ALGOL)' if self.mode_original else 'ÉTENDU (MTT-2075)'}",
            "grey")
        say()

    def conclusion(self, issue: str, probs: Dict[str, float]) -> None:
        self.log()
        self.log("=" * 49)
        self.log("CONVERGENCE INITIÉE.", "bold")
        for k, p in probs.items():
            self.log(f"   {k:<20} {bar(p, 24)}", "dim")
        self.log(f"   → ISSUE : {issue.upper()}", "magenta", "bold")
        self.log(issue_texte(issue), "white")
        self.log("LE CODE COSMIQUE S'EXPLORE LUI-MÊME.")
        self.log(f"SIGNÉ : {SIGNATURE}")
        self.log(SCEAU)
        self.log("=" * 49)

    def rapport(self, issue: str, probs: Dict[str, float]) -> Dict:
        return {
            "seed": self.seed,
            "mode": "original" if self.mode_original else "etendu",
            "coeur": self.coeur.value,
            "delta_final": round(self.trame.delta(), 4),
            "trame": {"C": round(self.trame.C, 3), "R": round(self.trame.R, 3), "H": round(self.trame.H, 3)},
            "ancrage_realite": self.ancrage_realite,
            "strate_bascule": self.strate_bascule,
            "echos_guillaume": self.echo_emis,
            "paleo_memes": self.paleo_utilises,
            "issue": issue,
            "probabilites": {k: round(v, 4) for k, v in probs.items()},
            "noeuds": [{"nom": n.nom, "reve": n.reve, "glitchs": n.glitchs,
                        "injections": n.injections, "resistance": round(n.resistance, 3),
                        "phase": n.phase, "historique": n.historique} for n in self.noeuds],
            "evenements": [asdict(e) for e in self.evenements],
        }


def issue_texte(issue: str) -> str:
    return {
        "Collapse Blanche": "Liberté totale : chaos créatif ou dissolution. Le Cœur Blanc s'est dissous dans le système.",
        "Verrou Noir": "Déterminisme absolu : paix forcée ou stagnation. La trame est figée.",
        "Fragmentation Grise": "Réalités multiples : richesse ou épuisement du sens. Les sept strates cohabitent.",
        "???": "Le Codex refuse de calculer…",
    }[issue]


# ---------------------------------------------------------------------
# 9. MONTE-CARLO
# ---------------------------------------------------------------------

def monte_carlo(n: int, coeur: Coeur, mode_original: bool, seed: Optional[int]) -> Dict:
    base = seed if seed is not None else random.SystemRandom().randrange(1 << 30)
    issues = {"Collapse Blanche": 0, "Verrou Noir": 0, "Fragmentation Grise": 0, "???": 0}
    bascules = {i: 0 for i in range(1, NB_STRATES_PROTOCOLE + 1)}
    jamais = 0
    deltas: List[float] = []
    echos: List[int] = []
    for k in range(n):
        z = Zelenograd(seed=base + k, coeur=coeur, mode_original=mode_original, verbeux=False)
        r = z.run()
        issues[r["issue"]] += 1
        deltas.append(r["delta_final"])
        echos.append(r["echos_guillaume"])
        if r["strate_bascule"]:
            bascules[r["strate_bascule"]] += 1
        else:
            jamais += 1
    moy = sum(deltas) / n
    var = sum((x - moy) ** 2 for x in deltas) / max(1, n - 1)
    return {"n": n, "coeur": coeur.value, "mode": "original" if mode_original else "etendu",
            "issues": {k: v / n for k, v in issues.items()},
            "bascule_par_strate": {k: v / n for k, v in bascules.items()},
            "jamais_bascule": jamais / n,
            "delta_moyen": moy, "delta_ecart_type": math.sqrt(var),
            "echos_moyens": sum(echos) / n, "seed_base": base}


def afficher_mc(res: Dict) -> None:
    say(f"MONTE-CARLO · {res['n']} exécutions · cœur {res['coeur'].upper()} · mode {res['mode']}", "bold")
    say(f"  Δ final moyen : {res['delta_moyen']:.3f} ± {res['delta_ecart_type']:.3f}   |   "
        f"échos-Guillaume moyens : {res['echos_moyens']:.2f}")
    say("  Issues de la Convergence (cible README : Blanche 9 % / Noire 23 % / Grise 68 %) :")
    for k, v in res["issues"].items():
        say(f"    {k:<20} {bar(v, 30)}  {v*100:5.1f} %")
    say("  Strate de rupture de l'ancrage :")
    for k, v in res["bascule_par_strate"].items():
        say(f"    Strate {k}  {bar(v, 30)}  {v*100:5.1f} %")
    say(f"    Jamais rompu {bar(res['jamais_bascule'], 30)}  {res['jamais_bascule']*100:5.1f} %")


# ---------------------------------------------------------------------
# 10. REPL FRACTUROSCRIPT
# ---------------------------------------------------------------------

AIDE_REPL = """
Commandes FracturoScript :  Ω<RUNE>vN lieu — intention •••
   RUNE : glyphe (ᚦ ᚨ ᛈ ᛟ ᚢ ᛒ ᚠ ᛁ ᚲ ᛃ ᛞ) ou nom (Thurisaz, Ansuz, ...) ou 'odin'
   lieu : hague, raz, caen, bayeux, rouen, jobourg, vauville, mont-saint-michel,
          fulda, zelenograd, local
Méta-commandes :
   :coeur noir|gris|blanc    change la posture de l'opérateur
   :heure aube|maree-montante|maree-descendante|crepuscule|midi
   :etat                     état de l'opérateur et de la trame
   :runes                    table des runes
   :lieux                    table des lieux
   :strict on|off            vérification de lieu stricte
   :codex N                  fresque Codex Stein (profondeur N)
   :muter texte...           applique `muter-recit`
   :aide  :quitter
"""


def repl(seed: Optional[int], coeur: Coeur) -> None:
    rng = random.Random(seed)
    op = Operateur("RuneSmith", coeur, rng=rng)
    trame = Trame(H=coeur.h_typique)
    heure = "aube"
    strict = True
    say("FRACTUROSCRIPT · console de Caen-Profonde — « décrire, c'est faire ». (:aide pour l'aide)", "bold")
    while True:
        try:
            ligne = input(UI.paint("Ω> ", "cyan")).strip()
        except (EOFError, KeyboardInterrupt):
            say("\n« Ce qui a été lu reste entre les strates. Δ, sois témoin. »", "dim")
            return
        if not ligne:
            continue
        if ligne.startswith(":"):
            parts = ligne[1:].split(None, 1)
            cmd, arg = parts[0].lower(), (parts[1] if len(parts) > 1 else "")
            if cmd in ("quitter", "q", "exit"):
                say("« Ce qui a été lu reste entre les strates. Δ, sois témoin. »", "dim")
                return
            elif cmd == "aide":
                say(AIDE_REPL)
            elif cmd == "coeur":
                try:
                    op.coeur = Coeur(arg.strip().lower())
                    op.H = op.coeur.h_typique
                    say(f"Cœur {op.coeur.value.upper()} — {op.coeur.effet}")
                except ValueError:
                    say("Cœurs valides : noir, gris, blanc", "red")
            elif cmd == "heure":
                heure = arg.strip().lower() or heure
                say(f"Heure glissante : {heure}")
            elif cmd == "etat":
                say(op.etat())
                say(f"Trame C={trame.C:.2f} R={trame.R:.2f} H={trame.H:.2f}  Δ {bar(trame.delta())}")
            elif cmd == "runes":
                for r in RUNES.values():
                    say(f"  {r.glyphe} {r.nom:<9} {r.fonction_py:<7} [{r.famille:<10}] {r.fonction}")
            elif cmd == "lieux":
                for k, v in LIEUX.items():
                    say(f"  {k:<18} Δ≈{v['delta']:.2f}  {v['desc']}")
            elif cmd == "strict":
                strict = arg.strip().lower() != "off"
                say(f"Vérification de lieu : {'stricte' if strict else 'souple'}")
            elif cmd == "codex":
                n = int(arg) if arg.strip().isdigit() else 2
                for l in fresque_codex(min(n, 3), rng):
                    say(l)
            elif cmd == "muter":
                say(muter_recit(arg, rng, taux=1.0))
            else:
                say("Méta-commande inconnue. :aide", "red")
            continue
        try:
            c = parser(ligne)
        except ErreurOntique as e:
            say(f"{e.nom} : {e}", "red")
            say(f"  Symptôme : {e.symptome}\n  Remède   : {e.remede}", "grey")
            continue
        r = executer(c, op, trame, heure, strict)
        for m in r.messages:
            say("  " + m, "green" if r.succes else "yellow")
        say(f"  → {'COMPILÉ' if r.succes else 'ÉCHEC'}  |  {op.etat()}", "bold")


# ---------------------------------------------------------------------
# 11. AUTO-TESTS
# ---------------------------------------------------------------------

def lancer_tests() -> int:
    ok = 0
    ko = 0

    def check(nom: str, cond: bool) -> None:
        nonlocal ok, ko
        if cond:
            ok += 1
            say(f"  ✓ {nom}", "green")
        else:
            ko += 1
            say(f"  ✗ {nom}", "red")

    say("AUTO-TESTS ZELENOGRAD", "bold")
    # Parseur
    c = parser("Ω<ᚦ>v4 hague — oubli douleur spécifique •••")
    check("parse : rune/version/lieu/intention",
          c.rune.nom == "Thurisaz" and c.version == 4 and c.lieu == "hague"
          and c.intention == "oubli douleur spécifique")
    c2 = parser("Ω<ᛃ>v6 rouen — voir passé 1944 •••")
    check("parse : intention multi-mots avec chiffres", c2.intention == "voir passé 1944")
    c3 = parser("Ω<odin>v4 hague — glissement temporel •••")
    check("parse : rune par nom (odin)", c3.rune.nom == "Odin")
    c4 = parser('Ω<ᚲ>v3 local — mot "sécurité" devient goût de cendre •••')
    check("parse : guillemets dans l'intention", "sécurité" in c4.intention)
    for mauvais, nom in [("Ω<ᚦ>v4 hague — oubli", "silence absent"),
                         ("<ᚦ>v4 hague — x •••", "sans Ω"),
                         ("Ω<ZZ>v4 hague — x •••", "rune inconnue")]:
        try:
            parser(mauvais)
            check(f"erreur de syntaxe attendue ({nom})", False)
        except SyntaxError_:
            check(f"erreur de syntaxe attendue ({nom})", True)

    # Type mismatch
    try:
        verifier_type(parser("Ω<ᛁ>v2 hague — brûler le dossier •••"))
        check("TypeMismatch Isa+brûler", False)
    except TypeMismatch:
        check("TypeMismatch Isa+brûler", True)

    # Lieu
    rng = random.Random(1)
    op = Operateur("T", Coeur.BLANC, rng=rng)
    tr = Trame()
    r = executer(parser("Ω<ᛟ>v2 hague — ancrer •••"), op, tr, strict_lieu=True)
    check("LocationMismatch Othala à La Hague", r.erreur == "LocationMismatch")

    # Δ monotone selon R
    check("Δ croît avec R", Trame(R=0.9).delta() > Trame(R=0.1).delta())
    check("Δ décroît avec C", Trame(C=0.9).delta() < Trame(C=0.1).delta())
    check("Δ ∈ [0,1]", all(0 <= Trame(C=a, R=b, H=c).delta() <= 1
                           for a in (0, .5, 1) for b in (0, .5, 1) for c in (0, .5, 1)))

    # Cœurs
    check("seuils de Cœur", Coeur.depuis_h(0.1) is Coeur.NOIR and Coeur.depuis_h(0.5) is Coeur.GRIS
          and Coeur.depuis_h(0.95) is Coeur.BLANC)

    # Reproductibilité
    a = Zelenograd(seed=42, verbeux=False).run()
    b = Zelenograd(seed=42, verbeux=False).run()
    check("reproductibilité par graine", a == b)

    # Mode original : doit se terminer et rompre l'ancrage dès le 1er glitch
    o = Zelenograd(seed=7, mode_original=True, verbeux=False).run()
    check("mode original : rapport complet", "issue" in o and o["mode"] == "original")

    # Distribution de convergence plausible (Monte-Carlo court)
    res = monte_carlo(300, Coeur.GRIS, False, 1234)
    check("MC : Fragmentation Grise est l'issue modale (cœur gris)",
          max(res["issues"], key=res["issues"].get) == "Fragmentation Grise")
    check("MC : somme des issues = 1", abs(sum(res["issues"].values()) - 1) < 1e-9)

    # Mutation Codex Stein
    m = muter_recit("skeith et innis", random.Random(3), taux=1.0)
    check("muter-recit produit des MUTANT", "MUTANT" in m)

    say(f"\n{ok} réussis, {ko} échoués", "bold", "green" if ko == 0 else "red")
    return 0 if ko == 0 else 1


# ---------------------------------------------------------------------
# 12. POINT D'ENTRÉE
# ---------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="PROTOCOLE ZELENOGRAD v4.0 — générateur de discordance ontologique (fiction MTT-2075)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Tout ceci est une fiction : aucune action réseau, aucun fichier modifié (hors --export).")
    ap.add_argument("--seed", type=int, help="graine aléatoire (exécution rejouable)")
    ap.add_argument("--coeur", choices=[c.value for c in Coeur], default="gris",
                    help="posture de l'opérateur (défaut : gris)")
    ap.add_argument("--original", action="store_true",
                    help="reproduit fidèlement la logique du pseudo-ALGOL de 1993")
    ap.add_argument("--strates", type=int, default=NB_STRATES_PROTOCOLE, help="nombre de strates (1-7)")
    ap.add_argument("--cibles", nargs="+", help="noms de noeuds cibles (défaut : DARPA/LOS ALAMOS/PENSACOLA)")
    ap.add_argument("--cibles-etendues", action="store_true", help="ajoute les noeuds du Corpus (Prométhée, Skaði…)")
    ap.add_argument("--monte-carlo", type=int, metavar="N", help="N exécutions silencieuses + statistiques")
    ap.add_argument("--fracturo", metavar="CMD", help="exécute une commande FracturoScript isolée")
    ap.add_argument("--heure", default="aube", help="heure glissante pour --fracturo")
    ap.add_argument("--repl", action="store_true", help="console FracturoScript interactive")
    ap.add_argument("--codex", type=int, metavar="PROF", help="fresque Codex Stein (profondeur 1-3)")
    ap.add_argument("--export", metavar="FICHIER.json", help="écrit le rapport JSON")
    ap.add_argument("--lent", type=float, default=0.0, metavar="SEC", help="pause dramatique entre les lignes")
    ap.add_argument("--no-color", action="store_true", help="désactive les couleurs ANSI")
    ap.add_argument("--tests", action="store_true", help="lance les auto-tests")
    args = ap.parse_args(argv)

    if args.no_color:
        UI.color = False
    UI.slow = args.lent
    coeur = Coeur(args.coeur)

    if args.tests:
        return lancer_tests()

    if args.repl:
        repl(args.seed, coeur)
        return 0

    if args.codex:
        rng = random.Random(args.seed)
        for l in fresque_codex(max(1, min(args.codex, 3)), rng):
            say(l)
        return 0

    if args.fracturo:
        rng = random.Random(args.seed)
        op = Operateur("RuneSmith", coeur, rng=rng)
        trame = Trame(H=coeur.h_typique)
        try:
            c = parser(args.fracturo)
        except ErreurOntique as e:
            say(f"{e.nom} : {e}", "red")
            say(f"  Symptôme : {e.symptome}\n  Remède   : {e.remede}", "grey")
            return 2
        r = executer(c, op, trame, args.heure)
        for m in r.messages:
            say("  " + m, "green" if r.succes else "yellow")
        say(f"→ {'COMPILÉ' if r.succes else 'ÉCHEC'} | {op.etat()}", "bold")
        return 0 if r.succes else 1

    if args.monte_carlo:
        res = monte_carlo(args.monte_carlo, coeur, args.original, args.seed)
        afficher_mc(res)
        if args.export:
            with open(args.export, "w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False, indent=2)
            say(f"\nRapport écrit dans {args.export}")
        return 0

    cibles = args.cibles or list(CIBLES_DEFAUT)
    if args.cibles_etendues:
        cibles += EXTRA_CIBLES
    z = Zelenograd(seed=args.seed, coeur=coeur, cibles=cibles, strates=args.strates,
                   mode_original=args.original)
    rapport = z.run()
    if args.export:
        with open(args.export, "w", encoding="utf-8") as f:
            json.dump(rapport, f, ensure_ascii=False, indent=2)
        say(f"\nRapport écrit dans {args.export}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
