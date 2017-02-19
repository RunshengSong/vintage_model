'''
Created on Mar 15, 2016
A caller to calculate the TiO2 vintage release
Year from 1970 to 2020
@author: rsong_admin
'''
import sys
sys.path.append('../packages')

import vintage_model
import numpy as np
import csv
import matplotlib.pylab as plt
from monte_carlo_lifetime import *
from matplotlib import style
style.use('ggplot')

'''
Calculate the average case
'''
def csv_to_dict(csv_file):
    with open(csv_file,'rU') as myfile:
        this_reader = csv.reader(myfile)
        # skip the header row
        next(this_reader, None)
        ''' row[0] is the sector name; row[1] percentage; row[2] average_lifetime; row[3] is the in use release rate '''
        market_dict = {rows[0]:[rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7]] for rows in this_reader}
    return market_dict

def calculate_defult_TiO2():
    '''
    Do a single vintage calculation
    default market share rate = 0.3
    '''
    # read data now
    TiO2_data = np.loadtxt('../data/TiO2_production_real.csv',delimiter=',')
    TiO2_to_paints = 0.3 # what portion of SiO2 are used in coating, paints and pigment market
    TiO2_data[:,1] = TiO2_data[:,1] * TiO2_to_paints
    market_data_dict = csv_to_dict('../data/coating_market_fake.csv')
    '''
    deal with dictionary here
    '''
    # set up the model
    TiO2_market = vintage_model.vintage_market(TiO2_data,market_data_dict, weibull=True)
    test = TiO2_market.calculate_market_vintage()
    
    # save the results to data frame and plot the market figure
    df = TiO2_market.to_dataframe(test)
    df.to_csv('../results/dynamic_results/TiO2_vintage_results_1215.csv')
#     df.to_csv('../results/static_results/TiO2_vintage_results_static_1215.csv')
    TiO2_market.plot_market_vintage()

def get_results_for_one_vintage(year):
    '''
    calculate the results for one vintage year
    '''
    # read data now
    TiO2_data = np.loadtxt('../data/TiO2_production_real.csv',delimiter=',')
    TiO2_to_paints = 0.3 # what portion of SiO2 are used in coating, paints and pigment market
    TiO2_data[:,1] = TiO2_data[:,1] * TiO2_to_paints
    market_data_dict = csv_to_dict('../data/coating_market_fake.csv')
    
    TiO2_market = vintage_model.vintage_market(TiO2_data,market_data_dict, weibull=True)
    
    this_year_vintage = TiO2_market.calculate_for_one_vintage(year=2016)
    
    df = TiO2_market.to_dataframe(this_year_vintage)
    df.to_csv('../results/dynamic_results/year_vintage/TiO2_vintage_2016.csv')

def do_shake_lifetime():
    data = './data/TiO2_production_real.csv'
    market = './data/coating_market_fake.csv'
    TiO2_to_coating = 0.3
    this_shaker = lifetime_shaker(data,market,TiO2_to_coating)
    MT_results = this_shaker.monte_carlo_analysis(round=500)
    average_tot = calculate_defult_TiO2()
    this_shaker.plot_error_bar(MT_results,average_tot)

def do_release_market():
    TiO2_data = np.loadtxt('./data/SiO2_production_real.csv',delimiter=',')
    market_data_dict = csv_to_dict('./data/coating_market_fake.csv')
    TiO2_to_coating = 0.3
    TiO2_data[:,1] = TiO2_data[:,1] * TiO2_to_coating
    TiO2_market = vintage_model.vintage_market(TiO2_data,market_data_dict)
    test = TiO2_market.calculate_market_vintage()
    print TiO2_market.tot_releases_year()
    TiO2_market.plot_market_vintage()

if __name__ == '__main__':
    # test
#     calculate_defult_TiO2()
    get_results_for_one_vintage(2016)