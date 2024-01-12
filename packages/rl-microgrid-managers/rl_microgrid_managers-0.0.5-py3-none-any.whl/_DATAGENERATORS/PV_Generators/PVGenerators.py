# Purpose: Classes for generating expected PV energy output  data for a month/hour combinations. 
#          The classes are used to generate data based on csv file used to generate fitted distributions 
#          used to generate the samples.
# Author: Gerald, Jones, gjones2@vols.utk.edu
# Creation Date: 2021-06-07
# Last Modified: 2024-01-07
# License: Appache 2.0

from distfit import distfit
import pandas as pd
import numpy as np

# import joblib
# import matplotlib.pyplot as plt

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



