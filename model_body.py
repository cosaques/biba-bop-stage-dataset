import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class HumanModel:
    def __init__(self, measures):
        """
        Initialise le modèle humain avec les mesures fournies
        
        Args:
            measures (dict): Dictionnaire contenant les mesures corporelles
        """
        self.measures = measures
        
        # Calcul des proportions
        self.head_height = measures['height'] / 8
        self.torso_height = measures['height'] * 0.3
        self.leg_height = measures['inseam']
        
        # Calcul des rayons
        self.head_radius = (measures.get('head', 55) / math.pi / 2)
        self.chest_radius = measures['chest'] / (2 * math.pi)
        self.waist_radius = measures['waist'] / (2 * math.pi)
        self.hips_radius = measures['hips'] / (2 * math.pi)
        self.arm_radius = measures.get('arm_circumference', 30) / (2 * math.pi)
        self.leg_radius = measures.get('leg_circumference', 40) / (2 * math.pi)
        
        self.angle = 0
        self.quadric = gluNewQuadric()
        
    def draw_sphere(self, radius, slices=20, stacks=20):
        gluSphere(self.quadric, radius, slices, stacks)
        
    def draw_cylinder(self, radius, height, slices=20, stacks=20):
        gluCylinder(self.quadric, radius, radius, height, slices, stacks)
        
    def draw_head(self):
        glPushMatrix()
        glTranslatef(0, self.head_height/2 + self.torso_height + self.leg_height, 0)
        self.draw_sphere(self.head_radius)
        glPopMatrix()
        
    def draw_torso(self):
        glPushMatrix()
        glTranslatef(0, self.leg_height + self.torso_height/2, 0)
        gluCylinder(self.quadric, 
                   self.chest_radius, 
                   self.waist_radius, 
                   self.torso_height, 
                   20, 20)
        glPopMatrix()
        
    def draw_hips(self):
        glPushMatrix()
        glTranslatef(0, self.leg_height, 0)
        gluCylinder(self.quadric, 
                   self.waist_radius, 
                   self.hips_radius, 
                   self.torso_height * 0.3, 
                   20, 20)
        glPopMatrix()
        
    def draw_limbs(self):
        arm_length = self.measures['arm_length']
        
        # Bras droit
        glPushMatrix()
        glTranslatef(self.chest_radius, self.leg_height + self.torso_height * 0.8, 0)
        glRotatef(90, 0, 1, 0)
        self.draw_cylinder(self.arm_radius, arm_length)
        glPopMatrix()
        
        # Bras gauche
        glPushMatrix()
        glTranslatef(-self.chest_radius, self.leg_height + self.torso_height * 0.8, 0)
        glRotatef(90, 0, 1, 0)
        self.draw_cylinder(self.arm_radius, arm_length)
        glPopMatrix()
        
        # Jambes
        glPushMatrix()
        glTranslatef(self.hips_radius * 0.4, 0, 0)
        glRotatef(90, 1, 0, 0)
        self.draw_cylinder(self.leg_radius, self.leg_height)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-self.hips_radius * 0.4, 0, 0)
        glRotatef(90, 1, 0, 0)
        self.draw_cylinder(self.leg_radius, self.leg_height)
        glPopMatrix()
        
    def draw(self):
        glPushMatrix()
        glRotatef(self.angle, 0, 1, 0)
        glColor3f(0.9, 0.75, 0.65)
        
        self.draw_hips()
        self.draw_torso()
        self.draw_head()
        self.draw_limbs()
        
        glPopMatrix()
        
        self.angle = (self.angle + 0.5) % 360

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 500.0)
    glTranslatef(0.0, 0.0, -300)
    glEnable(GL_DEPTH_TEST)
    
    default_measures = {
        'height': 175,
        'chest': 95,
        'waist': 80,
        'hips': 95,
        'inseam': 80,
        'arm_length': 60,
        'head': 55,
        'arm_circumference': 30,
        'leg_circumference': 40
    }
    
    human = HumanModel(default_measures)
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: glRotatef(1, -1, 0, 0)
        if keys[pygame.K_DOWN]: glRotatef(1, 1, 0, 0)
        if keys[pygame.K_LEFT]: glRotatef(1, 0, -1, 0)
        if keys[pygame.K_RIGHT]: glRotatef(1, 0, 1, 0)
        if keys[pygame.K_w]: glTranslatef(0, 0, 1)
        if keys[pygame.K_s]: glTranslatef(0, 0, -1)
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        human.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()