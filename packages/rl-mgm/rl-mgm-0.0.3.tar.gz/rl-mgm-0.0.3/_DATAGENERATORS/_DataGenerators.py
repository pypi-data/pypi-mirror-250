# Purpose: Tools to generate data from some distribution. Classes for
#          generating demand data for a given building type, and time 
#          of day are defined. In addition a class for generating PV 
#          energy outputs are defined. Lastly, a stored instances of python objects 
#          for generating demand and PV data are created and stored as variables.
# Author: Gerald, Jones, gjones2@vols.utk.edu
# Creation Date: 2021-06-07
# Last Modified: 2024-01-07
# License: Appache 2.0

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import joblib

import os 

from distfit import distfit

class DemandNodeSimulator:
    """Can be fitted with a data set of demand data tied to a  datetime and location type. The data times are
       decomposed into hours, and each hour has each hour fitted to a distribution for all locations in the given datasets,   
       as well as it's descriptives are stored in a dictionary keyed on hour. By passing a hour and location type, a sample 
       hourly demand for the given hour and location type can be generated. The class takes a dictionary keyed on location 
       types with values of paths to the given locations demand data. The data files are expected to be csv file that have 
       columns of date/time and demand. The data/time values are converted to 24 values and used to fit distributions for 
       each hour and generate the descriptive data. 
    """
    def __init__(self, type_path_dict, seed=None, **kwargs):
        """Generates a demand generator for each of the buildings pointed to by the path dictionary

        Args:
            type_path_dict (dict): key=building type, value=path to csv file with hourly demand data. 
            seed (float, optional): seed to pass to random number generator. Defaults to None.
        """
        self.seed=seed
        self.Demand_Generators = dict()
        self.type_path_dict = type_path_dict
        self.typeList = list(type_path_dict.keys())
        self.hourly_demand_stats = dict()
        self.paths = list(type_path_dict.values())
        self.initialize()
    
    
    def initialize(self, ):
        """generates a demand generator for each of the buildings pointed to by the path dictionary
           These will be demand distributions based on the given building type, and time of day
        """
        for ntype in self.type_path_dict:
            hourly_df_dict, demand_stats, distro_gens = self.generate_demand_generators(self.type_path_dict[ntype])
            self.Demand_Generators[ntype] = distro_gens
            self.hourly_demand_stats[ntype]  = demand_stats 
    
    
    def get_hourly_total(self, hour, node_count_dict=None):
        """Calculates the total hourly demand for all buildings for the given hour. 
           The node count can be used to simulate multiple buildings of the same type.

        Args:
            hour (int): [0,..., 23] hour of the day to get the demand for
            node_count_dict (dict, optional): key=demand node type, value=number of given type. Defaults to None.

        Returns:
            float: total demand for the current hour for the current demand node structure
        """
        ## calculates the total demand for the given hour for all buildings
        demands = 0
        total_max = 0
        
        # if need to generate a dict of node counts for each node type
        if node_count_dict is None:
            node_count_dict={}
            for node in self.Demand_Generators:
                node_count_dict[node]=1
        
        # node represents the type of demand node i.e., hospital, police station, etc.
        for node in self.Demand_Generators:
            # get the data frame for the node type and hour
            hrdf =  self.hourly_demand_stats[node]
            
            # get the min/max values for the hour
            minval = hrdf.loc[hrdf['hour']==hour, 'min'].values[0]
            maxval = hrdf.loc[hrdf['hour']==hour, 'max'].values[0]
            total_max += maxval
            
            # for the number of nodes of this type generate the demand for the hour
            # while ensuring the demand is within the min/max bounds for the data
            for c in range(node_count_dict[node]):
                # ensure demand is inside min/max bounds for data
                demand_sampleHc = np.sum(self.Demand_Generators[node][hour].generate(1, verbose=False)) 
                dem = max(minval, demand_sampleHc)
                dem = min(maxval, dem)
                demands += dem
        
        return demands
            
    
    def adjust_date_col(self, df, datecol="Date/Time", ):
        df[datecol] = [str(s.strip()) for s in df[datecol]]
        dl = list()
        for d in df[datecol]:
            s = d.split("  ")
            t = s[-1]
            f = s[0].strip()
            H = t.split(':')[0]
            d = f +"/22 "+ t

            if int(H) <= 10:
                rep = "0" + str(int(H)-1)
            else:
                rep = str(int(H)-1)
            d = d.replace(H+":", rep + ":")
            dl.append(d)
        return dl

    def generate_hourly_demand_stats(self, df_dict,  hourcol='Electricity:Facility [kW](Hourly)', hours=range(0, 24), Ftype="Hospital"):
        """Generates the descriptive statistics for the given demand data
        
        
        Args:
        
            df_dict (dict): key=hour, value=dataframe for the given hour
            hourcol (str, optional): column name for the demand data. Defaults to 'Electricity:Facility [kW](Hourly)'.
            hours (list, optional): list of hours to generate the stats for. Defaults to range(0, 24).
            Ftype (str, optional): building type. Defaults to "Hospital".
            
            returns:
            
            pd.DataFrame: dataframe with the descriptive statistics for the given demand data for the given hours
            
            """
        results = {
            "hour":[],
            "min":[],
            "max":[],
            "mu":[],
            "std":[],
        }

        # for each hour generate the stats
        for h in hours:
            results['hour'].append(h)

            results['min'].append(df_dict[h][hourcol].min())
            results['max'].append(df_dict[h][hourcol].max())

            results['mu'].append(df_dict[h][hourcol].mean())
            results['std'].append(df_dict[h][hourcol].std())

        return pd.DataFrame(results)

    
    def generate_hourly_df_dict(self, df, hourcol="hour", metriccol='Electricity:Facility [kW](Hourly)', percentile=.96):
        """Generates a dictionary of dataframes for each hour of the day where the energy metric is <= than the given percentile

        Args:
            df (_type_): a dataframe with a column for the hour of the day, and a column for the energy metric
            hourcol (str, optional): column for the hour value. Defaults to "hour".
            metriccol (str, optional): _description_. Defaults to 'Electricity:Facility [kW](Hourly)'.

        Returns:
            dict: key=hour, value=dataframe for the given hour with the energy metric <= the given percentile
        """
        hourly_df_dict = {}
        for f in df[hourcol]:
            hourly_df_dict[f] = df.loc[df[hourcol] == f, :]
            hourly_df_dict[f] = hourly_df_dict[f].loc[hourly_df_dict[f][metriccol] <= hourly_df_dict[f][metriccol].quantile(percentile), :]
        return hourly_df_dict


    def generate_fitted_given_hours_distros(self, H_df_dict, hourcol='Electricity:Facility [kW](Hourly)', hours=range(0, 24), Ftype="Hospital",
                                            verbose=False):
        """Generates a dictionary of distribution generators for each hour of the day for the given demand data, relies on the distfit package
        
        Args:
        
            H_df_dict (dict): key=hour, value=dataframe for the given hour
            hourcol (str, optional): column name for the demand data. Defaults to 'Electricity:Facility [kW](Hourly)'.
            hours (list, optional): list of hours to generate the stats for. Defaults to range(0, 24).
            Ftype (str, optional): building type. Defaults to "Hospital".
            
            returns:
            
            dict: key=hour, value=distribution generator for the given hour"""
        time = 0
        distGens = dict()
        for time in hours:
            distroB = H_df_dict[time][[hourcol]].dropna().values.ravel()
            dFIT = distfit()
            res = dFIT.fit_transform(distroB)
            if verbose:
                _, ax = dFIT.plot()
                ax.set_title(f"Hour: {time}")
            distGens[time] = dFIT
        return distGens

    

    def generate_demand_generators(self, data_path):
        """
            data_path: path to csv file with columns for date/time and kw used that hour for a given building
            Expected columns: Date/Time, Electricity:Facility [kW](Hourly)
        """
        _df = pd.read_csv(data_path)   # load demand data for the building and adjust data/get hours
        # convert date/time column to string and adjust the date/time to be the hours
        _df["Date/Time"] = [str(s).strip() for s in _df["Date/Time"]]
        _df["Date/Time"] = self.adjust_date_col(_df, datecol="Date/Time", )
        _df["Date/Time"] = pd.to_datetime(_df["Date/Time"], format="%m/%d/%y %H:%M:%S") 
        _df["hour"] = _df["Date/Time"].dt.hour

        # store each hours data keyed on the hour (0-23)
        hourly_df_dict = self.generate_hourly_df_dict(_df, hourcol="hour")

        #  Take a look at the stats for each hour
        demand_stats = self.generate_hourly_demand_stats(hourly_df_dict)
        distro_gens = self.generate_fitted_given_hours_distros(hourly_df_dict)


        return hourly_df_dict, demand_stats, distro_gens 


class MonthlyHourlyPVGenerator:
    """Can be fitted with a data set of PV output tied to a  datetime. The data times are 
       decomposed into months and hours, and each month has each hour fitted to a distribution, 
       as well as it's descriptives are stored in a dictionary keyed on month:hour: descriptive. 
       The object takes a path to a csv file with a power columne (powerCol), and datetime column (dateTimecol)
       and this file is stored as a dataframe with added hour/month columns as well as optional
       converted power columns. The data is used to fit the distributions, and generate the descriptive 
       dictionary. The data format is assumed to follow that of the NREL 5 minute PV data. 
    """
    class default_gen:
        def generate(n, **kwargs):
            return 0
    
    def __init__(self, data_path, PVCap=130e6, dateTimeCol="LocalTime", powerCol="Power(MW)", 
                 formatstr=None, convert_power_units=True, units_to_add=["kW"], 
                 **kwargs):
        self.pv_df=pd.read_csv(data_path, low_memory=False)
        self.monthly_df_dict=None
        self.dateTimeCol=dateTimeCol
        self.powerCol=powerCol
        self.PVCap=PVCap
        self.generateDateTime(self.pv_df, self.dateTimeCol, formatstr=formatstr)
        
        if convert_power_units:
            if "kW" in units_to_add:
                self.addkWFromMW(self.pv_df, mwcol=self.powerCol, newkwcol="Power(kW)")
        self.addHourFromDateTime(self.pv_df)
        self.addMonthFromDateTime(self.pv_df)
        self.generate_output_generators()
        
    def generateDateTime(self, df, time_col="LocalTime", newcol="DateTime", formatstr=None):
        df[newcol] = pd.to_datetime(df[time_col], format=formatstr)

    def addHourFromDateTime(self, df, datetimecol="DateTime", newhourcol="Hour"):    
        df[newhourcol] = [v.hour for v in df[datetimecol]]
    
    def addMonthFromDateTime(self, df, datetimecol="DateTime", newmonthcol="Month"):      
        df[newmonthcol] = [v.month for v in df[datetimecol]]

    def addkWFromMW(self, df, mwcol="Power(MW)", newkwcol="Power(kW)"):
        df[newkwcol] = df[mwcol]*1000
        
    ###################################################################################
    ####         Distribution and Stats Generator tools
    def generate_monthly_hourly_stats(self, df, powercol="Power(kW)", monthcol='Month', months=range(1, 13)):
        monthly_stats_dict = dict()
        for month in months:
            monthly_stats_dict[month] = self.generate_hourly_output_stats(df.loc[df[monthcol]==month, :], )
        self.monthly_stats_dict = monthly_stats_dict
    
    def generate_hourly_output_stats(self, df,  powercol="Power(kW)", hourcol='Hour', hours=range(0, 24)):
        results = {
            "hour":[],
            "min":[],
            "max":[],
            "mu":[],
            "std":[],
        }

        for h in hours:
            results['hour'].append(h)

            results['min'].append(df.loc[df[hourcol]==h, powercol].min())
            results['max'].append(df.loc[df[hourcol]==h, powercol].max())

            results['mu'].append(df.loc[df[hourcol]==h, powercol].mean())
            results['std'].append(df.loc[df[hourcol]==h, powercol].std())
 
        return pd.DataFrame(results)

    
    def generate_Monthly_df_dict(self, df, monthcol="Month"):
        monthly_df_dict = {}
        for m in df[monthcol]:
            monthly_df_dict[m] = df.loc[df[monthcol] == m, :]
        
        self.monthly_df_dict = monthly_df_dict
        return monthly_df_dict


    def generate_fitted_distros(self, M_df_dict, powercol="Power(kW)", hourcol='Hour', hours=range(0, 24), months=range(1, 13)):
        time = 0
        distGens = dict()
        for month in months:
            # get the dataframe for the current month from dictionary
            month_df = M_df_dict[month]
            # add distribution geneartor dictionary for each hour for this month
            distGens[month]=dict()
            for time in hours:
                # in the case the value over the hour is all zeros just set it to return 0
                # the default_gen.generate() just returns 0
                if month_df[powercol].max() == 0:
                    distGens[month][time] = self.default_gen(0)
                else:
                    distroB = month_df.loc[month_df[hourcol]==time, powercol].dropna().values.ravel()
                    dFIT = distfit()
                    res = dFIT.fit_transform(distroB)
                    distGens[month][time] = dFIT
        return distGens


    def generate_output_generators(self,):
        # store each hours data keyed on the hour (0-23)
        monthly_df_dict = self.generate_Monthly_df_dict(self.pv_df)
        self.generate_monthly_hourly_stats(self.pv_df, powercol="Power(kW)", monthcol='Month', months=range(1, 13))
        distro_gens = self.generate_fitted_distros(monthly_df_dict)
        self.distro_gens = distro_gens
        return 

    def generateOutput(self, month, hour, resamples=12, **kwargs):
        samples = list()
        mxv = self.pullStatOutput(month, hour, stat="max")
        if mxv == 0:
            return 0
        
        mnv = self.pullStatOutput(month, hour, stat="min")
        val = abs(self.distro_gens[month][hour].generate(n=1, verbose=False)[0])
        val = max(mnv, val)
        val = min(mxv, val)
        
        # for a in range(resamples): # get hours worth of 5 minute samples (60/5)
            # samples.append(abs(self.distro_gens[month][hour].generate(n=1, verbose=False))[0])
        # return np.mean(samples)
        return np.round(val, 3)
    
    def pullAvgOutput(self, month, hour):
        avg = self.monthly_stats_dict[month].loc[self.monthly_stats_dict[month]['hour']==hour, 'mu'].values[0]
        return np.around(avg, 3)
    
    def pullMinOutput(self, month, hour):
        minv = self.monthly_stats_dict[month].loc[self.monthly_stats_dict[month]['hour']==hour, 'min'].values[0]
        return np.around(minv, 3)
    
    def pullMaxOutput(self, month, hour):
        maxv = self.monthly_stats_dict[month].loc[self.monthly_stats_dict[month]['hour']==hour, 'max'].values[0]
        return np.around(maxv, 3)
    
    def pullStatOutput(self, month, hour, stat='mu'):
        v = self.monthly_stats_dict[month].loc[self.monthly_stats_dict[month]['hour']==hour, stat].values[0]
        return np.around(v, 3)

    def getPVoutDD(self, month, hour, weather, **kwargs):
        if weather == 0:
            return self.pullStatOutput(month, hour, stat="max")
        elif weather == 1:
            return self.pullStatOutput(month, hour, stat="mu")
        else:
            return self.pullStatOutput(month, hour, stat="min")


class DemandNodeSimulatorBU:
    def __init__(self, type_path_dict, **kwargs):
        self.Demand_Generators = dict()
        self.type_path_dict = type_path_dict
        self.typeList = list(type_path_dict.keys())
        self.paths = list(type_path_dict.values())
        self.initialize()
    
    
    def initialize(self, ):
        for h in self.type_path_dict:
            hourly_df_dict, demand_stats, distro_gens = self.generate_demand_generators(self.type_path_dict[h])
            self.Demand_Generators[h] = distro_gens
    
    def get_hourly_total(self, hour, node_count_dict=None):
        demands = 0
        if node_count_dict is None:
            node_count_dict={}
            for node in self.Demand_Generators:
                node_count_dict[node]=1
        for node in self.Demand_Generators:
            demands += np.sum(self.Demand_Generators[node][hour].generate(node_count_dict[node], verbose=False))
        return demands
            
    
    def adjust_date_col(self, df, datecol="Date/Time", ):
        df[datecol] = [str(s.strip()) for s in df[datecol]]
        dl = list()
        for d in df[datecol]:
            s = d.split("  ")
            t = s[-1]
            f = s[0].strip()
            H = t.split(':')[0]
            d = f +"/22 "+ t

            if int(H) <= 10:
                rep = "0" + str(int(H)-1)
            else:
                rep = str(int(H)-1)
            d = d.replace(H+":", rep + ":")
            dl.append(d)
        return dl

    def generate_hourly_demand_stats(self, df_dict,  hourcol='Electricity:Facility [kW](Hourly)', hours=range(0, 24), Ftype="Hospital"):
        results = {
            "hour":[],
            "min":[],
            "max":[],
            "mu":[],
            "std":[],
        }

        for h in hours:
            results['hour'].append(h)

            results['min'].append(df_dict[h][hourcol].min())
            results['max'].append(df_dict[h][hourcol].max())

            results['mu'].append(df_dict[h][hourcol].mean())
            results['std'].append(df_dict[h][hourcol].std())

        return pd.DataFrame(results)

    
    def generate_hourly_df_dict(self, df, hourcol="hour"):
        hourly_df_dict = {}
        for f in df[hourcol]:
            hourly_df_dict[f] = df.loc[df[hourcol] == f, :]
        return hourly_df_dict


    def generate_fitted_given_hours_distros(self, H_df_dict, hourcol='Electricity:Facility [kW](Hourly)', hours=range(0, 24), Ftype="Hospital"):
        time = 0
        distGens = dict()
        for time in hours:
            distroB = H_df_dict[time][[hourcol]].dropna().values.ravel()
            dFIT = distfit()
            res = dFIT.fit_transform(distroB)
            # _, ax = dFIT.plot()
            # ax.set_title(f"Hour: {time}")
            distGens[time] = dFIT
        return distGens

    

    def generate_demand_generators(self, data_path):
        _df = pd.read_csv(data_path)
        _df["Date/Time"] = [str(s).strip() for s in _df["Date/Time"]]
        _df["Date/Time"] = self.adjust_date_col(_df, datecol="Date/Time", )
        _df["Date/Time"] = pd.to_datetime(_df["Date/Time"], format="%m/%d/%y %H:%M:%S") 
        _df["hour"] = _df["Date/Time"].dt.hour

        # store each hours data keyed on the hour (0-23)
        hourly_df_dict = self.generate_hourly_df_dict(_df, hourcol="hour")

        #  Take a look at the stats for each hour
        demand_stats = self.generate_hourly_demand_stats(hourly_df_dict)
        distro_gens = self.generate_fitted_given_hours_distros(hourly_df_dict)


        return hourly_df_dict, demand_stats, distro_gens 


# # create generic one to call 
DemSim = joblib.load("../Demand_Generators/generators/5_NodeDemandGenerator2.sav")
DemSim2 = joblib.load("../Demand_Generators/generators/7_NodeDemandGenerator.sav")

# PV130_gen2 = joblib.load("./PV_130MW_generator.sav")
PV130_GEN = joblib.load("../PV_Generators/PV_Gen/PV_130MW_generator.sav")
PV65_GEN = joblib.load("../PV_Generators/PV_Gen/PV_65MW_generator.sav")
PV38_GEN = joblib.load("../PV_Generators/PV_Gen/PV_38MW_generator.sav")
PV27_GEN = joblib.load("../PV_Generators/PV_Gen/PV_27MW_generator.sav")
PV13_GEN = joblib.load("../PV_Generators/PV_Gen/PV_13MW_generator.sav")

# Hospital_path = curdir + "/Resources/data/USA_TN_Knoxville-McGhee.Tyson.AP.723260_TMY3/RefBldgHospitalNew2004_v1.3_7.1_4A_USA_MD_BALTIMORE.csv"
# Police_path = curdir + "/Resources/data/USA_TN_Knoxville-McGhee.Tyson.AP.723260_TMY3/RefBldgLargeOfficeNew2004_v1.3_7.1_4A_USA_MD_BALTIMORE.csv"
sunlight_hours = {
        1:  [7,17],
        2:  [7,17],
        3:  [7,17],
        4:  [6,18],
        5:  [6,19],
        6:  [6,19],
        7:  [6,19],
        8:  [7,19],
        9:  [7,18],
        10: [7,18],
        11: [7,17],
        12: [7,17],
    }
sunlight_hour_monthly_ranges = [
    [[1, 2, 3, 11, 12], [8, 17]],    
    [[4], [6, 18]],    
    [[5, 6, 7], [6, 19]],    
    [[8], [7, 19]],    
    [[9, 10], [7, 18]],    
]
    
def get_sunlight_riseset(month, riseset=0, sunlight_hour_monthly_ranges=sunlight_hour_monthly_ranges):
    for group in sunlight_hour_monthly_ranges:
        months = group[0]
        hours = group[1]
        if month in months:
            return hours[riseset]
# Supermarket_path = curdir + "/Resources/data/USA_TN_Knoxville-McGhee.Tyson.AP.723260_TMY3/RefBldgSuperMarketNew2004_v1.3_7.1_4A_USA_MD_BALTIMORE.csv"
# Shelter_Path = curdir + "/Resources/data/USA_TN_Knoxville-McGhee.Tyson.AP.723260_TMY3/" + "RefBldgLargeHotelNew2004_v1.3_7.1_4A_USA_MD_BALTIMORE.csv"
# GasStation_Path = curdir + "/Resources/data/USA_TN_Knoxville-McGhee.Tyson.AP.723260_TMY3/" + "RefBldgQuickServiceRestaurantNew2004_v1.3_7.1_4A_USA_MD_BALTIMORE.csv"




# label_paths_d = {
#     "Hospital":Hospital_path,
#     "Police Station": Police_path,
#     "Supermarket":Supermarket_path,
#     "Shelter": Shelter_Path,
#     "Gas Station": GasStation_Path,
# }


# DemSim = DemandNodeSimulator(type_path_dict=label_paths_d)
# print(DemSim.get_hourly_total(1))
