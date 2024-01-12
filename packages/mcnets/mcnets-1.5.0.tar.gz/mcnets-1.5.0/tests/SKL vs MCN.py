from sklearn.neural_network import MLPRegressor
import main as mc
import numpy as np
from time import perf_counter as pc
import matplotlib.pyplot as plt

mcmodel = mc.MCNeuralNetwork(hiddenCounts=[10])
skmodel = MLPRegressor(hidden_layer_sizes=(10,), max_iter=10000)

X = np.random.rand(200, 3)
Y = X[:, 0]**3 + X[:, 1]**2 + X[:, 2]

# # MCN Optimum Param Tests
# MCN_stScores = []
# MCN_rScores = []
# paramTests = [*range(1, 10)]
# sklt1 = pc()
# skmodel.fit(X, Y)
# sklt2 = pc()
# skl_stScore = skmodel.score(X, Y) / (sklt2 - sklt1)

# for param in paramTests:
#     mcmodel = mc.MCRegressor()
#     mcnt1 = pc()
#     mcmodel.fit(X, Y, Ieta=param, Beta=10, Gamma=4, Verbose=1)
#     mcnt2 = pc()
#     MCN_rScores.append(mcmodel.score(X, Y))
#     MCN_stScores.append(mcmodel.score(X, Y) / (mcnt2 - mcnt1)**0.5)

# plt.plot(paramTests, MCN_stScores)
# plt.plot(paramTests, MCN_rScores)
# plt.plot([paramTests[0], paramTests[-1]], [skl_stScore]*2)
# plt.legend(["MCN ST Scores", "MCN R^2 Scores", "SKL ST Score"])
# plt.title("MCN Cost & R^2 Scores vs SKL Cost (Higher is Better)")
# plt.grid(True)
# plt.show()

# Training (MCN vs SKL, single run)
t1 = pc()
mcmodel.fit(X, Y, Ieta=9, Beta=10, Gamma=2)
t2 = pc()
skmodel.fit(X, Y)
t3 = pc()

print(f"MCNets Score: {mcmodel.score(X, Y)} | MCNets Time: {t2-t1}s")
print(f"SKLearn Score: {skmodel.score(X, Y)} | Sklearn Time: {t3-t2}s")

print(f"\nMCN ST Score: {mcmodel.score(X, Y) / (t2-t1)}")
print(f"SKL ST Score: {skmodel.score(X, Y) / (t3-t2)}")