import random
# import matplotlib.pyplot as plt
import time 

# Simulated environment: true probabilities for 10 slot machines
n_arms = 10
true_conversion_rates = [random.uniform(0, 1) for _ in range(n_arms)]

# Step 1: Setup tracking
N = 10000  # total rounds
successes = [0] * n_arms
failures = [0] * n_arms
rewards = []
selected_arms = [0] * n_arms

# Step 2: Simulation with Thompson Sampling
for n in range(N):
    sampled_theta = [
        random.betavariate(successes[i] + 1, failures[i] + 1)
        for i in range(n_arms)
    ]
    arm = sampled_theta.index(max(sampled_theta))
    selected_arms[arm] += 1

    # Simulate pulling the arm
    reward = 1 if random.random() < true_conversion_rates[arm] else 0
    rewards.append(reward)

    # Update success/failure counts
    if reward == 1:
        successes[arm] += 1
    else:
        failures[arm] += 1

    # ✅ 🎲 Animation (ADD THIS inside the loop)
    print(f"🎰 Round {n+1}: Pulled Arm {arm} | Reward: {reward} | Total Reward: {sum(rewards)}")
    time.sleep(0.1)  # Slows it down for animation

# Step 3: Show results
print(f"True conversion rates: {true_conversion_rates}")
print(f"Arm selections: {selected_arms}")
print(f"Total reward: {sum(rewards)}")

# Step 4: Plot arm selections
plt.bar(range(n_arms), selected_arms, color='purple')
plt.xlabel('Arm')
plt.ylabel('Number of Selections')
plt.title('Thompson Sampling: Arm Selection Frequency')
plt.show()
