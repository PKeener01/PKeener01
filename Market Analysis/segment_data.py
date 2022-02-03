################################################################################
#       Written by Patrick Keener
#   The purpose of this module is to create the ds1 dataset which is panel data
#   for use with analysis
#
################################################################################

# Import functions
import pandas as pd
import numpy as np
import datetime
import sys
import time


def dropDuplicates_SD(listIn, tableName):
    # drops duplicates and returns the unique list and whether there were duplciates
    
    listInCount = len(listIn)
    listOut = list(set(listIn)) # get unique list
    listOutCount = len(listOut)
    noDupes = listInCount == listOutCount

    if noDupes:
        print(f'{listOutCount} variables to be loaded from table: {tableName}')
    else:
        numDupes = listInCount - listOutCount
        print(f'\n\n*********** {numDupes} duplicate Variables in List ***********\n\n')
        print(f'{listOutCount} variables to be loaded from table: {tableName}')

    return listOut


def mergeSf1Tickers(tickersInPath, sf1InPath):
    # Load data into memory and merge tables
    FnNm = sys._getframe().f_code.co_name
    print(f"\n######## {FnNm} function start ########")


    # List of categories (import from 'tickers' folders)
    segCols = ['ticker', 'sector', 'industry', 'scalemarketcap', 
    'currency']

    segCols = dropDuplicates_SD(segCols, 'Tickers')
    
    # List of variables from SF1 to include
    sf1Vars = ['ticker', 'calendardate','datekey', 'shareswa', 'dimension', 'eps'
    , 'equity', 'liabilities', 'netinc', 'rnd', 'assets', 'ebit', 'ebt'
    , 'investments', 'ppnenet', 'revenue', 'ebitda', 'opex', 'price'
    , 'debt', 'gp', 'intexp', 'ncfdiv', 'marketcap', 'ncfo']
    
    sf1Vars = dropDuplicates_SD(sf1Vars, 'Sf1')
    

    # load segment data and drop duplicates (unsure why data is duped)
    print(f"{FnNm}:  Loading tickers data set...")
    segData = pd.read_pickle(tickersInPath)
    segData = segData.filter(segCols)
    print(f"{FnNm}:  Tickers data set loaded")
    segData.drop_duplicates(inplace = True)

    
    sectors = list(segData['sector'].drop_duplicates())
    industries = list(segData['industry'].drop_duplicates())
    del sectors[10] # remove NaN from sectors


    # load SF1 using only columns
    print(f"{FnNm}:  Loading sf1 data set")
    sf1 = pd.read_pickle(sf1InPath)
    sf1 = sf1.filter(sf1Vars)
    print(f"{FnNm}:  sf1 loaded")
    
    # Only include quarterly data 
    print(f"{FnNm}:  Filtering for quarterly data only")
    sf1 = sf1[sf1['dimension'].isin(['ARQ'])]

    # Left-merge segment data in order to filter
    print(f"{FnNm}:  Merging sf1 and tickers data set")
    ds1 = sf1.merge(segData, on = ['ticker'], how = 'left')
    print(f"{FnNm}:  sf1 and tickers Merged")

    # Drop non-USD
    ds1 = ds1[ds1['currency'] == 'USD']
    print(f"{FnNm}:  Removed non-USD currencies")

    del sf1, segData


    return ds1, sectors, industries


def mergeDs1Daily(ds1, dailyInPath):
    # Add stock prices into the DS1 dataset
    FnNm = sys._getframe().f_code.co_name
    print(f"\n######## {FnNm} function start ########")

    # periods from which to test stock return
    periods = [0, 1,5,10,20,30,45,60,75,90,120,150,180,210,240,270,300,330,360]
    
    # get dates to draw prices from
    #allDates = getActiveDates(ds1, periods)

    colsIn = ['ticker', 'date', 'ev','marketcap']
    colsIn = dropDuplicates_SD(colsIn, 'Daily')


    print(f"{FnNm}:  Loading daily data set")
    daily = pd.read_pickle(dailyInPath)
    daily = daily.filter(colsIn)
    print(f"{FnNm}:  daily loaded")

    holiDates = getHoliDates(daily)
    print(f"{FnNm}:  HoliDates calculated")

    
    # Add prices to ds1

    ds1 = getHistoricalPrices(ds1, daily, holiDates, periods)
    print(f"{FnNm}:  Historical prices added to data set")

    return ds1


def segmentSector(fPath, ds1, sectors):
    # Segments data created in loadAndMerge by GICS Sector
    FnNm = sys._getframe().f_code.co_name
    print(f"\n######## {FnNm} function start ########")

    

    for sector in sectors:
        outFile = fPath + "\\sectorData"+ "\\DS1_" + str(sector) + "_GICS_sector_data.pcl"
        ds1[ds1['sector']==sector].to_pickle(outFile)
        print(f"{FnNm}:  {sector} completed")

    return


def segmentIndustry(fPath, sectors, industries):
    # Segments data by GICS Industry
    FnNm = sys._getframe().f_code.co_name
    print(f"\n######## {FnNm} function start ########")

    
    for sector in sectors:
        print(f"\n\n{FnNm}:  #### Now Starting {sector}\n")
        sectorData = fPath + "\\DS1_" + str(sector) + "_GICS_sector_data.pcl"
        
        try:
            secData = pd.read_pickle(sectorData)
            print(f"{FnNm}:  Size: {secData.size}  Sector: {sector}")
            print(secData.size, sector)

        except:
            print(f"{FnNm}:  Error loading {sector} from {sectorData}")
            pass
        

        for industry in industries:
            try:
                indData = secData[secData['industry']==str(industry)]
            except:
                print(f"{FnNm}:  Error in sector: {sector}  industry: {industry}")
                pass

            if indData.size > 0:
                indData.to_pickle(fPath + "\\DS1_" + str(sector) + "_" + str(industry)[:15] + "_industry_data.pcl")
                print(indData.size, sector, industry)
    return None
   

def getHistoricalPrices(ds1, daily, holiDates, periods):
    # Add historical firm value information to the data set

    FnNm = sys._getframe().f_code.co_name
    print(f"\n######## {FnNm} function start ########")

    print(f"{FnNm}:  Subsetting ds1")
    df = ds1[['ticker', 'datekey']].copy()

    print(f"{FnNm}:  Adding price data")
    for period in periods:
        df[period] = df['datekey'] + datetime.timedelta(days=period)
        df['temp'] = df[period].dt.dayofweek
        
        # Convert weekends into next weekday
        df[period] = np.where(df['temp'] == 5, df[period] + datetime.timedelta(days = 2), df[period])
        df[period] = np.where(df['temp'] == 6, df[period] + datetime.timedelta(days = 1), df[period])
        
        # Convert trading holidays to non-trading weekdays
        df['temp'] = df[period].dt.dayofweek
        
        holiDateCount = df[period].isin(holiDates['allDates']).sum()

        # cycle through, converting to next expected trading day until all dates are
        # trading days
        while holiDateCount > 0:
            # Convert trading holidays in next weekday
            df['temp'] = df[period].dt.dayofweek

            # if holiday on Friday, change date to Monday
            df[period] = np.where((df[period].isin(holiDates['allDates']) \
                & (df['temp']==4)), df[period] + datetime.timedelta(days = 3), df[period])
            
            df['temp'] = df[period].dt.dayofweek

            df[period] = np.where((df[period].isin(holiDates['allDates']) \
                & (df['temp']!=4)), df[period] + datetime.timedelta(days = 1), df[period])
            
            holiDateCount = df[period].isin(holiDates['allDates']).sum()

        # Add pricing data to dataframe
        df = df.merge(daily, how = 'left', left_on = [period, 'ticker'],\
            right_on = ['date', 'ticker'], suffixes = (None, f"{period}"))

    print(f"{FnNm}:  Pricing data extracted.  Merging into ds1")

    df.columns = df.columns.astype(str)
    ds1 = ds1.merge(df, how = 'left', left_on = ['ticker', 'datekey'],\
            right_on = ['ticker', 'datekey'])
    
    print(f"{FnNm}:  Pricing data merged in ds1")

    return ds1


def getHoliDates(daily):
    # Create list of holidays
    FnNm = sys._getframe().f_code.co_name
    print(f"\n######## {FnNm} function start ########")

    # Get list of trading dates (with data)
    tradingDates = daily['date'].drop_duplicates()

    # Build list of every date in historical record
    startDate = tradingDates.min()
    endDate = tradingDates.max()
    lastDate = startDate
    allDates = [lastDate]


    print(f"{FnNm}:  Creating full datelist")
    while lastDate != endDate:
        lastDate += datetime.timedelta(days=1)
        allDates.append(lastDate)

    allDates = pd.DataFrame(allDates, columns=['allDates'])

    print(f"{FnNm}:  Removing weekdays and trading days")
    # Remove weekdays
    allDates['temp'] = allDates['allDates'].dt.dayofweek
    allDates = allDates[~allDates['temp'].isin([5,6])].drop('temp', axis = 1)

    # Remove trading days to yield holiDates
    holiDates = allDates[~allDates['allDates'].isin(tradingDates)]

    return holiDates


def getActiveDates(ds1, periods):
    # Get list of dates that the data is active on
    FnNm = sys._getframe().f_code.co_name
    print(f"\n######## {FnNm} function start ########")
    

    activeDates = ds1[['ticker', 'datekey']]

    allDates = list()
    allDates.append(activeDates)
    
    
    for period in periods:
        allDates.append(activeDates + datetime.timedelta(days=period))
    
    # set comprehension to remove duplicates & pull embedded lists out
    allDates = {item for sublist in allDates for item in sublist}

    return allDates


def CreateDataset(fPath, tickersInPath, dailyInPath, sf1InPath):
    # Merges the raw SF1 sharadar dataset with Tickers and Daily
    FnNm = sys._getframe().f_code.co_name
    print(f"\n######## {FnNm} function start ########")

    ds1 = pd.DataFrame()

    # Create ds1 data set
    ds1, sectors, industries = mergeSf1Tickers(tickersInPath, sf1InPath)
    ds1 = mergeDs1Daily(ds1, dailyInPath)
    
    # save as pickle
    ds1.to_pickle(fPath + "\\ds1.pcl")
    print(f"\n{FnNm}:  Saved dataset as pickle")

    # sector segment
    print(f"\n{FnNm}:  Segmenting by sector...")
    segmentSector(fPath, ds1, sectors)

    print(f"{FnNm}:  Data segmented by sector.  Segmenting by industry...")

    # clean up memory
    del ds1
    fPath = fPath + '\\sectorData'

    # industry segment
    segmentIndustry(fPath, sectors, industries)
    print(f"{FnNm}:  Data segmented by industry.")
    
    print(f"{FnNm}:  \n\n##### Dataset Created.  Program run complete")

    return None


fPath = r'C:\tradingData\Sharadar'
tickersInPath = fPath + '\\SHARADAR_TICKERS.pcl'
dailyInPath = fPath + '\\SHARADAR_DAILY.pcl'
sf1InPath = fPath + '\\SHARADAR_SF1.pcl'

start = time.perf_counter()
CreateDataset(fPath, tickersInPath, dailyInPath, sf1InPath)
end = time.perf_counter()
print(f"Ran in {end - start}")

#### Testing


#ds1, sectors, industries = mergeSf1Tickers(tickersInPath, sf1InPath)



# # import pandas as pd

# fPath = r'C:\tradingData\Sharadar'
# tickersInPath = fPath + '\\SHARADAR_TICKERS.csv'
# dailyInPath = fPath + '\\SHARADAR_DAILY.csv'
# sf1InPath = fPath + '\\SHARADAR_SF1.csv'

# calDates = ['lastupdated','firstadded','firstpricedate','lastpricedate',
# 'firstquarter', 'lastquarter']

# df = pd.read_csv(tickersInPath, parse_dates = [calDates])
# df.to_pickle(fPath + "\\SHARADAR_TICKERS.pcl")
# del df
# print('tickers done')

# calDates = ['date', 'lastupdated']
# df = pd.read_csv(dailyInPath, parse_dates = calDates)
# df.to_pickle(fPath + "\\SHARADAR_DAILY.pcl")
# del df
# print('daily done')

# calDates = ['calendardate','datekey','reportperiod','lastupdated']
# df = pd.read_csv(sf1InPath, parse_dates=calDates)
# df.to_pickle(fPath + "\\SHARADAR_SF1.pcl")
# del df
# print('sf1 done')
# print('all done!')