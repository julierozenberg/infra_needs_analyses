import seaborn as sns
from SALib.analyze import sobol
from SALib.util import read_param_file

from rhodium import *
from rhodium.config import RhodiumConfig
 
# Read the parameter range file and Sobol samples
problem = read_param_file('FishGame/uncertain_params.txt')
param_values = np.loadtxt('FishGame/SobolSamples.txt')
 
# Load the first solution
Y = np.loadtxt('FishGame/SobolReeval/FishGame_Soln' + (soln_index+1) + '.obj')
 
# Evaluate sensitivity to the first objective, NPVharvest
obj_index = 0
Si = sobol.analyze(problem, Y[:,obj_index], calc_second_order=True, conf_level=0.95, print_to_console=False)
pretty_result = get_pretty_result(Si)
 
sns.set()
fig1 = pretty_result.plot()
fig2 = pretty_result.plot_sobol(threshold=0.01,groups={"Prey Growth Parameters" : ["a"],
        "Predator Growth Parameters" : ["b0"]})
 
def get_pretty_result(result):
    pretty_result = SAResult(result["names"] if "names" in result else problem["names"])
 
    if "S1" in result:
        pretty_result["S1"] = {k : float(v) for k, v in zip(problem["names"], result["S1"])}
    if "S1_conf" in result:
        pretty_result["S1_conf"] = {k : float(v) for k, v in zip(problem["names"], result["S1_conf"])}
    if "ST" in result:
        pretty_result["ST"] = {k : float(v) for k, v in zip(problem["names"], result["ST"])}
    if "ST_conf" in result:
        pretty_result["ST_conf"] = {k : float(v) for k, v in zip(problem["names"], result["ST_conf"])}
    if "S2" in result:
        pretty_result["S2"] = _S2_to_dict(result["S2"], problem)
    if "S2_conf" in result:
        pretty_result["S2_conf"] = _S2_to_dict(result["S2_conf"], problem)
    if "delta" in result:
        pretty_result["delta"] = {k : float(v) for k, v in zip(problem["names"], result["delta"])}
    if "delta_conf" in result:
        pretty_result["delta_conf"] = {k : float(v) for k, v in zip(problem["names"], result["delta_conf"])}
    if "vi" in result:
        pretty_result["vi"] = {k : float(v) for k, v in zip(problem["names"], result["vi"])}
    if "vi_std" in result:
        pretty_result["vi_std"] = {k : float(v) for k, v in zip(problem["names"], result["vi_std"])}
    if "dgsm" in result:
        pretty_result["dgsm"] = {k : float(v) for k, v in zip(problem["names"], result["dgsm"])}
    if "dgsm_conf" in result:
        pretty_result["dgsm_conf"] = {k : float(v) for k, v in zip(problem["names"], result["dgsm_conf"])}
    if "mu" in result:
        pretty_result["mu"] = {k : float(v) for k, v in zip(result["names"], result["mu"])}
    if "mu_star" in result:
        pretty_result["mu_star"] = {k : float(v) for k, v in zip(result["names"], result["mu_star"])}
    if "mu_star_conf" in result:
        pretty_result["mu_star_conf"] = {k : float(v) for k, v in zip(result["names"], result["mu_star_conf"])}
    if "sigma" in result:
        pretty_result["sigma"] = {k : float(v) for k, v in zip(result["names"], result["sigma"])}
 
    return pretty_result
 
def _S2_to_dict(matrix, problem):
    result = {}
    names = list(problem["names"])
    for i in range(problem["num_vars"]):
        for j in range(i+1, problem["num_vars"]):
            if names[i] not in result:
                result[names[i]] = {}
            if names[j] not in result:
                result[names[j]] = {}
 
            result[names[i]][names[j]] = result[names[j]][names[i]] = float(matrix[i][j])
 
    return result