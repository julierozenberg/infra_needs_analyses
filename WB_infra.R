################################################
# example scripts for the functions in
# the repository 'dataVisSpecialPlots'
################################################

#### libraries ####
library("RColorBrewer")   # nice color palettes
library("grDevices")      # polygon function, some color palettes
library("graphics")       # color ramp & color ramp palettes
library("plotrix")        # used for circles and rectanges in Sobol'

################################################
# example of Sobol' Sensitivity Analysis Radial Convergence
###############################################

# loading function
setwd('SobolSensitivityRadialConvergence')
source('plotRadCon.R')

####


####
# Example 2:
#   Single function call
#   Only plotting values greater than 0.02
#   Controlling output plot name and format (pdf, png)
####
## importing data from sensitivity analysis----
# see Python files for examples of how the input was saved to csv files

# importing first- and total-order indices with their confidence intervals
s1st_opt2 <- read.csv("S1ST_sharepib_ASIA.csv"
                      , sep=','
                      , header=TRUE
                      ,as.is=c(TRUE,rep(FALSE,4)))

# importing second-order indices with their confidence intervals
# both should be a k-by-k matrix with numbers in the upper triangular
# portion and nans elsewhere (k = number of parameters)
s2_opt2 <- read.csv("S2_sharepib_ASIA.csv"
                    , sep=','
                    , header=FALSE)

s2_conf_opt2 <- read.csv("S2_conf_sharepib_ASIA.csv"
                         , sep=','
                         , header=FALSE)

# defining lists of the variables for each group
name_list_opt2 <- list("Imaclim"=c('Growth_drivers', 'Mitigation_challenges', 'Transport_activity', 'Transport_structure', 'Transport_intensity', 'Transport_fuel'),  "Investments module"=c('Modal_shift', 'Road_costs', 'Rail_costs', 'Road_target', 'Rail_target', 'Delay'))
                       
                      

## completing calculations of statistical significance
# and creating plot from single function call
# using all default values when possible

stst_opt2 <- evalPlotIndsRadCon(df=s1st_opt2               # data frame of S1 and ST indices (and confidence intervals if evaluating significance)
                                ,dfs2=s2_opt2              # matrix/data frame of S2 indices
                                ,dfs2Conf=s2_conf_opt2     # matrix/data frame of S2 indices confidence interval
                                ,gpNameList=name_list_opt2 # list of variables names for each group
                                ,s1stmeth='gtr'            # method for significance of S1 and ST
                                ,s1stgtr = 0.00            # threshold for significance of S1 and ST
                                ,s2meth = 'gtr'            # method for significance of S2
                                ,s2gtr = 0.05              # threshold for significance of S2
                                ,ptTitle = ''     # title for plot
                                ,ptFileNm = 'ASIA_sharepib'        # name for file
                                ,ptType = 'PDF'            # type of file
                                ,gpNmMult=1.8
                                ,ptVarNmMult = 1.2   # location of variable name with respect to the plot radius
)






dev.off()