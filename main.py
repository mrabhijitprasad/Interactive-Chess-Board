import pygame
import pygame.locals
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
import random

# Initialize GLUT first
glutInit()

# Roll number last 2 digits
ROLL_LAST_2 = 2

# Dynamic configuration based on roll number 02
BOARD_SIZE = 8 + (ROLL_LAST_2 % 3)  # 8-10 squares
PIECE_VARIATION = (ROLL_LAST_2 % 5) + 1  # 1-5
ANIMATION_COMPLEXITY = (ROLL_LAST_2 % 4) + 2  # 2-5 keyframes
SPECIAL_EFFECTS = ROLL_LAST_2 % 3  # 0-2

class InteractiveChessboard:
    def __init__(self):
        self.is_perspective = True
        self.rotation_x = 25
        self.rotation_y = 0
        self.zoom = -12
        self.animating = False
        self.animation_time = 0
        self.keyframes = []
        self.piece_animations = {}
        self.setup_keyframes()
        self.setup_piece_animations()
        
        # Roll number 02 specific features
        self.grid_enabled = True
        self.wireframe_mode = False
        self.color_scheme = ROLL_LAST_2 % 3
        
    def setup_keyframes(self):
        # Enhanced keyframes for roll number 02
        self.keyframes = [
            {"time": 0, "rotation_x": 25, "rotation_y": 0, "zoom": -12, "height": 0},
            {"time": 3, "rotation_x": 60, "rotation_y": 90, "zoom": -8, "height": 2},
            {"time": 6, "rotation_x": 30, "rotation_y": 180, "zoom": -10, "height": -1},
            {"time": 9, "rotation_x": 10, "rotation_y": 270, "zoom": -15, "height": 1},
            {"time": 12, "rotation_x": 25, "rotation_y": 360, "zoom": -12, "height": 0}
        ]
    
    def setup_piece_animations(self):
        # Individual piece animations for roll number 02
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % PIECE_VARIATION == 0:
                    self.piece_animations[(row, col)] = {
                        'phase': random.uniform(0, 2 * math.pi),
                        'amplitude': 0.2 + (row * col) % 3 * 0.1,
                        'speed': 1 + (row + col) % 3
                    }
    
    def get_color_scheme(self, is_white):
        # Different color schemes based on roll number
        if self.color_scheme == 0:  # Classic
            return [1.0, 0.9, 0.8] if is_white else [0.4, 0.2, 0.0]
        elif self.color_scheme == 1:  # Modern
            return [0.9, 0.95, 1.0] if is_white else [0.1, 0.3, 0.5]
        else:  # Fantasy
            return [0.8, 1.0, 0.8] if is_white else [0.5, 0.2, 0.7]
    
    def draw_enhanced_square(self, x, z, is_white, height_variation=0):
        y = height_variation * 0.2
        vertices = [
            [x, y, z],
            [x + 1, y, z],
            [x + 1, y, z + 1],
            [x, y, z + 1]
        ]
        
        color = self.get_color_scheme(is_white)
        
        # Draw square with enhanced visuals
        glBegin(GL_QUADS)
        glColor3f(color[0], color[1], color[2])
        for vertex in vertices:
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
        
        # Enhanced border for roll number 02
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glColor3f(0.0, 0.0, 0.0)
        for vertex in vertices:
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
        glLineWidth(1.0)
    
    def draw_advanced_piece(self, x, z, is_white, piece_type, animation_time=0):
        base_y = 0.3
        anim_data = self.piece_animations.get((int(z + BOARD_SIZE/2), int(x + BOARD_SIZE/2)), None)
        
        if anim_data:
            hover_height = math.sin(animation_time * anim_data['speed'] + anim_data['phase']) * anim_data['amplitude']
            base_y += hover_height
        
        piece_color = [0.95, 0.95, 0.95] if is_white else [0.05, 0.05, 0.05]
        
        glPushMatrix()
        glTranslatef(x + 0.5, base_y, z + 0.5)
        
        # Piece-specific dimensions for roll number 02
        piece_heights = {
            "pawn": 0.8, "rook": 1.2, "knight": 1.1, 
            "bishop": 1.3, "queen": 1.6, "king": 1.8
        }
        
        height = piece_heights.get(piece_type, 1.0)
        radius = 0.25 + (ROLL_LAST_2 % 3) * 0.05
        
        # Draw sophisticated piece without glutSolidSphere
        slices = 20
        
        # Main body - using custom cylinder instead of glut
        glColor3f(piece_color[0], piece_color[1], piece_color[2])
        self.draw_cylinder(radius, height, slices)
        
        # Custom top for different pieces (replacing glutSolidSphere)
        if piece_type in ["king", "queen"]:
            glColor3f(0.8, 0.8, 0.0)  # Gold color for crown
            self.draw_sphere(radius * 0.6, 10, 10)
        
        glPopMatrix()
    
    def draw_cylinder(self, radius, height, slices):
        # Draw cylinder body
        glBegin(GL_QUAD_STRIP)
        for i in range(slices + 1):
            angle = 2 * math.pi * i / slices
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glVertex3f(x, 0, z)
            glVertex3f(x, height, z)
        glEnd()
        
        # Draw top
        glBegin(GL_POLYGON)
        for i in range(slices):
            angle = 2 * math.pi * i / slices
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glVertex3f(x, height, z)
        glEnd()
        
        # Draw bottom
        glBegin(GL_POLYGON)
        for i in range(slices):
            angle = 2 * math.pi * i / slices
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glVertex3f(x, 0, z)
        glEnd()
    
    def draw_sphere(self, radius, slices, stacks):
        # Custom sphere implementation to replace glutSolidSphere
        for i in range(slices):
            lat0 = math.pi * (-0.5 + float(i) / slices)
            z0 = math.sin(lat0) * radius
            zr0 = math.cos(lat0) * radius

            lat1 = math.pi * (-0.5 + float(i + 1) / slices)
            z1 = math.sin(lat1) * radius
            zr1 = math.cos(lat1) * radius

            glBegin(GL_QUAD_STRIP)
            for j in range(stacks + 1):
                lng = 2 * math.pi * float(j) / stacks
                x = math.cos(lng)
                y = math.sin(lng)
                glVertex3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()
    
    def draw_coordinate_grid(self):
        if not self.grid_enabled:
            return
            
        glBegin(GL_LINES)
        glColor3f(0.3, 0.3, 0.3)
        
        # Draw grid lines
        for i in range(-BOARD_SIZE, BOARD_SIZE + 1):
            glVertex3f(i, -0.1, -BOARD_SIZE)
            glVertex3f(i, -0.1, BOARD_SIZE)
            glVertex3f(-BOARD_SIZE, -0.1, i)
            glVertex3f(BOARD_SIZE, -0.1, i)
        glEnd()
    
    def draw_board(self):
        current_time = time.time()
        
        # Draw coordinate grid
        self.draw_coordinate_grid()
        
        # Draw chessboard squares with height variation
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                is_white = (row + col) % 2 == 0
                x = col - BOARD_SIZE / 2
                z = row - BOARD_SIZE / 2
                
                # Height variation for visual interest
                height_var = math.sin((row + col) * 0.5 + current_time * 0.5) * 0.3
                self.draw_enhanced_square(x, z, is_white, height_var)
        
        # Draw pieces with animations
        piece_types = ["pawn", "rook", "knight", "bishop", "queen", "king"]
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Strategic piece placement for roll number 02
                if (row < 2 or row >= BOARD_SIZE - 2) and (col % (PIECE_VARIATION + 1) == 0):
                    is_white = row >= BOARD_SIZE - 2
                    x = col - BOARD_SIZE / 2
                    z = row - BOARD_SIZE / 2
                    piece_type = piece_types[(row * 3 + col) % len(piece_types)]
                    
                    self.draw_advanced_piece(x, z, is_white, piece_type, current_time)
    
    def update_animation(self, delta_time):
        if not self.animating:
            return
        
        self.animation_time += delta_time
        
        if self.animation_time > self.keyframes[-1]["time"]:
            self.animation_time = 0
            self.animating = False
            return
        
        # Smooth interpolation between keyframes
        for i in range(len(self.keyframes) - 1):
            if self.keyframes[i]["time"] <= self.animation_time <= self.keyframes[i + 1]["time"]:
                t1 = self.keyframes[i]["time"]
                t2 = self.keyframes[i + 1]["time"]
                alpha = (self.animation_time - t1) / (t2 - t1)
                
                # Smooth interpolation
                smooth_alpha = self.smoothstep(alpha)
                
                self.rotation_x = self.lerp(self.keyframes[i]["rotation_x"], 
                                          self.keyframes[i + 1]["rotation_x"], smooth_alpha)
                self.rotation_y = self.lerp(self.keyframes[i]["rotation_y"], 
                                          self.keyframes[i + 1]["rotation_y"], smooth_alpha)
                self.zoom = self.lerp(self.keyframes[i]["zoom"], 
                                    self.keyframes[i + 1]["zoom"], smooth_alpha)
                break
    
    def smoothstep(self, x):
        return x * x * (3 - 2 * x)
    
    def lerp(self, a, b, alpha):
        return a + (b - a) * alpha
    
    def toggle_projection(self):
        self.is_perspective = not self.is_perspective
        print(f"Projection: {'Perspective' if self.is_perspective else 'Orthographic'}")
    
    def toggle_wireframe(self):
        self.wireframe_mode = not self.wireframe_mode
        if self.wireframe_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        print(f"Wireframe: {'ON' if self.wireframe_mode else 'OFF'}")
    
    def toggle_grid(self):
        self.grid_enabled = not self.grid_enabled
        print(f"Grid: {'ON' if self.grid_enabled else 'OFF'}")
    
    def cycle_color_scheme(self):
        self.color_scheme = (self.color_scheme + 1) % 3
        schemes = ["Classic", "Modern", "Fantasy"]
        print(f"Color Scheme: {schemes[self.color_scheme]}")
    
    def start_animation(self):
        self.animating = True
        self.animation_time = 0
        print("Animation started!")
    
    def reset_view(self):
        self.rotation_x = 25
        self.rotation_y = 0
        self.zoom = -12
        self.animating = False
        print("View reset")
    
    def draw(self):
        # Set up projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        aspect_ratio = 800 / 600
        if self.is_perspective:
            gluPerspective(45, aspect_ratio, 0.1, 50.0)
        else:
            glOrtho(-10, 10, -10, 10, 0.1, 50.0)
        
        # Set up modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 5, self.zoom, 0, 0, 0, 0, 1, 0)
        
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        # Enable depth testing for better 3D
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Draw the scene
        self.draw_board()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption(f"Roll 02 Chessboard - Size: {BOARD_SIZE}x{BOARD_SIZE} | Pieces: Lvl {PIECE_VARIATION}")
    
    # Initialize OpenGL
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.2, 1.0)
    
    chessboard = InteractiveChessboard()
    
    clock = pygame.time.Clock()
    last_time = time.time()
    
    print("=" * 50)
    print("ROLL NUMBER 02 - ENHANCED CHESSBOARD")
    print("=" * 50)
    print("Board Configuration:")
    print(f"  Size: {BOARD_SIZE}x{BOARD_SIZE}")
    print(f"  Piece Variation: Level {PIECE_VARIATION}")
    print(f"  Animation Complexity: {ANIMATION_COMPLEXITY} keyframes")
    print(f"  Special Effects: Level {SPECIAL_EFFECTS}")
    print("\nControls:")
    print("  SPACE - Toggle Perspective/Orthographic")
    print("  A - Start Animation Sequence")
    print("  R - Reset View")
    print("  W - Toggle Wireframe Mode")
    print("  G - Toggle Coordinate Grid")
    print("  C - Cycle Color Schemes")
    print("  Mouse Drag - Rotate View")
    print("  Mouse Wheel - Zoom In/Out")
    print("=" * 50)
    
    dragging = False
    last_mouse_pos = (0, 0)
    
    while True:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    chessboard.toggle_projection()
                elif event.key == pygame.K_a:
                    chessboard.start_animation()
                elif event.key == pygame.K_r:
                    chessboard.reset_view()
                elif event.key == pygame.K_w:
                    chessboard.toggle_wireframe()
                elif event.key == pygame.K_g:
                    chessboard.toggle_grid()
                elif event.key == pygame.K_c:
                    chessboard.cycle_color_scheme()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
                    last_mouse_pos = event.pos
                elif event.button == 4:  # Mouse wheel up
                    chessboard.zoom = min(chessboard.zoom + 0.5, -5)
                elif event.button == 5:  # Mouse wheel down
                    chessboard.zoom = max(chessboard.zoom - 0.5, -20)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            
            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                chessboard.rotation_y += dx * 0.5
                chessboard.rotation_x += dy * 0.5
                last_mouse_pos = event.pos
        
        chessboard.update_animation(delta_time)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        chessboard.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()