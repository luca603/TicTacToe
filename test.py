import pygame
import sys
import random

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

VERHAELTNIS = screen_width / screen_height

# Farben
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)
ROT = (255, 0, 0)
BLAU = (0, 0, 255)
GRAU = (200, 200, 200)

# Schriftarten erstellen
font = pygame.font.Font(None, 36)

# Hintergrund laden (Anpassung an deine Pfade)
hintergrund = pygame.image.load('Grafiken/hintergrund.jpg')
hintergrund = pygame.transform.scale(hintergrund, (screen_width, screen_height))

# Fenster erstellen
screen = pygame.display.set_mode((FENSTER_BREITE, FENSTER_HOEHE))
pygame.display.set_caption("TicTacToe")


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
        pygame.draw.rect(surface, draw_color, self.rect)
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


def create_menu_buttons():
    return [
        Button("Singleplayer", FENSTER_BREITE / 2 - 100, FENSTER_HOEHE / 2 - 100, 200, 40, action=start_singleplayer),
        Button("Multiplayer", FENSTER_BREITE / 2 - 100, FENSTER_HOEHE / 2, 200, 40, action=start_multiplayer),
    ]


def menue_anzeigen():
    screen.blit(hintergrund, (0, 0))
    for button in menue_buttons:
        button.draw(screen)
    pygame.display.update()


# Funktionen für die verschiedenen Spielzustände
def start_singleplayer():
    global spielzustand
    spielzustand = "singleplayer"
    print("Singleplayer-Spiel gestartet")


def start_multiplayer():
    global spielzustand
    spielzustand = "multiplayer"
    print("Multiplayer-Spiel gestartet")


# Spielfeld zeichnen
def zeichne_spielfeld(color, linienstaerke, oberflaeche):
    # Füllen des Hintergrundes mit der Farbe Weiß

    # obere linke Ecke
    x = (FENSTER_BREITE - zellen_groesse * 3) / 2
    y = (FENSTER_HOEHE - zellen_groesse * 3) / 2

    # Vertikale Linien
    for spalte in range(1, spielfeld_grosse):
        x += zellen_groesse
        pygame.draw.line(oberflaeche, color, (x, y), (x, y + (zellen_groesse * 3)), linienstaerke)

    # obere linke Ecke
    x = (FENSTER_BREITE - zellen_groesse * 3) / 2
    y = (FENSTER_HOEHE - zellen_groesse * 3) / 2

    # Horizontale Linien
    for reihe in range(1, spielfeld_grosse):
        y += zellen_groesse
        pygame.draw.line(screen, color, (x, y), (x + (zellen_groesse * 3), y), linienstaerke)

    pygame.display.update()


# Funktion um ein Feld hervorzuheben (optional)
def feld_hervorheben(oberflaeche, feld_index, farbe):
    if feld_index is None:
        return

    y = (FENSTER_HOEHE - zellen_groesse * spielfeld_grosse) / 2
    x = (FENSTER_BREITE - ZELLEN_GROESSE * SPIELFELD_GROESSE) / 2

    reihe = feld_index // SPIELFELD_GROESSE
    spalte = feld_index % SPIELFELD_GROESSE

    x += spalte * ZELLEN_GROESSE
    y += reihe * ZELLEN_GROESSE
    feld_rect = pygame.Rect(x, y, ZELLEN_GROESSE, ZELLEN_GROESSE)
    pygame.draw.rect(oberflaeche, farbe, feld_rect)


# Klick auf das Spielfeld
def feld_ausgewaehlt(maus_position):
    # obere linke Feldecke
    y = (FENSTER_HOEHE - zellen_groesse * 3) / 2

    for reihe in range(spielfeld_grosse):
        x = (FENSTER_BREITE - zellen_groesse * 3) / 2
        for spalte in range(spielfeld_grosse):

            feld_rect = pygame.Rect(x, y, zellen_groesse, zellen_groesse)  # Erstelle ein Rect mit allen Parametern
            x += zellen_groesse
            #pygame.draw.rect(screen, SCHWARZ, feld_rect)

            if feld_rect.collidepoint(maus_position) and spielfeld[reihe * spielfeld_grosse + spalte] == " ":
                #pygame.draw.rect(screen, WEISS, feld_rect)
                #pygame.display.update()
                return reihe * spielfeld_grosse + spalte  # Die Stelle im Spielfeld

        y += zellen_groesse

    return None


# Gewinnprüfung
def spiel_gewonnen(symbol):
    for reihe in range(spielfeld_grosse):
        if all(spielfeld[reihe * spielfeld_grosse + i] == symbol for i in range(spielfeld_grosse)):
            return True  # Reihe gleich

    for spalte in range(spielfeld_grosse):
        if all(spielfeld[i * spielfeld_grosse + spalte] == symbol for i in range(spielfeld_grosse)):
            return True  # Spalte gleich

    # Diagonale
    if all(spielfeld[i * spielfeld_grosse + i] == symbol for i in range(spielfeld_grosse)):
        return True

    if all(spielfeld[i * spielfeld_grosse + (spielfeld_grosse - 1 - i)] == symbol for i in range(spielfeld_grosse)):
        return True

    return False


# Unentschieden
def unentschieden():
    return all(zelle != " " for zelle in spielfeld)  # Ist das Spielfeld voll


# Spieler wechseln
def wechsel_spieler():
    global spieler
    spieler = "O" if spieler == "X" else "X"


def multiplayer_anzeigen(color):
    screen.blit(hintergrund, (0, 0))
    zeichne_spielfeld(SCHWARZ, 3)
    pygame.display.update()


def singleplayer_anzeigen(color):
    screen.blit(hintergrund, (0, 0))
    zeichne_spielfeld(SCHWARZ, 5, screen)
    pygame.display.update()


# Spielfeld
spielfeld_grosse = 3  # 3x3
zellen_groesse = STANDARD_FENSTER_HOEHE // spielfeld_grosse * 0.7  # Berechne die Zellengröße basierend auf der Fensterbreite

# Speichere alle Felder als Liste mit leeren Strings
spielfeld = [" " for _ in range(spielfeld_grosse * spielfeld_grosse)]

# Globale Variable für den Spielzustand (Menü, Singleplayer, Multiplayer)
spielzustand = "menue"
menue_buttons = create_menu_buttons()
# Speichern der letzten Fenstergröße
letzte_fenster_groesse = (FENSTER_BREITE, FENSTER_HOEHE)
neue_breite = 0
neue_hoehe = 0
resize = False


# Initiales Zeichnen des Spielfelds
zeichne_spielfeld(SCHWARZ, 5, screen)
pygame.display.update()

if spielzustand == "menue":
    menue_buttons = create_menu_buttons()
    menue_anzeigen()

# Hauptschleife
spiel_laeuft = True
while spiel_laeuft:

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spiel_laeuft = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if spielzustand == "menue":
                for button in menue_buttons:
                    if button.is_clicked(event.pos):
                        button.click_handler()

        if event.type == pygame.MOUSEMOTION:
            if spielzustand == "menue":
                for button in menue_buttons:
                    if button.is_hovering(event.pos):
                        if not button.is_hovered:
                            button.is_hovered = True
                            menue_anzeigen()
                    elif button.is_hovered:
                        button.is_hovered = False
                        menue_anzeigen()
            elif spielzustand == "singleplayer":
                maus_pos = event.pos
                feld_index = feld_ausgewaehlt(maus_pos)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
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

    if spielzustand == "singleplayer":
        singleplayer_anzeigen(SCHWARZ)
    elif spielzustand == "multiplayer":
        multiplayer_anzeigen(SCHWARZ)


def singleplayer_anzeigen(farbe):
    screen.fill(farbe)
    pygame.display.update()


def multiplayer_anzeigen(farbe):
    screen.fill(farbe)
    pygame.display.update()
