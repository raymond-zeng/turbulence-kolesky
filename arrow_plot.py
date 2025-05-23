import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def plot_velocity_arrow(points, velocity):
    # Initial time
    time = 0

    # Set up figure and axis
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    # Plot initial arrows and points
    quiver = ax.quiver(points[:, 0], points[:, 2], velocity[time, :, 0], velocity[time, :, 2], color='black', scale=25)
    scatter = ax.scatter(points[:, 0], points[:, 2], color='blue')

    ax.set_title(f"Velocity Arrows at Time {time}")
    ax.set_xlabel("X")
    ax.set_ylabel("Z")

    # Add slider
    ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03])
    slider = Slider(ax_slider, 'Time', 0, 10.054, valinit=time, valstep=0.002)

    # Update function
    def update(val):
        t = int(slider.val)
        quiver.set_UVC(velocity[t, :, 0], velocity[t, :, 2])
        ax.set_title(f"Velocity Arrows at Time {t}")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

def plot_velocity_arrow_3d(points, velocity):
    time = 0

    # Set up figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.2)

    # Plot initial points and arrows
    scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='blue')
    quiver = ax.quiver(points[:, 0], points[:, 1], points[:, 2],
                       velocity[time, :, 0], velocity[time, :, 1], velocity[time, :, 2],
                       length=0.1, normalize=True, color='black')

    ax.set_title(f"Velocity Arrows at Time {time}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Add slider
    ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03])
    slider = Slider(ax_slider, 'Time', 0, velocity.shape[0] - 1, valinit=time, valstep=1)

    def update(val):
        nonlocal quiver
        t = int(slider.val)
        quiver.remove()
        quiver = ax.quiver(points[:, 0], points[:, 1], points[:, 2],
                           velocity[t, :, 0], velocity[t, :, 1], velocity[t, :, 2],
                           length=0.1, normalize=True, color='black')
        ax.set_title(f"Velocity Arrows at Time {t}")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

def reverse_maximin(points):
    n = np.shape(points)[0]
    indices = np.zeros(n, dtype=int)
    lengths = np.zeros(n, dtype=float)
    dists = np.linalg.norm(points - points[0], axis=1)
    indices[-1] = 0
    lengths[0] = np.inf
    for i in range(n - 2, -1, -1):
        k = np.argmax(dists)
        indices[i] = k
        lengths[i] = dists[k]
        dists = np.minimum(dists, np.linalg.norm(points[k] - points, axis=1))
    return indices, lengths

def maximin(points):
    order = reverse_maximin(points)[0]
    return order[::-1]

nx = 10
nz = 10
x_points = np.linspace(0.0, 18 * np.pi / 512, nx, dtype = np.float64)
y_points = np.pi / 2
z_points = np.linspace(0.0, 18 * np.pi / 512, nx, dtype = np.float64)
points = np.array([axis.ravel() for axis in np.meshgrid(x_points, y_points, z_points, indexing = 'ij')], dtype = np.float64).T
with open('10x10iso1024.pickle', 'rb') as f:
    velocity = pickle.load(f)
order = maximin(points)
ordered_points = points[order]
plot_velocity_arrow(ordered_points, velocity)