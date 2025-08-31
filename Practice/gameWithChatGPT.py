# Python Single-Level Ice Racing Prototype (pygame)
# ------------------------------------------------------------
# Features
# - Single level, one camera (top-down fixed following player)
# - Low-friction ice physics with drift
# - Nitro boost + pickups
# - Simple AI opponents following waypoints
# - Particles for ice spray
# - Finish line + timer + basic HUD
# ------------------------------------------------------------
# How to run
#   1) Install pygame:    pip install pygame
#   2) Save this file as ice_race.py
#   3) Run:               python ice_race.py
# Controls:
#   W / Up    : Accelerate
#   S / Down  : Brake
#   A / Left  : Steer Left
#   D / Right : Steer Right
#   Space     : Nitro (if bar > 0)
#   R         : Restart level
#   ESC       : Quit
# ------------------------------------------------------------

import math
import random
import sys
import pygame
from pygame.math import Vector2 as V2

# ----------------------------- Config -----------------------------
WIN_W, WIN_H = 1024, 600
TRACK_W, TRACK_H = 2000, 3500
FPS = 120
RNG = random.Random(1337)

PI = math.pi

def clamp(x, a, b):
    return a if x < a else b if x > b else x

# --------------------------- World Objects ------------------------
class Particle:
    __slots__ = ("pos", "vel", "life", "max_life", "size")
    def __init__(self, pos, vel, life, size):
        self.pos = V2(pos)
        self.vel = V2(vel)
        self.life = life
        self.max_life = life
        self.size = size

class Sled:
    def __init__(self, pos, color, is_ai=False):
        self.pos = V2(pos)
        self.vel = V2(0, 0)
        self.heading_deg = 90.0
        self.target_steer = 0.0
        self.nitro = 0.5
        self.max_speed = 900.0
        self.color = color
        self.is_ai = is_ai
        self.wp_index = 0
        self.progress = 0.0

class Track:
    def __init__(self):
        self.length = 3000.0
        self.bounds = pygame.Rect(0, 0, TRACK_W, TRACK_H)
        self.obstacles = []  # list of pygame.Rect (axis-aligned)
        self.pickups = []    # list of (pos, active)
        self.finish_rect = pygame.Rect(100, int(self.length), TRACK_W-200, 12)

# --------------------------- Helpers ------------------------------

def frand(a, b):
    return RNG.uniform(a, b)

# Soft ice background as a repeated procedural texture rendered into a Surface

def make_ice_surface(w, h):
    surf = pygame.Surface((w, h))
    # Generate a subtle pattern
    for y in range(h):
        for x in range(w):
            nx, ny = x / w, y / h
            v = 0.5 + 0.5 * math.sin(8*nx + 5*ny) * 0.3 + 0.2 * math.sin(14*nx + 11*ny)
            c = int(200 + v * 30)
            surf.set_at((x, y), (c, min(255, c+15), 255))
    return surf

# ------------------------- Game Construction ----------------------

def build_track():
    t = Track()
    # Obstacles: ice cracks/blocks AABBs (simple collision)
    for _ in range(25):
        w = frand(60, 140)
        h = frand(18, 30)
        x = frand(200, TRACK_W-200)
        y = frand(300, t.length-300)
        r = pygame.Rect(0, 0, int(w), int(h))
        r.center = (int(x), int(y))
        t.obstacles.append(r)
    # Nitro pickups (pos, active)
    for _ in range(18):
        x = frand(150, TRACK_W-150)
        y = frand(200, t.length-200)
        t.pickups.append([V2(x, y), True])
    return t


def build_waypoints(track):
    pts = []
    cols = 6
    margin = 160.0
    step_y = track.length / 18.0
    for i in range(18):
        x = margin + (i % cols) * ((TRACK_W - 2*margin) / (cols - 1))
        y = 200.0 + i * step_y
        if i % 2 == 1:
            x = TRACK_W - x
        pts.append(V2(x, y))
    return pts

# ---------------------------- AI ---------------------------------

def update_ai(sled: Sled, waypoints, dt):
    target = waypoints[sled.wp_index]
    to = target - sled.pos
    ang_to = math.degrees(math.atan2(to.y, to.x))
    delta = math.sin(math.radians(ang_to - sled.heading_deg))
    sled.target_steer = clamp(delta * 2.0 + frand(-0.15, 0.15), -1.0, 1.0)
    if to.length() < 120.0:
        sled.wp_index = (sled.wp_index + 1) % len(waypoints)
    # Nitro regen
    sled.nitro = min(1.0, sled.nitro + dt * 0.15)

# --------------------------- Physics ------------------------------

def integrate_sled(s: Sled, steer, throttle, brake, nitro_on, dt):
    ACCEL = 600.0
    BRAKE = 900.0
    TURN = 120.0
    BASE_FRICTION = 0.6

    speed_ratio = clamp(s.vel.length() / s.max_speed, 0.0, 1.0)
    s.heading_deg += steer * TURN * dt * (0.5 + 0.5 * speed_ratio)

    forward = V2(math.cos(math.radians(s.heading_deg)), math.sin(math.radians(s.heading_deg)))
    right = V2(-forward.y, forward.x)

    vF = forward.dot(s.vel)
    vR = right.dot(s.vel)

    vF += throttle * ACCEL * dt
    vF -= brake * BRAKE * dt

    fr_long = BASE_FRICTION * 0.6
    fr_lat = BASE_FRICTION * 2.2
    vF -= vF * fr_long * dt
    vR -= vR * fr_lat * dt

    if nitro_on and s.nitro > 0.0:
        vF += 1100.0 * dt
        s.nitro = max(0.0, s.nitro - dt * 0.4)

    # Clamp speed
    speed = math.hypot(vF, vR)
    max_spd = s.max_speed + (300.0 if nitro_on else 0.0)
    if speed > max_spd:
        k = max_spd / speed
        vF *= k
        vR *= k

    s.vel = forward * vF + right * vR
    s.pos += s.vel * dt

    s.pos.x = clamp(s.pos.x, 40.0, TRACK_W - 40.0)
    s.pos.y = clamp(s.pos.y, 0.0, TRACK_H - 20.0)

    s.progress = max(s.progress, s.pos.y)

# --------------------------- Rendering ----------------------------

def draw_ice_background(screen, ice_tile, camera_y):
    # Tile a 512x512 pattern across the view for speed
    tile = pygame.transform.smoothscale(ice_tile, (512, 512))
    start_y = int((camera_y - WIN_H/2) // 512 * 512)
    for y in range(start_y, start_y + WIN_H + 512, 512):
        for x in range(0, WIN_W + 512, 512):
            screen.blit(tile, (x - 0, y - camera_y + WIN_H/2))


def draw_track(screen, track, camera_y):
    # Borders
    left = pygame.Rect(20, -camera_y + WIN_H/2, 8, int(track.length + 400))
    right = pygame.Rect(TRACK_W-28, -camera_y + WIN_H/2, 8, int(track.length + 400))
    pygame.draw.rect(screen, (170, 200, 230), left)
    pygame.draw.rect(screen, (170, 200, 230), right)

    # Obstacles
    for r in track.obstacles:
        rr = r.copy()
        rr.y = rr.y - camera_y + WIN_H/2
        pygame.draw.rect(screen, (160, 200, 230), rr)
        pygame.draw.rect(screen, (140, 170, 200), rr, 2)

    # Pickups
    for pos, active in track.pickups:
        if not active:
            continue
        p = (int(pos.x), int(pos.y - camera_y + WIN_H/2))
        pygame.draw.circle(screen, (255, 255, 255), p, 10)
        pygame.draw.circle(screen, (100, 200, 255), p, 12, 3)

    # Finish line
    fr = track.finish_rect.copy()
    fr.y = fr.y - camera_y + WIN_H/2
    pygame.draw.rect(screen, (255, 255, 255), fr)
    pygame.draw.rect(screen, (0, 0, 0), fr.inflate(0, 12), 6)


def draw_sled(screen, sled: Sled, camera_y, outline=False):
    # Triangle body
    p0 = V2(20, 0)
    p1 = V2(-14, -10)
    p2 = V2(-14, 10)
    pts = [p0, p1, p2]
    ang = math.radians(sled.heading_deg)
    rot = V2(math.cos(ang), math.sin(ang))
    right = V2(-rot.y, rot.x)
    world = []
    for p in pts:
        world.append((sled.pos + rot * p.x + right * p.y))
    screen_pts = [(int(w.x), int(w.y - camera_y + WIN_H/2)) for w in world]
    if outline:
        pygame.draw.polygon(screen, (255, 255, 255), screen_pts, 3)
    pygame.draw.polygon(screen, sled.color, screen_pts)


def draw_particles(screen, particles, camera_y):
    for p in particles:
        a = int(max(0.0, p.life / p.max_life) * 180)
        col = (255, 255, 255, a)
        s = pygame.Surface((int(p.size*2), int(p.size*2)), pygame.SRCALPHA)
        pygame.draw.circle(s, col, (int(p.size), int(p.size)), int(p.size))
        screen.blit(s, (p.pos.x - p.size, p.pos.y - p.size - camera_y + WIN_H/2))


def emit_particles(s, particles):
    ang = math.radians(s.heading_deg)
    f = V2(math.cos(ang), math.sin(ang))
    r = V2(-f.y, f.x)
    vF = f.dot(s.vel)
    vR = r.dot(s.vel)
    slip = min(1.0, abs(vR) / 300.0)
    count = int(slip * 30)
    for _ in range(count):
        pos = s.pos - f * 10 + r * frand(-6, 6)
        vel = -r * frand(40, 160) + V2(frand(-20, 20), frand(-20, 20))
        life = frand(0.2, 0.6)
        size = frand(1.5, 3.5)
        particles.append(Particle(pos, vel, life, size))

# ------------------------------ Main ------------------------------

def reset_game(state):
    track, waypoints = state['track'], state['waypoints']
    player = Sled((TRACK_W/2, 80), (50, 120, 255))
    player.max_speed = 900.0

    bots = []
    for i in range(3):
        b = Sled((300 + i*90, 40 - i*30), (255, 140-20*i, 70+40*i), is_ai=True)
        b.nitro = frand(0.2, 0.7)
        b.max_speed = frand(760.0, 860.0)
        b.heading_deg = 90.0
        b.wp_index = i % len(waypoints)
        bots.append(b)

    particles = []
    # reactivate pickups
    for pk in track.pickups:
        pk[1] = True

    state.update(dict(player=player, bots=bots, particles=particles,
                      finished=False, finish_time=0.0, time_elapsed=0.0))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Ice Sprint – Single Level (pygame)")
    clock = pygame.time.Clock()

    ice_tile = make_ice_surface(256, 256)

    track = build_track()
    waypoints = build_waypoints(track)

    state = {'track': track, 'waypoints': waypoints}
    reset_game(state)

    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000.0, 1/30.0)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_r:
                    reset_game(state)

        player: Sled = state['player']
        bots = state['bots']
        particles = state['particles']
        track = state['track']
        waypoints = state['waypoints']
        finished = state['finished']

        if not finished:
            state['time_elapsed'] += dt

        # Input
        keys = pygame.key.get_pressed()
        steer = (1.0 if keys[pygame.K_d] or keys[pygame.K_RIGHT] else 0.0) - \
                (1.0 if keys[pygame.K_a] or keys[pygame.K_LEFT] else 0.0)
        throttle = 1.0 if (keys[pygame.K_w] or keys[pygame.K_UP]) else 0.0
        brake = 1.0 if (keys[pygame.K_s] or keys[pygame.K_DOWN]) else 0.0
        nitro_on = (keys[pygame.K_SPACE] and player.nitro > 0.0)

        if not finished and player.nitro < 1.0:
            player.nitro = min(1.0, player.nitro + dt * 0.05)

        # Update player
        integrate_sled(player, steer, throttle, brake, nitro_on, dt)

        # Collisions: obstacles
        for r in track.obstacles:
            if r.collidepoint(player.pos.x, player.pos.y):
                player.vel *= 0.4
                # Push out minimally along y
                if player.pos.y < r.centery:
                    player.pos.y = r.top - 1
                else:
                    player.pos.y = r.bottom + 1

        # Pickups
        for pos, active in track.pickups:
            if not active:
                continue
            if (player.pos - pos).length_squared() < 26*26:
                player.nitro = min(1.0, player.nitro + 0.35)
                # deactivate
                idx = track.pickups.index([pos, active])
                track.pickups[idx][1] = False

        # AI update
        for b in bots:
            update_ai(b, waypoints, dt)
            t = 1.0
            br = 0.0
            n = (b.nitro > 0.2 and RNG.random() < 0.01)
            integrate_sled(b, b.target_steer, t, br, n, dt)
            # collisions simple
            for r in track.obstacles:
                if r.collidepoint(b.pos.x, b.pos.y):
                    b.vel *= 0.5

        # Finish
        if not finished and player.pos.y >= track.length:
            state['finished'] = True
            state['finish_time'] = state['time_elapsed']

        # Particles
        emit_particles(player, particles)
        for b in bots:
            emit_particles(b, particles)
        for p in particles:
            p.life -= dt
            p.pos += p.vel * dt
        particles[:] = [p for p in particles if p.life > 0.0]

        # Camera (single view): follow player.y
        cam_y = clamp(player.pos.y, WIN_H/2, track.length)

        # Render
        screen.fill((190, 220, 255))
        draw_ice_background(screen, ice_tile, cam_y)
        draw_track(screen, track, cam_y)

        # Bots
        for b in bots:
            draw_sled(screen, b, cam_y)
        # Player with outline
        draw_sled(screen, player, cam_y)
        draw_sled(screen, player, cam_y, outline=True)

        # Particles
        draw_particles(screen, particles, cam_y)

        # HUD
        # Switch to screen coords (we already are)
        time_elapsed = state['time_elapsed']
        hud_lines = [
            f"Time: {time_elapsed:.2f}s",
            f"Distance: {int(player.pos.y)}/{int(track.length)} px",
            f"Nitro: {int(player.nitro*100)}%  (SPACE)",
            ("FINISHED! Time: %.2fs  (R to restart)" % state['finish_time']) if state['finished'] else ""
        ]
        y = 12
        for line in hud_lines:
            if not line:
                continue
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (16, y))
            y += 22

        # Nitro bar
        bar_w, bar_h = 240, 14
        x0, y0 = 16, y + 6
        pygame.draw.rect(screen, (20, 20, 20), (x0-2, y0-2, bar_w+4, bar_h+4), 2)
        fill_w = int(bar_w * player.nitro)
        pygame.draw.rect(screen, (120, 180, 255), (x0, y0, fill_w, bar_h))

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise
