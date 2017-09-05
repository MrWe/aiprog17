import main
import time
import random
import math

def run():
  lowest_time = math.inf
  longest_time = -math.inf
  best_num = 1
  worst_num = 0
  t0 = time.time()
  main.main([1, 1, 1])
  t1 = time.time()
  lowest_time = t1-t0
  for i in range(2000):
    t0 = time.time()
    rand = [random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100)]
    main.main(rand)
    t1 = time.time()
    t = t1-t0
    if(lowest_time > t):
      lowest_time = t
      best_num = rand
    elif(longest_time < t):
      longest_time = t
      worst_num = rand
  print("lowest time:", lowest_time)
  print("Best number:", best_num)

  print("Longest time:", longest_time)
  print("Worst number:", worst_num)




if __name__ == "__main__":
  run()
