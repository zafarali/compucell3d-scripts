## MAY 2015

"""
	GenomeCompare
	allows easy analysis 
"""

from Genome import Genome
import numpy as np
import matplotlib.pyplot as plt

class GenomeCompare:
	def __init__ ( self, genomes = [ None , None ] ):
		assert len( genomes ) > 1 , 'Must provide at least two genomes to initiatile GenomeCompare'
		assert isinstance( genomes[0] , Genome ) and isinstance( genomes[1] , Genome ) , 'genomes must contain Genome objects only'
		self.genomes = genomes		
		
	def diff( self , genome1 , genome2 ):
		"""
			returns the number and loci of genes that
			are unqiue between the two genomes supplied whos id are supplied
			@params
				genome1 / int / index of the first genome to compare
				genome2 / int / index of the second genome to compare
			@return
				object with properties specified
		"""

		g1 = self.genomes[genome1]
		g2 = self.genomes[genome2]

		size = ( g1.size + g2.size ) / 2
		
		g1_mutated = g1.get_mutated_loci()
		g2_mutated = g2.get_mutated_loci()

		different_genes = 0
		different_loci = []

		g1_only = []
		g2_only = []


		# check which loci in 1 are in 2
		for locus in g1_mutated:
			if not (locus in g2_mutated):
				different_genes += 1
				different_loci.append(locus)
				g1_only.append(locus)

		# check which loci in 2 are in 1 but not already counted
		for locus in g2_mutated:
			if not(locus in g1_mutated) and not(locus in different_loci):
				different_genes +=1 
				different_loci.append(locus)
				g2_only.append(locus)
			
		return { 'total_unique_mutations': different_genes , 'loci_different': different_loci , 'unique_to_1' : g1_only , 'unique_to_2' : g2_only }

	def comm( self , genome1 , genome2 ):
		"""
			returns the number and loci common to
			a pair of genomes whos id are supplied
		"""

		g1 = self.genomes[genome1]
		g2 = self.genomes[genome2]


		size = ( g1.size + g2.size ) / 2

		g1_mutated = g1.get_mutated_loci()
		g2_mutated = g2.get_mutated_loci()

		common_mutations = 0
		common_mutation_loci = []

		# check which loci in 1 are in 2
		for locus in g1_mutated:
			if locus in g2_mutated:
				common_mutations += 1
				common_mutation_loci.append(locus)

		# check which loci in 2 are in 1 but not already counted
		for locus in g2_mutated:
			if locus in g1_mutated and not (locus in common_mutation_loci):
				common_mutations += 1 
				common_mutation_loci.append(locus)

		return { 'total_common_mutations': common_mutations , 'loci_common': common_mutation_loci }

	def simillarity_matrix( self ):
		"""
			returns a matrix containing the % of mutations shared
			between any two genomes
		"""

		pass

	def mutation_chart( self, draw = False, order = None ):
		"""
			returns a matrix where the y-indicies
			are genes, and 1 represents mutated
			@params
				draw / boolean / False
					if true: draws a graph representing all the
					mutations per genome

		"""
		size = self.genomes[1].size
		num_genomes = len(self.genomes)
		rep = np.zeros( ( size, num_genomes ) )
		if order is None:
			order = [ x for x in range( num_genomes ) ]

		for genomeid in order:
			genome = self.genomes[genomeid]
			for gene in genome.get_mutated_loci():
				rep[gene][genomeid] = 1

		if draw:
			plt.figure()
			plt.imshow( rep , interpolation = 'nearest' )
			plt.title('Genome Wide Visualization of Mutated Genes')
			plt.xlabel('Genome')
			plt.xticks( range( num_genomes ) , order )
			plt.ylabel('Gene')
			plt.show()
		return rep

	def gene_chart( self , draw = False ):

		return self.mutation_chart(draw=draw)

	def gene_mutations( self ):
		"""
			returns a list indexed by genes
			which represent the % of genomes over which 
			the indexed gene is mutated
		"""
		x = self.mutation_chart()
		return map ( lambda y : y / float( len( self.genomes ) ), map( sum , x ) )

	def genome_mutations ( self ):
		"""
			returns a list indexed by genomes
			which represent the % of genes in the 
			indexed genome which are mutated
		"""

		pass


	@staticmethod
	def from_gen_file ( file_name ):
		"""
			imports a gen_file and returns a GenomeCompare object
		"""

		import csv
		genomes = []
		with open( file_name , 'r' ) as f:
			reader = csv.reader( f ) 
			for row in reader:
				genomes.append( Genome.from_mutated_loci( map( int , row ) ) )
		return GenomeCompare( genomes = genomes )

def newick_order( s ):
	"""
		takes in a newick representaiton of a tree
		and returns the ordering of genomes from the tree.
	"""
		# split ( brackets and then join and then split ) brakets and join. 
		# disregard the ; at the end of the string and then split according to the commas.
		# map the split strings into ints.
	return map( int , ''.join( ''.join( s.split( '(' ) ).split( ')' ) )[0:-1].split( ',' ) )

