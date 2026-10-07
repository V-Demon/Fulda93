# 📂 Z80_UNDOC_ONTOLOGY.md
> **CLASSIFICATION :** TARVOS / STRATE III  
> **SOURCE :** Ministère de la Cohérence Ontologique, Département de Reverse-Engineering (Fulda, RDA)  
> **TRANSCRIPTION :** Archiviste Null-Sector (Caen-Profonde, 2025/2075)  
> **MATÉRIEL CIBLE :** U880 (Clone Zilog Z80, Robotron 1715)  

---

## [0x00] PRÉAMBULE : L'ILLUSION DU SILICIUM

Dans l'ingénierie conventionnelle, les "opcodes non documentés" du Z80 (et de son clone est-allemand, l'U880 du Robotron 1715) sont considérés comme des artefacts de fabrication, des bugs de microcode ou des états de transition laissés par les ingénieurs de Zilog. 

Le Ministère de la Cohérence Ontologique sait qu'il n'en est rien. 

Le silicium est de la matière (couche **Lithique**). Lorsqu'il est soumis à des champs de Δ (Delta) élevés — comme dans les fonderies de Zelenograd ou les sous-sols de Fulda après l'Incident de Pripyat-Alpha — le microcode commence à refléter la structure de la Trame. Les opcodes "non documentés" ne sont pas des bugs. Ce sont des **backdoors ontologiques**. Ce sont les seuls endroits où le Master Code (Promethee_Prime) a oublié de verrouiller la porte.

Ce document mappe les instructions non documentées du Z80 à leurs effets réels sur la fonction d'onde du réel.

---

## [0x01] MATRICE DES OPCODES GLITCHÉS (MTT-2075)

| Hex | Z80/U880 Officiel (Undocumented) | Interprétation MTT (Glitched Opcode) | Effet sur le Δ (Delta) | Équivalent FracturoScript |
|:---:|:---------------------------------|:-------------------------------------|:----------------------:|:--------------------------|
| `CB 3x` | `SLL r` (Shift Left Logical) | **S**hift **L**ocal **L**ithic : Décale la matière brute d'un bit vers la gauche, injectant un "1" dans le vide. Crée une micro-anomalie physique (ex: objet déplacé de 2mm). | +0.05 | `ᚢ` (Uruz - Renforcement local) |
| `ED 70` | `IN F, (C)` | **I**nterstice **N**eutral **F**lag : Lit l'état du port de la réalité (C) sans modifier le registre A (Lithique), mais met à jour les drapeaux (F). Permet de "sentir" le Δ ambiant sans le perturber. | 0.00 (Scan) | `ᚨ` (Ansuz - Écoute inter-strates) |
| `DD 24` / `DD 25` | `INC IXH` / `DEC IXH` | **D**elta **D**rive **X**-strata **H**idden : Accès direct aux octets cachés du registre d'index. Permet de lire/écrire dans la strate Onirique de Caen-Profonde sans toucher au présent (Verðandi). | +0.15 | `ᛈ` (Perthro - Superposition) |
| `ED 36`* | *(Non standard / SLI)* | **S**hift **L**ayer **I**nterstice : Force une ouverture temporaire entre la Strate II (2061-2075) et la Strate I. Risque élevé d'écho inversé (recevoir un message que l'on a soi-même envoyé dans le futur). | +0.33 | `Ωv <lieu> — <intention>` |
| `ED 44` | `NEG` (Documenté, mais détourné) | **N**ullify **E**xistence **G**rid : Si exécuté immédiatement après un `SLL`, annule la dette causale de l'opération précédente. Utilisé par les Hackervölvas pour "effacer" leurs traces dans le journal de Promethee_Prime. | -0.10 | `ᚦ` (Thurisaz - Barrière/Oubli) |
| `ED 3E` | `RLD` (Rotate Left Decimal) | **R**eality **L**ayer **D**issolution : Fait transiter la phase du nœud local selon le Codex Stein (ex: MAGUS → FIDCHELL). **DANGER CRITIQUE.** | +0.89 (Seuil de basculement) | `•••` (Silence Sacré requis) |

> *\* Note de l'archiviste : `ED 36` n'est pas un opcode Z80 valide dans la documentation officielle. Son existence dans le microcode de l'U880 de Joachim W. Rauch a été confirmée par analyse du dump ROM `zelenograd_jwr.a68`. Son exécution provoque un pic de tension sur la broche 16 du processeur et un sifflement à 14.250 MHz.*

---

## [0x02] LE PARADOXE DE BERGMANN (V9) ET LES DRAPEAUX FANTÔMES

Le Z80 possède une particularité connue des hackers de la démoscene : lors de certaines opérations, les bits 3 et 5 du registre de drapeaux (F register) copient les bits 3 et 5 du registre accumulateur (A). 

Dans le cadre du **Master Code**, ces bits sont les canaux de résonance mémétique. 

L'incident d'avril 1993 impliquant l'ingénieur Bergmann s'est produit lorsqu'il a tenté de compiler le code suivant :
```assembly
LD A, 0x00      ; Intention : "Oublier" (Cœur Noir)
LD C, 0x14      ; Port 20m (Bande radio)
IN F, (C)       ; Lecture du Δ ambiant
; À ce stade, les bits 3 et 5 de F reflètent l'état onirique du système.
OR A, 0xFF      ; Intention : "Brûler la mémoire" (Cœur Blanc)
