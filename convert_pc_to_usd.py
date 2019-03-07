import pandas as pd

GDP_file = 'C:\\Users\\WB451855\\OneDrive - WBG\\!infra_needs_data\\summary_all_data.xlsx'

def load_GDP(GDP_file):
    xl = pd.ExcelFile(GDP_file)

    GDP = xl.parse("GDP")  # read a specific sheet to DataFrame
    GDP2 = GDP.set_index(["wbregionname","year","ssp"]).gdp.unstack("wbregionname")

    GDP2 = GDP2.rename(columns={"Europe and Central Asia":"Eastern Europe and Central Asia","Middle East and North Africa":"Middle-East and North Africa"})

    GDP2["Africa"] = GDP2["Middle-East and North Africa"]+GDP2["Sub-Saharan Africa"]
    GDP2["Asia"] = GDP2["East Asia and Pacific"]+GDP2["South Asia"]
    GDP2["all_countries"] = GDP2["Africa"]+GDP2["Asia"]+GDP2["Latin America and Caribbean"]+GDP2["Eastern Europe and Central Asia"]

    return GDP2

def return_usd(res,region_col_name,data_col_name,ini_index_list,GDP2,d=0.06,ssp='ssp2',wbregions=True):

    #ini_index_list = ["sector","scenario","capital vs maintenance"]
    #region_col_name = "region"
    #data_col_name = "data"

    if wbregions:
        res['wbregion'] = res[region_col_name].copy()
        res.loc[res[region_col_name]=='Africa','wbregion'] = 'Sub-Saharan Africa'
        res.loc[res[region_col_name]=='Asia','wbregion'] = 'East Asia and Pacific'

        res.loc[res[region_col_name]=='Former soviet Union','wbregion'] = 'Eastern Europe and Central Asia'

        disag_afr = res.loc[res[region_col_name]=='Africa'].copy()
        disag_afr.loc[disag_afr[region_col_name]=='Africa','wbregion'] = 'Middle-East and North Africa'

        disag_asia = res.loc[res[region_col_name]=='Asia'].copy()
        disag_asia.loc[disag_asia[region_col_name]=='Asia','wbregion'] = 'South Asia'

        res = res.append(disag_afr).append(disag_asia)                            
    res['ssp'] = ssp
    
    if wbregions:
        col_for_merging = "wbregion"
    else:
        col_for_merging = region_col_name
    
    mydata = res.merge(GDP2.stack().reset_index().rename(columns={"wbregionname":col_for_merging,0:"GDP"}),on=[col_for_merging,"ssp"])
    mydata["cost_bUSD"] = 1e-9*mydata[data_col_name]*mydata.GDP
    mydata["discount_factor"] = (1+d)**(1-(mydata.year.astype(int)-2015))
    mydata["cost_bUSD_disc"] = mydata["cost_bUSD"]*mydata["discount_factor"]
    newdata = mydata.set_index(ini_index_list+[col_for_merging,"year"]).cost_bUSD_disc.sum(level=ini_index_list+[col_for_merging])
    newdata2 = newdata.reset_index()
    newdata2["cost_bUSD_disc_annual"] = newdata2["cost_bUSD_disc"]/15
    
    return newdata2
    
    