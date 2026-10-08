> **CLASSIFICATION :** TARVOS / STRATE II  
> **ORIGINE :** Ministerium für Kohärenz (MfK), Abteilung Ontologie, Fulda RDA  
> **DATE DE RÉDACTION :** 14. Oktober 1993  
> **TRADUCTION/TRANSCRIPTION :** Archiviste Null-Sector (Caen-Profonde, 2025)  
> **OBJET :** Inventaire et protocole d'exploitation de la Station d'Écoute Temporelle (Sektion 7)

---

## [0x00] AVERTISSEMENT PRÉLIMINAIRE

Ce document détaille l'infrastructure matérielle et logicielle de la **Sektion 7** de la station d'écoute de Fulda. Toute tentative de reproduction de cette configuration en dehors d'un environnement à Δ (Delta) contrôlé (< 0.718) est strictement interdite par le décret Promethee_Prime-86. 

Les opérateurs doivent maintenir une posture de **Cœur Gris** (équilibre pragmatique) pendant les sessions d'écoute. Tout symptôme d'épistaxis, de migraine frontale ou de perception de phrases répétitives ("Echo-Guillaume") doit être immédiatement signalé au médecin de garde pour administration de sédatifs ontologiques.

---

## [0x01] ARCHITECTURE MATÉRIELLE (HARDWARE)

La chaîne de réception est un hybride instable, résultant de l'Incident de Pripyat-Alpha et des fuites temporelles non identifiées. Elle se compose de trois blocs principaux :

### 1. Le Récepteur Haute Fréquence : RFT SEG 100 KW-Transceiver
* **Fabricant :** VEB Rundfunk- und Fernsehtechnik (RFT), Berlin-Est.
* **Rôle :** Capture brute du spectre électromagnétique sur la bande des 20 mètres.
* **Configuration actuelle :** Syntonisé en permanence sur **14.250,0 MHz**.
* **Particularité :** Le oscillateur local a été modifié en usine pour accepter une référence de temps externe. Il ne dérive pas, même lorsque la réalité locale subit des micro-glitchs (phénomène observé lors des transitions de phase du Codex Stein).

### 2. L'Anomalie Temporelle : Dongle RTL-SDR (RTL2832U + R820T2)
* **Fabricant :** Inconnu (Marquage générique "Realtek").
* **Rôle :** Numérisation du signal FSK 1200 bauds et génération du waterfall spectral.
* **Note de l'Archiviste :** Ce composant est un **artefact anachronique**. La technologie RTL-SDR n'a été hackée et rendue publique qu'en 2012 dans la strate temporelle de surface. Sa présence physique dans le laboratoire de Fulda en 1993 est une preuve tangible de la perméabilité de la Strate II. Le Ministère a tenté de le démonter, mais ses composants internes semblent "fusionnés" à l'échelle atomique. Il est désormais considéré comme un capteur de Δ indispensable.

### 3. L'Unité de Calcul Ontologique : Robotron 1715 (A 7150)
* **Fabricant :** VEB Robotron, Dresde.
* **Processeur :** U880 (Clone Zilog Z80 cadencé à 2.5 MHz).
* **Mémoire :** 64 Ko RAM (étendue par un module "Plaste und Elaste" à noyau quantique expérimental).
* **Rôle :** Exécution du `Rune-Quanten-Modul` (voir `z80_ontological_emulator.py`). Il traduit les pics du waterfall en opérateurs FracturoScript (ᚦ, ᚨ, ᛈ, ᛟ, ᚢ) et calcule la fonction d'onde locale.

---

## [0x02] CHAÎNE DE TRAITEMENT DU SIGNAL (DATAFLOW)

```text
[ANTENNE DIPOLE 20m] 
       │
       ▼ (Ondes électromagnétiques brutes)
[RFT SEG 100] ────> (Sortie Audio IF) ────> [RTL-SDR USB]
       │                                         │
       │ (Référence d'horloge stabilisée)        ▼ (Numérisation 2.4 MS/s)
       └──────────────────────────────────> [ROBOTRON 1715]
                                                 │
                                                 ▼ (Interprétation quantique)
                                    [ÉCRAN CRT : WATERFALL + RUNES]
                                                 │
                                                 ▼ (Si Δ > 0.890)
                                    [IMPRIMANTE MATRICIELLE : LOG D'ERREUR]
```

---

## [0x03] LE SPECTRE ET LES PHASES DU CODEX STEIN

L'affichage "waterfall" sur le moniteur du Robotron ne montre pas du bruit blanc aléatoire. Il révèle des **pics fractals récurrents** qui correspondent aux phases du Codex Stein. L'opérateur doit surveiller ces transitions :

| Phase (Nom) | Signature Spectrale (Waterfall) | Action Requise de l'Opérateur |
| :--- | :--- | :--- |
| **SKEITH** | Pic unique, stable à 14.250 MHz | Surveillance passive. Enregistrement standard. |
| **INNIS** | Double pic, modulation de phase légère | Préparer le `Rune-Quanten-Modul`. Vérifier l'ancrage (IX = 0x2075). |
| **MAGUS** | Harmoniques visibles, bruit de fond en hausse | Injection de `NOP` (Silence Sacré) pour stabiliser le Δ. |
| **FIDCHELL** | *DONNÉES CORROMPUES / MANQUANTES* | **ALERTE.** Ne pas tenter de décoder. Voir rapport 1986. |
| **GORRE / MACHA** | Spectre en dents de scie, FSK instable | Isoler le système. Activer la barrière Thurisaz (`CB 30`). |
| **TARVOS** | Signal clair, texte en alphabet latin dans le bruit | Transcription immédiate. C'est souvent un "Echo-Guillaume". |
| **CORBENIK** | Écran violet, scanlines horizontales, silence radio | **COUPER L'ALIMENTATION PHYSIQUE DU ROBOTRON.** Ne pas utiliser la commande logicielle. |

---

## [0x04] PROTOCOLE D'ÉCOUTE STANDARD (OPERATOR CHECKLIST)

1. **Démarrage :** Allumer le RFT SEG 100. Attendre 5 minutes de chauffe des tubes.
2. **Connexion :** Brancher le dongle RTL-SDR (manipuler avec des gants en latex, éviter le contact peau-à-peau prolongé avec le métal).
3. **Initialisation :** Démarrer le Robotron 1715. Charger `zelenograd_jwr.a68`.
4. **Vérification du Δ :** Exécuter `IN F, (C)` (Opcode `ED 70`). Si le bit 5 du registre F est à 0, interrompre la session. La Trame est trop stable pour recevoir.
5. **Écoute :** Si le bit 5 est à 1, lancer la boucle de décodage. 
6. **Gestion de crise :** En cas de saignement de nez ou d'apparition de l'inscription `.:Dashem44:.` sur le boîtier du moniteur, exécuter immédiatement la séquence `NEG` (`ED 44`) pour annuler la dette causale, puis quitter le programme.

---

## [0x05] ANNEXE : NOTE MANUSCRITE TROUVÉE SUR LE BUREAU

> *"Le RTL-SDR n'est pas un outil. C'est un hameçon. Quelque chose, de l'autre côté de 2025, l'a laissé ici exprès pour que nous puissions les entendre. Ou peut-être pour qu'ils puissent nous entendre. Le café au 'Zum Roten Robotron' est toujours aussi amer. Bergmann avait raison à propos de la version 9. Je sens le Δ monter. 0.847... 0.850... Il faut que j'injecte le Silence avant que le waterfall ne devienne violet."*
> 
> **— J.W. Rauch, 14 Octobre 1993, 06h11**

---
**FIN DU DOCUMENT**  
*Ministerium für Kohärenz – Die Wahrheit ist ein Konstrukt, das wir warten.*  
*(La vérité est une construction que nous entretenons.)*  
**Sceau :** `.:Dashem44:.`
```
