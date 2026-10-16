
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider

# ==========================================
# MARS ROVER MISSION ANALYTICS DASHBOARD
# ==========================================

from main import run_simulation

path, obstacles = run_simulation()
grid_size = 5

# Animation settings
interval = 700
paused = False
current_step = 0

total_steps = len(path) - 1
unique_positions = len(set(path))

# Calculate cumulative distance
distances = [0]

for i in range(1, len(path)):
    x1, y1 = path[i - 1]
    x2, y2 = path[i]

    distance = abs(x2 - x1) + abs(y2 - y1)
    distances.append(distances[-1] + distance)

# Validate example path
assert all(
    0 <= x < grid_size and 0 <= y < grid_size
    for x, y in path
), "Path contains an out-of-bound position!"

assert not any(
    position in obstacles for position in path
), "Path crosses an obstacle!"

# ==========================================
# CREATE FIGURE
# ==========================================

fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(
    left=0.08,
    right=0.70,
    bottom=0.24,
    top=0.90
)

ax.set_title("Mars Rover Mission Control", fontsize=16)
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")

ax.set_xlim(-0.5, grid_size - 0.5)
ax.set_ylim(-0.5, grid_size - 0.5)

ax.set_xticks(range(grid_size))
ax.set_yticks(range(grid_size))
ax.grid(True, linestyle="--", alpha=0.5)
ax.set_aspect("equal")

# ==========================================
# OBSTACLES
# ==========================================

for index, (ox, oy) in enumerate(sorted(obstacles)):
    ax.scatter(
        ox, oy,
        color="red",
        marker="s",
        s=300,
        label="Obstacle" if index == 0 else None,
        zorder=3
    )

    ax.text(
        ox, oy, "X",
        color="white",
        ha="center",
        va="center",
        fontweight="bold",
        zorder=4
    )

# ==========================================
# START AND DESTINATION
# ==========================================

ax.scatter(
    *path[0],
    color="green",
    s=180,
    label="Start",
    zorder=4
)

ax.scatter(
    *path[-1],
    color="orange",
    marker="D",
    s=100,
    label="Destination",
    zorder=4
)

# ==========================================
# ROVER AND TRAIL
# ==========================================

trail, = ax.plot(
    [], [],
    "b-o",
    linewidth=2,
    markersize=6,
    label="Rover Trail",
    zorder=5
)

rover, = ax.plot(
    [], [],
    "o",
    color="deepskyblue",
    markeredgecolor="black",
    markersize=18,
    label="Rover",
    zorder=6
)

ax.legend(loc="upper right")

# ==========================================
# ANALYTICS DASHBOARD
# ==========================================

dashboard = fig.text(
    0.73,
    0.78,
    "",
    fontsize=11,
    va="top",
    family="monospace",
    bbox=dict(
        boxstyle="round,pad=0.8",
        facecolor="#eef4ff",
        edgecolor="#4060a0"
    )
)

progress_ax = fig.add_axes(
    [0.73, 0.30, 0.23, 0.035]
)

progress_ax.set_xlim(0, 100)
progress_ax.set_ylim(0, 1)
progress_ax.set_yticks([])
progress_ax.set_xticks([0, 25, 50, 75, 100])
progress_ax.set_title("Mission Progress", fontsize=11)

progress_bar = progress_ax.barh(
    0.5, 0,
    height=0.7,
    color="seagreen"
)[0]

# ==========================================
# UPDATE ANIMATION
# ==========================================

def update(frame):
    global current_step

    current_step = frame

    visited = path[:frame + 1]

    xs = [point[0] for point in visited]
    ys = [point[1] for point in visited]

    trail.set_data(xs, ys)
    rover.set_data([xs[-1]], [ys[-1]])

    progress = (
        frame / total_steps * 100
        if total_steps > 0 else 100
    )

    dashboard.set_text(
        "MISSION ANALYTICS\n"
        "-----------------------\n"
        f"Step: {frame}/{total_steps}\n"
        f"Position: {visited[-1]}\n"
        f"Distance: {distances[frame]}\n"
        f"Unique Visited: {len(set(visited))}\n"
        f"Total Obstacles: {len(obstacles)}\n"
        f"Progress: {progress:.0f}%\n"
        "-----------------------\n"
        f"Status: {'COMPLETED' if frame == total_steps else 'RUNNING'}"
    )

    progress_bar.set_width(progress)

    return trail, rover, dashboard, progress_bar


# ==========================================
# RELIABLE ANIMATION CONTROLS
# ==========================================

def toggle_pause(event):
    global paused

    if paused:
        animation.event_source.start()
        paused = False
        play_button.label.set_text("Pause")
    else:
        animation.event_source.stop()
        paused = True
        play_button.label.set_text("Play")

    fig.canvas.draw_idle()


def restart(event):
    global paused

    # Stop the current timer
    animation.event_source.stop()

    # Reset animation to the first frame
    animation.frame_seq = animation.new_frame_seq()
    update(0)

    # Apply current speed and resume
    animation.event_source.interval = int(speed_slider.val)
    animation.event_source.start()

    paused = False
    play_button.label.set_text("Pause")

    fig.canvas.draw_idle()



def change_speed(value):
    delay = int(value)

    # Apply the new animation interval
    animation.event_source.interval = delay
    animation.event_source.stop()
    animation.event_source.start()

    # Show the selected speed in the console
    print(f"Speed changed: {delay} ms")

    fig.canvas.draw_idle()



# ==========================================
# CREATE CONTROL WIDGETS
# ==========================================

play_ax = fig.add_axes([0.12, 0.09, 0.14, 0.06])
restart_ax = fig.add_axes([0.30, 0.09, 0.14, 0.06])
speed_ax = fig.add_axes([0.58, 0.09, 0.30, 0.05])

play_button = Button(play_ax, "Pause")
restart_button = Button(restart_ax, "Restart")

speed_slider = Slider(
    speed_ax,
    "Speed (ms)",
    valmin=100,
    valmax=1500,
    valinit=interval,
    valstep=100
)

# Keep references to widgets and register callbacks
play_button.on_clicked(toggle_pause)
restart_button.on_clicked(restart)
speed_slider.on_changed(change_speed)

# ==========================================
# START ANIMATION
# ==========================================

animation = FuncAnimation(
    fig,
    update,
    frames=len(path),
    interval=interval,
    repeat=True,
    blit=False,
    cache_frame_data=False
)

update(0)

plt.show()
