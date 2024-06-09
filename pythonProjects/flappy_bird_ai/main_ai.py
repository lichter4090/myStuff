import pygame.key

from constants import *
from bird import Bird
from pipe import Pipe

import neat

SCORE = 0
GEN = 0
fps = FPS
AMOUNT_OF_GENS = 10

GOOD = 0.1
VERY_GOOD = 5
BAD = -1

config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    'neat_conf.ini'  # Path to your NEAT configuration file
)

window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))


def find_closest_pipe(bird, pipes):
    closest = None
    dis = float('inf')
    for pipe in pipes:
        distance = pipe.x + PIPE_GAP - bird.x

        if distance < 0:
            continue

        if dis > distance:
            dis = distance
            closest = pipe

    return closest


def draw_window(birds, pipes):
    window.blit(BACKGROUND, (0, 0))

    for bird in birds:
        if bird is not None:
            bird.draw(window)

    for pipe in pipes:
        pipe.draw(window)

    draw_text(window, "gen", (WINDOW_SIZE // 5, TITLE_Y), little_font, black)
    draw_text(window, "birds", (WINDOW_SIZE // 5 * 2, TITLE_Y), little_font, black)
    draw_text(window, "score", (WINDOW_SIZE // 5 * 3, TITLE_Y), little_font, black)
    draw_text(window, "fps", (WINDOW_SIZE // 5 * 4, TITLE_Y), little_font, black)

    draw_text(window, f"{GEN}/{AMOUNT_OF_GENS}", (WINDOW_SIZE // 5, TEXT_Y), little_font, black)
    draw_text(window, f"{len(birds) - birds.count(None)}/{len(birds)}", (WINDOW_SIZE // 5 * 2, TEXT_Y), little_font, black)
    draw_text(window, f"{SCORE}", (WINDOW_SIZE // 5 * 3, TEXT_Y), little_font, black)
    draw_text(window, f"{fps}", (WINDOW_SIZE // 5 * 4, TEXT_Y), little_font, black)

    pygame.display.update()


def eval_genomes(genomes, config_file):
    global SCORE, GEN, fps

    birds = []
    nets = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config_file)
        bird = Bird()
        birds.append(bird)
        nets.append(net)
        ge.append(genome)

    clock = pygame.time.Clock()
    pipes = [Pipe()]

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    fps += 100

                elif event.key == pygame.K_DOWN:
                    fps -= 100

        for i in range(len(genomes)):
            bird = birds[i]

            if bird is None:
                continue

            net = nets[i]

            closest_pipe = find_closest_pipe(bird, pipes)
            inputs = [bird.y, abs(bird.y - closest_pipe.height_of_upper), abs(bird.y - closest_pipe.y), closest_pipe.x - bird.x]

            output = net.activate(inputs)

            if output[0] > 0.5:  # Example condition for jumping
                bird.flap()

            try:
                bird.move_single_frame()

                collision = False

                for pipe in pipes:
                    if pipe.check_collide(bird):
                        collision = True
                        break  # Exit loop if collision detected

                if not collision:
                    ge[i].fitness += GOOD  # Reward survival single frame

                else:
                    birds[i] = None
                    ge[i].fitness += BAD  # punish dying

            except RuntimeError:  # bird hit the floor
                ge[i].fitness += BAD  # punish dying
                birds[i] = None

        new_pipes = []
        # Move and update pipes
        for pipe in pipes:
            try:
                pipe.move_single_frame()
                new_pipes.append(pipe)

            except RuntimeError:
                new_pipes.append(pipe)
                new_pipes.append(Pipe())

                for idx, genome in enumerate(ge):
                    if birds[idx] is not None:
                        genome.fitness += VERY_GOOD  # reward for passing a pipe

                SCORE += 1

            except OSError:
                pass

        pipes = new_pipes.copy()

        if all(item is None for item in birds):  # Check if all birds have failed
            SCORE = 0
            GEN += 1
            break

        draw_window(birds, pipes)


def run_neat(config_file):
    pygame.init()
    pygame.display.set_caption("Flappy Bird ai")

    population = neat.Population(config_file)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, AMOUNT_OF_GENS)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    run_neat(config)
