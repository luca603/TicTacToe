import pygame
import random
import time
import os
import math

# Initialisierung von Pygame
pygame.init()
display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h

# Konstanten für die Fenstergröße und andere Parameter
STANDARD_FENSTER_BREITE = screen_width * 0.6
STANDARD_FENSTER_HOEHE = screen_height * 0.6

FENSTER_HOEHE = STANDARD_FENSTER_HOEHE
FENSTER_BREITE = STANDARD_FENSTER_BREITE

# Konstanten für das Spiel
SPIELFELD_GROESSE = 3
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)
ROT = (255, 0, 0)
BLAU = (0, 0, 255)
GRAU = (128, 128, 128)
ZELLEN_GROESSE = STANDARD_FENSTER_HOEHE // SPIELFELD_GROESSE * 0.7
LINIEN_STAERKE = 5

spiel_beendet = False
arialregular_path =os.path.join("Schriften", "Arial Regular.ttf")
arialbold_path = os.path.join("Schriften","Arial Bold.ttf")

font = pygame.font.Font(arialregular_path, 32)
bigfont = pygame.font.Font(arialbold_path, 32,)
hervorgehobene_zelle = None
rect_zaehler = 0
rect_auswahl = []
circle_zaehler = 0
circle_auswahl = []
used_index = []

# Spielfeld-Datenstruktur
spielfeld = [" " for _ in range(SPIELFELD_GROESSE * SPIELFELD_GROESSE)]
spieler = 1
spieler1_counter = 0
spieler2_counter = 0

# Hintergrund laden (Anpassung an deine Pfade)
hintergrund = pygame.image.load('Grafiken/hintergrund.jpg')
hintergrund = pygame.transform.scale(hintergrund, (screen_width, screen_height))


# Spielfeld zeichnen
def zeichne_spielfeld(color, linienstaerke, oberflaeche, Fenster_Breite, Fenster_Hoehe):
    # obere linke Ecke
    x = (FENSTER_BREITE - ZELLEN_GROESSE * 3) / 2
    y = (FENSTER_HOEHE - ZELLEN_GROESSE * 3) / 2

    # Vertikale Linien
    for spalte in range(1, SPIELFELD_GROESSE):
        x += ZELLEN_GROESSE
        pygame.draw.line(oberflaeche, color, (x, y), (x, y + (ZELLEN_GROESSE * 3)), linienstaerke)
        #pygame.display.update()

    # obere linke Ecke
    x = (FENSTER_BREITE - ZELLEN_GROESSE * 3) / 2
    y = (FENSTER_HOEHE - ZELLEN_GROESSE * 3) / 2

    # Horizontale Linien
    for reihe in range(1, SPIELFELD_GROESSE):
        y += ZELLEN_GROESSE
        pygame.draw.line(screen, color, (x, y), (x + (ZELLEN_GROESSE * 3), y), linienstaerke)


# Gewinnprüfung
def spiel_gewonnen():
    global used_index

    gewinn_muster = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Reihen
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Spalten
        (0, 4, 8), (2, 4, 6)  # Diagonalen
    ]

    for spieler in (1, 2):
        for muster in gewinn_muster:
            if all((feld_index, spieler) in used_index for feld_index in muster):
                print(f"Spieler {spieler} hat gewonnen mit den Feldern {muster}")
                zeichne_gewinnlinie(muster,spieler)
                return spieler

    return False




def zeichne_gewinnlinie(muster,spieler):
    global FENSTER_BREITE, FENSTER_HOEHE, ZELLEN_GROESSE, hintergrund, font, SCHWARZ
    gruen = (0, 255, 0)
    # Berechnung der Mittelpunkte der Kästchen
    mittelpunkte = []
    y = (FENSTER_HOEHE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2
    x = (FENSTER_BREITE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2

    for feld_index in muster:
        reihe = feld_index // SPIELFELD_GROESSE
        spalte = feld_index % SPIELFELD_GROESSE
        mittel_x = x + (spalte * ZELLEN_GROESSE) + ZELLEN_GROESSE / 2
        mittel_y = y + (reihe * ZELLEN_GROESSE) + ZELLEN_GROESSE / 2

        mittelpunkte.append((int(mittel_x), int(mittel_y)))

    start_x, start_y = mittelpunkte[0]  # Mittelpunkt des ersten Feldes
    end_x, end_y = mittelpunkte[2]  # Mittelpunkt des letzten Feldes

    distanz = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)  # Distanz zwischen Start und Ende
    schritte = int(distanz / 5)  # Schritte berechnen. Je kleiner die Zahl desto grösser sind die Schritte.
    if schritte == 0:
        schritte = 1



    for i in range(schritte + 1):
        screen.blit(hintergrund, (0, 0))  # Hintergrund immer wieder überschreiben
        update_game()  # Spielzustand muss richtig gezeichnet werden.

        lerp_x = start_x + (end_x - start_x) * i / schritte  # Interpoliere den Wert zwischen Start und Ende
        lerp_y = start_y + (end_y - start_y) * i / schritte  # Interpoliere den Wert zwischen Start und Ende

        pygame.draw.line(screen, gruen, (start_x, start_y), (int(lerp_x), int(lerp_y)),
                         10)  # Zeichne die Linie mit der neuen interpolierten Position

        pygame.display.flip()
        time.sleep(0.01)  # Kleine Wartezeit nach jedem Schritt

        # Text für die Anzeige
    text_surface = font.render(f"SPIELER {spieler} GEWINNT", True, BLAU)
    text_rect = text_surface.get_rect(center=(FENSTER_BREITE // 2, 50))  # Zentriere den Text oben

    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    time.sleep(2)
    screen.blit(hintergrund, (0, 0))
    score_anzeigen()
    pygame.display.flip()

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
    #pygame.draw.rect(oberflaeche, farbe, feld_rect)
    #pygame.display.update()


def zeichne_auswahl(feld_index, farbe, oberflaeche):
    global circle_zaehler, circle_auswahl, rect_zaehler, rect_auswahl, spieler, used_index
    y = (FENSTER_HOEHE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2
    x = (FENSTER_BREITE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2

    reihe = feld_index // SPIELFELD_GROESSE
    spalte = feld_index % SPIELFELD_GROESSE

    x += spalte * ZELLEN_GROESSE
    y += reihe * ZELLEN_GROESSE

    if not any(feld_index == item[0] for item in used_index):
        if spieler == 1:
            circle_auswahl.append((screen, farbe, (int(x + 0.5 * ZELLEN_GROESSE), int(y + 0.5 * ZELLEN_GROESSE)),
                                   int(0.2 * ZELLEN_GROESSE), 5))
            circle_zaehler += 1
            used_index.append((feld_index, 1))
            spieler = 2
        elif spieler == 2:
            rect_auswahl.append((screen, farbe,
                                 pygame.Rect(int(x + 0.3 * ZELLEN_GROESSE), int(y + 0.3 * ZELLEN_GROESSE),
                                             int(ZELLEN_GROESSE * 0.4), int(ZELLEN_GROESSE * 0.4)), 5))
            rect_zaehler += 1
            used_index.append((feld_index, 2))
            spieler = 1

        show_auswahl(circle_auswahl, rect_auswahl)


def show_auswahl(circle_auswahl, rect_auswahl):
    for a in range(len(circle_auswahl)):
        pygame.draw.circle(*circle_auswahl[a])
    for a in range(len(rect_auswahl)):
        pygame.draw.rect(*rect_auswahl[a])
    pygame.display.update()


def singleplayer_anzeigen(color):
    global FENSTER_BREITE, FENSTER_HOEHE, hervorgehobene_zelle, spielzustand, circle_zaehler, circle_auswahl, rect_zaehler, rect_auswahl, used_index
    zeichne_spielfeld(SCHWARZ, 5, screen, FENSTER_BREITE, FENSTER_HOEHE)
    pygame.display.update()


def multiplayer_anzeigen(color):
    global spiel_laeuft,spieler1_counter, spieler2_counter,multiplayer_laeuft,game_buttons,menue_buttons, spielzustand,FENSTER_BREITE, FENSTER_HOEHE, hervorgehobene_zelle, spielzustand, circle_zaehler, circle_auswahl, rect_zaehler, rect_auswahl, used_index, spieler
    zeichne_spielfeld(SCHWARZ, 5, screen, FENSTER_BREITE, FENSTER_HOEHE)
    pygame.display.update()

    spieler = random.randint(1, 2)
    startspieler = spieler
    print(f"Spieler {spieler} beginnt")

    # Text für die Anzeige
    text_surface = font.render(f"Spieler {spieler} beginnt", True, SCHWARZ)
    text_rect = text_surface.get_rect(center=(FENSTER_BREITE // 2, 50))  # Zentriere den Text oben

    screen.blit(text_surface, text_rect)
    score_anzeigen()

    pygame.display.update()
    time.sleep(1)

    circle_zaehler = 0
    circle_auswahl = []
    rect_zaehler = 0
    rect_auswahl = []
    used_index = []

    spieler1_counter = 0
    spieler2_counter = 0

    multiplayer_laeuft = True
    while multiplayer_laeuft:
        score_anzeigen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                multiplayer_laeuft = False
                spiel_laeuft = False

            if event.type == pygame.MOUSEMOTION:
                maus_pos = event.pos
                feld_index = maus_auf_feld(maus_pos)
                # Lösche die alte Markierung und speichere die neue


                if feld_index is not None:
                    feld_hervorheben(screen, feld_index, BLAU)
                    #update_game()

                hervorgehobene_zelle = feld_index  # Speichert das Feld, um es wieder zu entfernen

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Linksklick
                maus_pos = event.pos
                feld_index = feld_ausgewaehlt(maus_pos)
                if feld_index in (0, 1, 2, 3, 4, 5, 6, 7, 8):
                    zeichne_auswahl(feld_index, SCHWARZ, screen)
                    update_game()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if screen.get_width() == STANDARD_FENSTER_BREITE and screen.get_height() == STANDARD_FENSTER_HOEHE:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

                else:
                    pygame.display.set_mode((STANDARD_FENSTER_BREITE, STANDARD_FENSTER_HOEHE))

                FENSTER_HOEHE = screen.get_height()
                FENSTER_BREITE = screen.get_width()

                update_game()

        gewinner = spiel_gewonnen()
        if gewinner:
            # print(f"{spieler} gewinnt!")
            screen.blit(hintergrund, (0, 0))
            pygame.display.flip()




            if gewinner == 1:
                spieler1_counter += 1

            elif gewinner == 2:
                spieler2_counter += 1


            if startspieler == 1:
                spieler = 2
                startspieler = 2
            elif startspieler == 2:
                spieler = 1
                startspieler = 1

            print(f"Spieler1: {spieler1_counter}")
            print(f"Spieler2: {spieler2_counter}")


            game_anzeigen()



            abfrage = True
            while abfrage:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        abfrage = False
                        multiplayer_laeuft = False
                        spiel_laeuft = False

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                        if screen.get_width() == STANDARD_FENSTER_BREITE and screen.get_height() == STANDARD_FENSTER_HOEHE:
                            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

                        else:
                            pygame.display.set_mode((STANDARD_FENSTER_BREITE, STANDARD_FENSTER_HOEHE))

                        FENSTER_HOEHE = screen.get_height()
                        FENSTER_BREITE = screen.get_width()

                        game_buttons = create_game_buttons()
                        menue_buttons = create_menu_buttons()

                        game_anzeigen()
                        score_anzeigen()

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                        for button in game_buttons:
                            if button.is_clicked(event.pos):
                                button.click_handler()
                                abfrage = False


                    elif event.type == pygame.MOUSEMOTION:

                        for button in game_buttons:
                            if button.is_hovering(event.pos):
                                if not button.is_hovered:
                                    button.is_hovered = True
                                    game_anzeigen()

                            elif button.is_hovered:
                                button.is_hovered = False
                                game_anzeigen()








# Button-Klasse
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WEISS
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        draw_color = GRAU if self.is_hovered else self.color
        pygame.draw.rect(surface, draw_color, self.rect,border_radius=5)
        text_surface = font.render(self.text, True, SCHWARZ)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def is_hovering(self, pos):
        return self.rect.collidepoint(pos)

    def click_handler(self):
        if self.action:
            self.action()


def menue_anzeigen():
    screen.blit(hintergrund, (0, 0))
    for button in menue_buttons:
        button.draw(screen)
    pygame.display.update()


def create_menu_buttons():
    global FENSTER_BREITE, Fenster_HOEHE
    return [
        Button("Singleplayer", FENSTER_BREITE / 2 - 100, FENSTER_HOEHE / 2 - 100, 200, 40, action=start_singleplayer),
        Button("Multiplayer", FENSTER_BREITE / 2 - 100, FENSTER_HOEHE / 2, 200, 40, action=start_multiplayer),
    ]

# Funktionen für die verschiedenen Spielzustände
def start_singleplayer():
    global spielzustand
    spielzustand = "singleplayer"
    print("Singleplayer-Spiel gestartet")


def start_multiplayer():
    global spielzustand
    spielzustand = "multiplayer"
    print("Multiplayer-Spiel gestartet")

def game_anzeigen():
    screen.blit(hintergrund, (0, 0))
    for button in game_buttons:
        button.draw(screen)

    score_anzeigen()
    pygame.display.flip()


def create_game_buttons():
    global FENSTER_BREITE,FENSTER_HOEHE
    return [
        Button("Weiterspielen", FENSTER_BREITE / 2 - 100, FENSTER_HOEHE / 2 - 100, 200, 40, action=weiterspielen),
        Button("Hauptmenü", FENSTER_BREITE / 2 - 100, FENSTER_HOEHE / 2, 200, 40, action=hauptmenue),
    ]




def weiterspielen():
    global circle_zaehler, circle_auswahl, rect_zaehler, rect_auswahl, used_index, multiplayer_laeuft
    multiplayer_laeuft = True

    circle_zaehler = 0
    circle_auswahl = []
    rect_zaehler = 0
    rect_auswahl = []
    used_index = []

    update_game()

    print("Weiterspielen")


def hauptmenue():
    global  multiplayer_laeuft, spielzustand
    multiplayer_laeuft = False
    spielzustand = "menue"
    menue_anzeigen()  # Hier die Anzeige auslösen

    print("Hauptmenü")



def score_anzeigen():
    global spieler1_counter, spieler2_counter, spieler

    # Texte für die Anzeige
    text_score = font.render(f"Score:", True, SCHWARZ)

    if spieler == 1:
        text_spieler1 = bigfont.render(f"Spieler □: {spieler1_counter}", True, BLAU)
    else:
        text_spieler1 = font.render(f"Spieler □: {spieler1_counter}", True, SCHWARZ)

    if spieler == 2:
        text_spieler2 = bigfont.render(f"Spieler ○: {spieler2_counter}", True, BLAU)
    else:
        text_spieler2 = font.render(f"Spieler ○: {spieler2_counter}", True, SCHWARZ)

    # Text-Rechtecke erstellen
    text_score_rect = text_score.get_rect()
    text_spieler1_rect = text_spieler1.get_rect()
    text_spieler2_rect = text_spieler2.get_rect()

    # Berechne die Größe des Rechtecks
    max_breite = max(text_score_rect.width, text_spieler1_rect.width, text_spieler2_rect.width)
    rect_hoehe = text_score_rect.height + text_spieler1_rect.height + text_spieler2_rect.height + 20 # Abstand zu den Texten
    rect_breite = max_breite + 20 # Abstand zum Text

    # Positionen des Rechteckes
    rect_x = 10
    rect_y = 10
    rect = pygame.Rect(rect_x, rect_y, rect_breite, rect_hoehe+10) # Erstelle das Rect
    # Abgerundetes Rechteck
    pygame.draw.rect(screen, (255,255,255,0), rect, border_radius=10)
    pygame.draw.rect(screen, BLAU, rect, border_radius=10, width=2)

    # Positionierung der Texte innerhalb des Rechtecks
    text_score_rect.topleft = (rect_x + 10, rect_y + 10) # Position des ersten Textes
    text_spieler1_rect.topleft = (rect_x + 10, text_score_rect.bottom + 5)  # Text unterhalb von Score
    text_spieler2_rect.topleft = (rect_x + 10, text_spieler1_rect.bottom + 5)  # Text unterhalb von Spieler 1

    # Blitte alle Texte auf den Screen
    screen.blit(text_score, text_score_rect)
    screen.blit(text_spieler1, text_spieler1_rect)
    screen.blit(text_spieler2, text_spieler2_rect)




def update_game():
    global  spieler
    screen.blit(hintergrund, (0, 0))
    zeichne_spielfeld(SCHWARZ, 5, screen, FENSTER_BREITE, FENSTER_HOEHE)
    show_auswahl(circle_auswahl, rect_auswahl)
    score_anzeigen()

    pygame.display.update()


# Fenster erstellen
screen = pygame.display.set_mode((FENSTER_BREITE, FENSTER_HOEHE))
pygame.display.set_caption("TicTacToe")
screen.blit(hintergrund, (0, 0))
menue_buttons = create_menu_buttons()
game_buttons = create_game_buttons()

menue_anzeigen()
pygame.display.update()

spielzustand = "menue"

# Hauptschleife
spiel_laeuft = True
while spiel_laeuft:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spiel_laeuft = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if spielzustand == "menue":
                for button in menue_buttons:
                    if button.is_clicked(event.pos):
                        button.click_handler()


        elif event.type == pygame.MOUSEMOTION:
            if spielzustand == "menue":
                for button in menue_buttons:
                    if button.is_hovering(event.pos):
                        if not button.is_hovered:
                            button.is_hovered = True
                            menue_anzeigen()
                    elif button.is_hovered:
                        button.is_hovered = False
                        menue_anzeigen()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            if screen.get_width() == STANDARD_FENSTER_BREITE and screen.get_height() == STANDARD_FENSTER_HOEHE:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

            else:
                pygame.display.set_mode((STANDARD_FENSTER_BREITE, STANDARD_FENSTER_HOEHE))

            FENSTER_HOEHE = screen.get_height()
            FENSTER_BREITE = screen.get_width()

            screen.blit(hintergrund, (0, 0))

            menue_buttons = create_menu_buttons()
            menue_anzeigen()
            pygame.display.update()

        # Spielzustand prüfen und entsprechend reagieren
        if spielzustand == "multiplayer":
            screen.blit(hintergrund, (0, 0))
            multiplayer_anzeigen(SCHWARZ)
        if spielzustand == "singleplayer":
            screen.blit(hintergrund, (0, 0))
            singleplayer_anzeigen(SCHWARZ)

pygame.quit()
