import pandas as pd
import os
def format_bts(base_dir,fall='22560_NEFSCFallFisheriesIndependentBottomTrawlData', spring='22561_NEFSCSpringFisheriesIndependentBottomTrawlData'):
    """
    PURPOSE: Format BTS data for use in Fish-PACE hackweek. 
             1. Read both spring and fall BTS trawl csvs. 
             2. Merge stations and catch data 
             3. Concatenate spring and fall data togther. 
             4. Retain data that coincides with the PACE time series (ie Spring 2024, Fall 2024, Spring 2025 surveys). 
    REQUIRED INPUT: 
        base_dir (path): Directory with both spring and fall folders 
    OPTIONAL INPUT: 
        fall (str): subdirectory folder name for the fall BTS data folder. Default is 22560_NEFSCFallFisheriesIndependentBottomTrawlData
        spring (str): subdirectory folder name for the spring BTS data folder. Default is 22561_NEFSCSpringFisheriesIndependentBottomTrawlData  
    HISTORY:
        1/26/25: Code created by HS and MKM
        1/27/26: Function initialized by HS
    """
    sta = pd.read_csv(os.path.join(base_dir,fall,'22560_UNION_FSCS_SVSTA.csv'),encoding='latin1')
    catch = pd.read_csv(os.path.join(base_dir,fall,'22560_UNION_FSCS_SVCAT.csv'),encoding='latin1')
    data_fall = pd.merge(sta, catch, on=['CRUISE6','CRUISE','STATUS_CODE','STRATUM','TOW','STATION','ID'], how='outer')
    sta = pd.read_csv(os.path.join(base_dir,spring,'22561_UNION_FSCS_SVSTA.csv'),encoding='latin1')
    catch = pd.read_csv(os.path.join(base_dir,spring,'22561_UNION_FSCS_SVCAT.csv'),encoding='latin1')
    data_spring = pd.merge(sta, catch, on=['CRUISE6','CRUISE','STATUS_CODE','STRATUM','TOW','STATION','ID'], how='outer')
    data = pd.concat([data_spring,data_fall])
    data =data[(data['EST_YEAR']==2024) | (data['EST_YEAR']==2025)]
    return data 
