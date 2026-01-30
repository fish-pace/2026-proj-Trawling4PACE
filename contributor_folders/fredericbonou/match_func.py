var='var'
def match_nearest(df, ds, var, new_name=var, date=None):
    """
    PURPOSE: 
        Loop through each row of a dataframe and find the nearest neighbor matchup from a xarray dataset
    INPUTS:
        df (pandas dataframe): dataframe (base coordinates to match to)
        ds (xarray dataset): xarray dataset to extract data from
        var (str): variable name that you are matching (ex. chla or avw or Rrs_665)
        new_name (str): Optional. variable name to add to original dataframe (ex chla_PACE). Default is original variable name
        date (): Optional. Dates from the dataframe. NOTE the dtype of dataframe date and dtype of xarray date must be the same! 
    RETURNS:
        df (pandas dataframe): original dataframe updated with a new column (new_name)
    HISTORY:
        2024: originally written (adapted from turtle track code)
        8/5/25: updated for PACE HACKWEEK
    """  
    try:
        df = df.rename(columns={'lat':'latitude','lon':'longitude'})
        ds = ds
    except:
        pass
    try:
        d = []
        for i in range(0, len(df)):
            # Crop the dataset to include data that corresponds to track locations
            cropped_ds = ds[var].sel(time=df.date[i],
                                           latitude=df.latitude[i],
                                           longitude=df.longitude[i],
                                           method='nearest'
                                           )
            d.append(cropped_ds.values)
        df.insert(0,new_name,d)
        return df
    except:
        d = []
        for i in range(0, len(df)):
            # Crop the dataset to include data that corresponds to track locations
            cropped_ds = ds[var].sel(latitude=df.latitude[i],
                                           longitude=df.longitude[i],
                                           method='nearest'
                                           )
            d.append(cropped_ds.values)
        df.insert(0,new_name,d)
        return df
