from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# =======================
# Mesures corporelles (en cm)
# =======================
taille = 187.0
epaule_largeur = 48.46
tour_poitrine = 96.51
tour_taille = 83.59
longueur_bras = 66.66
longueur_avant_bras = 27.62
tour_cuisse = 59.55
tour_cheville = 27.13
hauteur_jambe = 87.33
hauteur_tete = 24.0  # estimation

# Conversion en mètres
def cm_to_m(val):
    return val / 100.0

# =======================
# Fonctions dessin primitives
# =======================
def draw_cylinder(radius, height):
    quad = gluNewQuadric()
    gluCylinder(quad, radius, radius, height, 32, 32)
    gluDisk(quad, 0, radius, 32, 1)
    glPushMatrix()
    glTranslatef(0, 0, height)
    gluDisk(quad, 0, radius, 32, 1)
    glPopMatrix()
    gluDeleteQuadric(quad)

def draw_sphere(radius):
    quad = gluNewQuadric()
    gluSphere(quad, radius, 32, 32)
    gluDeleteQuadric(quad)

# =======================
# Dessin du corps
# =======================
def draw_body():
    glPushMatrix()
    # Placer les pieds à z = 0
    glTranslatef(0, 0, 0)

    # Torse
    glPushMatrix()
    glTranslatef(0, cm_to_m(hauteur_jambe), 0)
    glScalef(cm_to_m(tour_poitrine)/2, cm_to_m(taille)/4, cm_to_m(tour_poitrine)/2)
    draw_sphere(0.5)
    glPopMatrix()

    # Tête
    glPushMatrix()
    glTranslatef(0, cm_to_m(hauteur_jambe) + cm_to_m(taille)/4 + cm_to_m(hauteur_tete)/2, 0)
    draw_sphere(cm_to_m(hauteur_tete)/2)
    glPopMatrix()

    # Bras gauche
    glPushMatrix()
    glTranslatef(cm_to_m(epaule_largeur)/2, cm_to_m(hauteur_jambe) + cm_to_m(taille)/4, 0)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(cm_to_m(5), cm_to_m(longueur_bras))
    glPopMatrix()

    # Bras droit
    glPushMatrix()
    glTranslatef(-cm_to_m(epaule_largeur)/2, cm_to_m(hauteur_jambe) + cm_to_m(taille)/4, 0)
    glRotatef(-90, 0, 1, 0)
    draw_cylinder(cm_to_m(5), cm_to_m(longueur_bras))
    glPopMatrix()

    # Jambes
    glPushMatrix()
    glTranslatef(cm_to_m(10), 0, 0)
    draw_cylinder(cm_to_m(tour_cuisse)/4, cm_to_m(hauteur_jambe))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-cm_to_m(10), 0, 0)
    draw_cylinder(cm_to_m(tour_cuisse)/4, cm_to_m(hauteur_jambe))
    glPopMatrix()

    glPopMatrix()

# =======================
# OpenGL / GLUT
# =======================
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 1.0, 4.0,   # Position caméra
              0, 1.0, 0,     # Cible
              0, 1, 0)       # Orientation verticale

    glColor3f(0.8, 0.7, 0.6)
    draw_body()

    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.2, 0.2, 1)

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Modele corporel simplifie")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()
