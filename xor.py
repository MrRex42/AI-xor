from __future__ import print_function
import os
import neat
import visualize

xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [0.0, 1.0, 1.0, 0.0]

def eval_genomes(genomes, config):
	for genomes_id, genome in genome:
		genome.fitness = 4.0
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		for xi, xo in zip(xor_inputs, xor_outputs):
			output = net.activate(xi)
			genome.fitness -= (output[0] - xo)**2


def run(config_file):
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	p.add_reporter(neat.Checkpointer(5))

	winner = p.run(eval_genomes, 300)

	print('\nBest genome:\n{!s}'.format(winner))

	print('\nOutput:')
	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

	for xi, xo in zip(xor_inputs, xor_outputs):
		output = winner_net.activate(xi)
		print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

	node_names = {-1:'A', -2:'B', 0:'A XOR B'} 

	visualize.draw_net(config, winner, True, node_names=node_names)
	visualize.plot_stats(stats, ylog=False, view=True)
	visualize.plot_species(stats, view=True)

	p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
	p.run(eval_genomes, 10)


if __name__ == '__main__':

	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'NeatConfigXOR.txt')
	run(config_path)
	
"""
Quand exécution : 
run (générations 1,2,...) puis erreur : "graphviz.backend.ExecutableNotFound: failed to execute ['dot', '-Tsvg', '-O', 'Digraph.gv'], 
make sure the Graphviz executables are on your systems' PATH"
"""
