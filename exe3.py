import cv2
import numpy as np
import time

# Initialize game parameters
width, height = 800, 400
ball_radius = 20
ball_pos = [100, height - 30 - ball_radius]
ball_vel = 0
gravity = 1
jump_strength = -20
obstacle_width, obstacle_height = 20, 40
obstacle_speed = 10
score = 0

# Create a black image
game_window = np.zeros((height, width, 3), dtype=np.uint8)

# Function to draw the ball
def draw_ball(img, position, radius):
    cv2.circle(img, position, radius, (255, 255, 255), -1)

# Function to draw an obstacle
def draw_obstacle(img, position, width, height):
    cv2.rectangle(img, position, (position[0] + width, position[1] + height), (255, 255, 255), -1)

# Function to check for collision
def check_collision(ball_pos, ball_radius, obstacle_pos, obstacle_width, obstacle_height):
    if (ball_pos[0] + ball_radius > obstacle_pos[0] and
        ball_pos[0] - ball_radius < obstacle_pos[0] + obstacle_width and
        ball_pos[1] + ball_radius > obstacle_pos[1]):
        return True
    return False

# Main game loop
obstacle_pos = [width, height - 30 - obstacle_height]
game_over = False
while True:
    game_window.fill(0)
    
    # Draw the ball
    draw_ball(game_window, tuple(ball_pos), ball_radius)
    
    # Move the ball
    ball_pos[1] += ball_vel
    ball_vel += gravity
    if ball_pos[1] > height - 30 - ball_radius:
        ball_pos[1] = height - 30 - ball_radius
        ball_vel = 0
    
    # Draw the obstacle
    draw_obstacle(game_window, tuple(obstacle_pos), obstacle_width, obstacle_height)
    
    # Move the obstacle
    obstacle_pos[0] -= obstacle_speed
    if obstacle_pos[0] < -obstacle_width:
        obstacle_pos[0] = width
        score += 1
    
    # Check for collision
    if check_collision(ball_pos, ball_radius, obstacle_pos, obstacle_width, obstacle_height):
        game_over = True
    
    # Display the score
    cv2.putText(game_window, f'Score: {score}', (width - 150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Show the game window
    cv2.imshow('Dino Game', game_window)
    
    # Check for key presses
    key = cv2.waitKey(30) & 0xFF
    if key == ord(' '):
        if ball_pos[1] == height - 30 - ball_radius:
            ball_vel = jump_strength
    elif key == ord('q') or game_over:
        break

# Display 'Game Over' message
cv2.putText(game_window, 'Game Over', (width // 2 - 100, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
cv2.imshow('Dino Game', game_window)
cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()
