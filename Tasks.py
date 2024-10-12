from random import randint, random, choices, sample
import random
import string
def generate_chromosome():
     alphabets = list(string.ascii_uppercase[:13]) 
     random_alphabets = random.sample(alphabets, 10)
     return random_alphabets    

filename = 'Matrix.txt' 
def read_matrix_from_file(filename):
     with open(filename, 'r') as file:
          lines = file.readlines()
     matrix = [list(map(int, line.split(','))) for line in lines]
     return matrix
try:
     matrix = read_matrix_from_file(filename)
except FileNotFoundError:
     print(f"Error: The file '{filename}' was not found.")

chromosome = generate_chromosome()
def fitness(chromosome):
     score = 0
     matrix = read_matrix_from_file(filename)
     for i in range(len(chromosome)):
          if chromosome[i] == 'A':
               score += matrix[0][i]
          elif chromosome[i] == 'B':
               score += matrix[1][i]
          elif chromosome[i] == 'C':
               score += matrix[2][i]
          elif chromosome[i] == 'D':
               score += matrix[3][i] 
          elif chromosome[i] == 'E':
               score += matrix[4][i]               
          elif chromosome[i] == 'F':
               score += matrix[5][i]  
          elif chromosome[i] == 'G':
               score += matrix[6][i]  
          elif chromosome[i] == 'H':
               score += matrix[7][i] 
          elif chromosome[i] == 'I':
               score += matrix[8][i] 
          elif chromosome[i] == 'J':
               score += matrix[9][i] 
          elif chromosome[i] == 'K':
               score += matrix[10][i]  
          elif chromosome[i] == 'L':
               score += matrix[11][i] 
          else:
               score += matrix[12][i] 
     return score

def repair(off,par):
     seen = []  # To keep track of unique items
     newOff = []  #repaired offspring

     for item in off:
          if item not in seen:
               newOff.append(item)
               seen.append(item)
             
     for i in par:
          if i not in newOff:
               newOff.append(i)
     return newOff


def crossover(p1, p2):
     # Choose a random crossover point
     cross_idx = randint(1, 3) 
     # Create offspring
     offspring1 = p1[:cross_idx] + p2[cross_idx:]
     offspring2 = p2[:cross_idx] + p1[cross_idx:]
     
     repairedOff1 = repair(offspring1,p1)
     repairedOff2 = repair(offspring2,p2)
 
     return repairedOff1, repairedOff2

def mutate(chromosome):
     idx1, idx2 = sample(range(len(chromosome)), 2)
     # Swap the values at the selected indexes
     chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
     
def run():
     population_size = 20
     population = [generate_chromosome() for _ in range(population_size)]
     #print(population)
     best, best_eval = population[0], fitness(population[0])
     for gen in range(20):
          scores = [fitness(c) for c in population]
          for i in range(population_size):
               if scores[i] > best_eval:
                    best, best_eval = population[i], scores[i]
                    print(">%d, new best f(%s) = %.3f" % (gen, population[i], scores[i]))
                    selected = selection(population, scores)
                    children = list()
                    # Apply crossover and mutation based on the crossover and mutation rates
                    while len(children) < population_size:
                        # Select random indexes for crossover
                         idx1, idx2 = randint(0, population_size - 1), randint(0, population_size - 1)
                         p1, p2 = selected[idx1], selected[idx2]
                        
                         # Apply crossover with a probability of cross_rate
                         if random.random() < 0.9:
                              for c in crossover(p1, p2):
                              # Apply mutation with a probability of mutate_rate
                                   if random.random() < 0.1:
                                        mutate(c)
                                        children.append(c)
                         else:
                             # If no crossover, check if we want to mutate
                             # then mutate and add or directly add parents to the next generation
                              if random.random() < 0.1:
                                   mutate(p1)
                              if random.random() < 0.1:
                                   mutate(p2)
                                   children.extend([p1, p2])
                         
                              # Ensure children list does not exceed population
                              if len(children) > population_size:
                                   children = children[:population_size]
                 
     population = children
     return best, best_eval  

#Rank Based Selection
def selection(pop, scores):     
     population_size = 20
     scores = []
     population = [generate_chromosome() for _ in range(population_size)]
     best, best_eval = population[0], fitness(population[0])
     for gen in range(100):
          scores = [int(fitness(c)) for c in population]    
     # Sort the population based on fitness scores
     sorted_pop = [x for _, x in sorted(zip(scores, pop))]
     # Rank weights: higher rank has higher weight
     rank_weights = [i + 1 for i in range(population_size)]
     total_rank = sum(rank_weights)  # Total of rank weights
     # Calculate selection probabilities for each individual based on rank
     prob_select = [rank_weight / total_rank for rank_weight in rank_weights]
     # Select and return individuals based on calculated probabilities
     return choices(sorted_pop, weights=prob_select, k=population_size)


print(run())