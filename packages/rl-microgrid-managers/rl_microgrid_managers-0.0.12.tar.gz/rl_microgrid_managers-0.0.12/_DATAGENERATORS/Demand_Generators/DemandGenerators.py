# Purpose: Classes for generating demand data for a different building types, and time 
#          of day are defined. The classes are used to generate demand data for the
#          demand nodes in a simulation.
# Author: Gerald, Jones, gjones2@vols.utk.edu
# Creation Date: 2021-06-07
# Last Modified: 2024-01-07
# License: Appache 2.0

from distfit import distfit
import pandas as pd
import numpy as np
# import joblib
# import matplotlib.pyplot as plt


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