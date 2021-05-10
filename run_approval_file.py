import random
import os
import matplotlib.pyplot as plt
import math

# for margin in range(1, 100):
#     probs = [random.randint(1, 100) for _ in range(3)]
#     for _ in range(5):
#         print('python3.8 margin_approval_plot.py '+str(random.randint(1, 1000))+' '+ ' '.join([str(i) for i in probs+[max(probs)+margin]]))
#         # os.system('python margin_approval_plot.py '+str(random.randint(1, 1000))+' '+ ' '.join([str(i) for i in probs+[max(probs)+margin]]))
    
# 80267

# complexity = [102, 95, 87, 73, 68, 50, 46, 38]
# alphas = [1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2]
#
# plt.plot([-math.log10(i) for i in alphas], complexity)
# plt.xlabel("log(1/delta)")
# plt.ylabel("sample complexity")
# plt.title("Variation with delta")
# plt.show()


# slopes = [-0.8110365849096722, -22.709024377470822, -23.24971543407727, -21.3572967359547, -105.16441050995417, -50.824959321006126, -39.74079266057394, -55.15048777385771, -59.20567069840607, -38.11871949075459, -43.525630056819075, -51.365650377612575, -13.787621943464428, -40.281483717180386, -25.682825188806287, -23.79040649068372, -41.09252030209006, -25.95317071710951, -11.084166660432187, -13.24693088685798, -16.491077226496667, -7.29932926418705, -9.191747962309618]
# slopes = [-71.58749589469373, -57.15104468330158, -22.70902437747082, -15.247487796301836, -10.381268286843804]
slopes = [-2.324971543407727, -35.73967884168623, -66.50499996259313, -64.23409752484604, -71.58749589469373, -80.29262190605753, -75.047918656975, -68.82997150600086, -66.77534549089634, -57.15104468330158, -49.689508102132585, -34.766434939794614, -21.627642264257922, -22.49274795482824, -22.70902437747082, -18.65384145292246, -18.383495924619236, -18.383495924619236, -15.463764218944416, -15.247487796301836, -14.38238210573152, -11.300443083074766, -11.084166660432187]

eps = [i/100 for i in range(1, 24)]
# eps = [0.05, 0.1, 0.15, 0.2, 0.24]

plt.plot([1/(i*i) for i in eps], [-i for i in slopes])
plt.xlabel("1/(eps^2)")
plt.ylabel("sample complexity")
plt.title("Variation of slope")
plt.savefig("slope_var.png")
plt.show()
