import streamlit as st
import random
# import matplotlib.pyplot as plt

# Setup (only on first run)
if "n_arms" not in st.session_state:
    st.session_state.n_arms = 5
    st.session_state.true_rates = [random.uniform(0, 1) for _ in range(st.session_state.n_arms)]
    st.session_state.successes = [0] * st.session_state.n_arms
    st.session_state.failures = [0] * st.session_state.n_arms
    st.session_state.rewards = []
    st.session_state.selected_arms = [0] * st.session_state.n_arms
    st.session_state.round = 0
    st.session_state.total_reward = 0

st.title("🎰 Thompson Sampling Simulator")
st.caption("An interactive casino game powered by reinforcement learning")

st.markdown("### 🎰 Slot Machines")

cols = st.columns(st.session_state.n_arms)
for i, col in enumerate(cols):
    col.markdown(f"🎰 **Machine {i}**")
    col.progress(st.session_state.selected_arms[i] / max(1, sum(st.session_state.selected_arms)))



# Show hidden conversion rates (debugging or testing)
if st.checkbox("Show true conversion rates"):
    for i, rate in enumerate(st.session_state.true_rates):
        st.write(f"Arm {i}: {rate:.2f}")

# Button to simulate one round
if st.button("🎯 Pull an Arm"):
    sampled_theta = [
        random.betavariate(st.session_state.successes[i] + 1, st.session_state.failures[i] + 1)
        for i in range(st.session_state.n_arms)
    ]
    arm = sampled_theta.index(max(sampled_theta))

    # Simulate reward
    reward = 1 if random.random() < st.session_state.true_rates[arm] else 0

    # Update
    st.session_state.selected_arms[arm] += 1
    st.session_state.rewards.append(reward)
    if reward == 1:
        st.session_state.successes[arm] += 1
    else:
        st.session_state.failures[arm] += 1
    st.session_state.round += 1

    # st.success(f"Round {st.session_state.round}: Pulled Arm {arm} 🎉 | Reward: {reward}")
    if reward:
        st.success(f"🎉 Round {st.session_state.round}: Hit Machine {arm} and won 🪙 1 coin!")
    else:
        st.warning(f"❌ Round {st.session_state.round}: Machine {arm} gave nothing. Try again!")


# Show reward chart
st.subheader("📈 Total Reward Over Time")
st.line_chart(st.session_state.rewards)
st.subheader("🏆 Scoreboard")
st.metric(label="💰 Total Coins Won", value=sum(st.session_state.rewards))
st.metric(label="🎯 Total Spins", value=st.session_state.round)


# Show arm selection bar chart
st.subheader("📊 Arm Selection Frequency")
st.bar_chart(st.session_state.selected_arms)

# Reset button
if st.button("🔄 Reset"):
    st.session_state.true_rates = [random.uniform(0, 1) for _ in range(st.session_state.n_arms)]
    st.session_state.successes = [0] * st.session_state.n_arms
    st.session_state.failures = [0] * st.session_state.n_arms
    st.session_state.rewards = []
    st.session_state.selected_arms = [0] * st.session_state.n_arms
    st.session_state.round = 0
    st.success("Simulation reset!")
