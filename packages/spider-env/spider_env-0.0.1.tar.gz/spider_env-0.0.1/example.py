import spider_env as gym

env = gym.SpiderEnv()

while True:
    done = False
    cumulative_reward = 0.0

    observation, info = env.reset()

    while not done:
        print(f"{observation=}")
        print(f"{info=}")

        # Get a (generated) query.
        action = input("Action: ")  # TODO: Generate based on observation.

        if action == "quit":
            exit()
        if action == "reset":
            break

        # Run the generated query against database.
        observation, reward, terminated, truncated, info = env.step(action)
        print(f"{reward=}\n")

        cumulative_reward += reward
        done = terminated or truncated

    print(f"{cumulative_reward=}\n")
