import mcnets as mc
import multiprocessing
import numpy as np
from time import perf_counter as pc

def trainModel(X, model, power):
    Y0 = X[:, 0]**power
    model.fit(X, Y0)
    print(model.score(X, Y0))
    # return model, power

if __name__ == "__main__":
    # Args
    X = np.random.rand(150, 2)
    model = mc.MCNeuralNetwork()

    # Normal fashion
    t1 = pc()
    trainModel(X, model, 2)
    trainModel(X, model, 2)
    trainModel(X, model, 2)
    t2 = pc()
    print(f"Normal Time Taken: {t2-t1}\n")

    # Multiprocessing way
    t3 = pc()
    pool = multiprocessing.Pool(processes=3)
    print(pool.starmap(trainModel, iterable=[(X, model, 2), (X, model, 3), (X, model, 4)]))
    t4 = pc()
    print(f"Multiprocessing Time Taken: {t4-t3}")

    # Results
    print("\nComparison:")
    print(f"MP Speed Reduction (s): {(t2-t1)-(t4-t3)}")
    print(f"Relative Time Taken  %: {(t4-t3)/(t2-t1)}")

