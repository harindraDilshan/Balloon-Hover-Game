from Balloon_Hover_Env import *

if __name__ == "__main__":
    env = BalloonHoverEnv(render_mode=True)
    state = env.reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()
                sys.exit()

        # Get user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            action = 0  # decrease fan
        elif keys[pygame.K_UP]:
            action = 2  # increase fan
        else:
            action = 1  # keep fan power

        state, reward, done, _ = env.step(action)
        # print(state, reward, done)
        env.render()

        if done:
            pygame.time.wait(1000)
            state = env.reset()
