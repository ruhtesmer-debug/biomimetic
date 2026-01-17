import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title("Biomimetic vs Traditional Cooling Simulation")

# Sliders
initial_temp = st.slider("Initial Room Temp (°C)", 20, 45, 30)
outside_temp = st.slider("Outside Temp (°C)", 10, 35, 25)
airflow = st.slider("Biomimetic Airflow Strength", 0.0, 1.0, 0.2)
ac_target = st.slider("AC Target Temp (°C)", 16, 28, 22)
steps = st.slider("Simulation Steps", 50, 400, 200)

# Simulation function (paste your cooling_simulation here)
def cooling_simulation(initial_temp, outside_temp, airflow, ac_target, steps):
    size = 30
    alpha = 0.1
    dt = 0.1
    bio = np.ones((size, size)) * initial_temp
    ac = np.ones((size, size)) * initial_temp
    avg_bio = []
    avg_ac = []

    for _ in range(steps):
        laplace = (
            np.roll(bio, 1, 0) + np.roll(bio, -1, 0) +
            np.roll(bio, 1, 1) + np.roll(bio, -1, 1) -
            4 * bio
        )
        bio += alpha * laplace * dt
        bio[:, 0] -= airflow * (bio[:, 0] - outside_temp)
        ac += 0.05 * (ac_target - ac)
        avg_bio.append(np.mean(bio))
        avg_ac.append(np.mean(ac))

    return bio, ac, avg_bio, avg_ac

# Run simulation
bio, ac, avg_bio, avg_ac = cooling_simulation(initial_temp, outside_temp, airflow, ac_target, steps)

# Plotting
st.subheader("Heatmaps")
fig, axes = plt.subplots(1, 2, figsize=(10,4))
im1 = axes[0].imshow(bio, cmap='coolwarm', vmin=20, vmax=45)
axes[0].set_title("Biomimetic Cooling")
im2 = axes[1].imshow(ac, cmap='coolwarm', vmin=20, vmax=45)
axes[1].set_title("Traditional AC")
st.pyplot(fig)

st.subheader("Average Temperature Over Time")
fig2, ax2 = plt.subplots(figsize=(8,4))
ax2.plot(avg_bio, label="Biomimetic")
ax2.plot(avg_ac, label="Traditional AC")
ax2.set_xlabel("Time Step")
ax2.set_ylabel("Average Temperature (°C)")
ax2.legend()
st.pyplot(fig2)