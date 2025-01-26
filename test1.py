import pygame

pygame.init()

# Konstanten für das Spiel
SPIELFELD_GROESSE = 3
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)
ROT = (255, 0, 0)
BLAU = (0, 0, 255)
FENSTER_BREITE = 600
FENSTER_HOEHE = 600
ZELLEN_GROESSE = FENSTER_BREITE // SPIELFELD_GROESSE
LINIEN_STAERKE = 5

screen = pygame.display.set_mode((FENSTER_BREITE, FENSTER_HOEHE), pygame.RESIZABLE)
pygame.display.set_caption("Tic Tac Toe")

# Spielfeld-Datenstruktur
spielfeld = [" " for _ in range(SPIELFELD_GROESSE * SPIELFELD_GROESSE)]
spieler = "X"
spiel_beendet = False
font = pygame.font.Font(None, 72)
# Erstellen der Spielfeldoberfläche und Hintergrund
spielfeld_oberflaeche = pygame.Surface((FENSTER_BREITE, FENSTER_HOEHE), pygame.SRCALPHA)  # Surface für das Spielfeld
hintergrund = pygame.Surface((FENSTER_BREITE, FENSTER_HOEHE))

# Zwischenspeicher für die hervorgehobene Zelle
hervorgehobene_zelle = None


# Funktion um das Spielfeld zu Zeichnen (ohne Linien)
def zeichne_spielfeld(color, linienstaerke, oberflaeche):
    # Füllen des Hintergrundes mit der Farbe Weiß
    oberflaeche.fill(color)

    # Vertikale Linien
    for spalte in range(1, SPIELFELD_GROESSE):
        x = spalte * ZELLEN_GROESSE
        pygame.draw.line(oberflaeche, SCHWARZ, (x, 0), (x, FENSTER_HOEHE), linienstaerke)

    # Horizontale Linien
    for reihe in range(1, SPIELFELD_GROESSE):
        y = reihe * ZELLEN_GROESSE
        pygame.draw.line(oberflaeche, SCHWARZ, (0, y), (FENSTER_BREITE, y), linienstaerke)


# Funktion für das Zeichnen des Textes
def zeichne_text(oberflaeche):
    for reihe in range(SPIELFELD_GROESSE):
        for spalte in range(SPIELFELD_GROESSE):
            # Text/Figuren in Zellen
            text = font.render(spielfeld[reihe * SPIELFELD_GROESSE + spalte], True, SCHWARZ)
            text_rect = text.get_rect(
                center=((spalte * ZELLEN_GROESSE + ZELLEN_GROESSE / 2), (reihe * ZELLEN_GROESSE + ZELLEN_GROESSE / 2)))
            oberflaeche.blit(text, text_rect)


# Funktion um ein Feld hervorzuheben (optional)
def feld_hervorheben(oberflaeche, feld_index, farbe):
    if feld_index is None:
        return

    y = (FENSTER_HOEHE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2
    x = (FENSTER_BREITE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2

    reihe = feld_index // SPIELFELD_GROESSE
    spalte = feld_index % SPIELFELD_GROESSE

    x += spalte * ZELLEN_GROESSE
    y += reihe * ZELLEN_GROESSE
    feld_rect = pygame.Rect(x, y, ZELLEN_GROESSE, ZELLEN_GROESSE)
    pygame.draw.rect(oberflaeche, farbe, feld_rect)


# Funktion, die nur den Bildschirm aktualisiert
def screen_aktualisieren():
    pygame.display.flip()


# Funktion um das Spiel darzustellen
def singleplayer_anzeigen(color):
    screen.blit(hintergrund, (0, 0))
    screen.blit(spielfeld_oberflaeche, (0, 0))
    zeichne_text(screen)  # Der Text muss bei jeder Anzeige neu gezeichnet werden.
    screen_aktualisieren()  # Aktualisiere den Screen


# Klick auf das Spielfeld
def feld_ausgewaehlt(maus_position):
    # obere linke Feldecke
    y = (FENSTER_HOEHE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2

    for reihe in range(SPIELFELD_GROESSE):
        x = (FENSTER_BREITE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2
        for spalte in range(SPIELFELD_GROESSE):
            feld_rect = pygame.Rect(x, y, ZELLEN_GROESSE, ZELLEN_GROESSE)  # Erstelle ein Rect mit allen Parametern

            if feld_rect.collidepoint(maus_position) and spielfeld[reihe * SPIELFELD_GROESSE + spalte] == " ":
                return reihe * SPIELFELD_GROESSE + spalte  # Die Stelle im Spielfeld

            x += ZELLEN_GROESSE

        y += ZELLEN_GROESSE
    return None


# Mausposition überprüfen
def maus_auf_feld(maus_position):
    # obere linke Feldecke
    y = (FENSTER_HOEHE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2

    for reihe in range(SPIELFELD_GROESSE):
        x = (FENSTER_BREITE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2
        for spalte in range(SPIELFELD_GROESSE):
            feld_rect = pygame.Rect(x, y, ZELLEN_GROESSE, ZELLEN_GROESSE)
            if feld_rect.collidepoint(maus_position):
                return reihe * SPIELFELD_GROESSE + spalte
            x += ZELLEN_GROESSE
        y += ZELLEN_GROESSE
    return None


# Gewinnprüfung
def spiel_gewonnen(symbol):
    for reihe in range(SPIELFELD_GROESSE):
        if all(spielfeld[reihe * SPIELFELD_GROESSE + i] == symbol for i in range(SPIELFELD_GROESSE)):
            return True  # Reihe gleich

    for spalte in range(SPIELFELD_GROESSE):
        if all(spielfeld[i * SPIELFELD_GROESSE + spalte] == symbol for i in range(SPIELFELD_GROESSE)):
            return True  # Spalte gleich

    # Diagonale
    if all(spielfeld[i * SPIELFELD_GROESSE + i] == symbol for i in range(SPIELFELD_GROESSE)):
        return True

    if all(spielfeld[i * SPIELFELD_GROESSE + (SPIELFELD_GROESSE - 1 - i)] == symbol for i in range(SPIELFELD_GROESSE)):
        return True

    return False


# Unentschieden
def unentschieden():
    return all(zelle != " " for zelle in spielfeld)  # Ist das Spielfeld voll


# Spieler wechseln
def wechsel_spieler():
    global spieler
    spieler = "O" if spieler == "X" else "X"


# Initiales Zeichnen des Spielfelds
zeichne_spielfeld(WEISS, LINIEN_STAERKE, spielfeld_oberflaeche)
# Spiel-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            # Bei einem Fensterresize, muss die Oberfläche neu gerendert werden
            FENSTER_BREITE = event.w
            FENSTER_HOEHE = event.h
            ZELLEN_GROESSE = FENSTER_BREITE // SPIELFELD_GROESSE
            screen = pygame.display.set_mode((FENSTER_BREITE, FENSTER_HOEHE), pygame.RESIZABLE)
            spielfeld_oberflaeche = pygame.Surface((FENSTER_BREITE, FENSTER_HOEHE),
                                                   pygame.SRCALPHA)  # Surface für das Spielfeld
            hintergrund = pygame.Surface((FENSTER_BREITE, FENSTER_HOEHE))
            zeichne_spielfeld(WEISS, LINIEN_STAERKE, spielfeld_oberflaeche)  # Neu Zeichnen

        if event.type == pygame.MOUSEMOTION:
            maus_pos = event.pos
            feld_index = maus_auf_feld(maus_pos)
            # Lösche die alte Markierung und speichere die neue
            if hervorgehobene_zelle is not None:
                feld_hervorheben(spielfeld_oberflaeche, hervorgehobene_zelle, WEISS)
            if feld_index is not None:
                feld_hervorheben(spielfeld_oberflaeche, feld_index, BLAU)

            hervorgehobene_zelle = feld_index  # Speichert das Feld, um es wieder zu entfernen

        if not spiel_beendet:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Linksklick
                maus_pos = event.pos
                feld_index = feld_ausgewaehlt(maus_pos)
                if feld_index is not None:
                    spielfeld[feld_index] = spieler
                    if spiel_gewonnen(spieler):
                        print(f"{spieler} gewinnt!")
                        spiel_beendet = True
                    elif unentschieden():
                        print("Unentschieden!")
                        spiel_beendet = True
                    else:
                        wechsel_spieler()

    singleplayer_anzeigen(WEISS)

pygame.quit()