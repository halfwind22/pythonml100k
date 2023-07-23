from typing import List
import pandas as pd
import os,time
from logger_etl import logger
from utils import data_columns,item_columns

def read_input_dataframe(file_name:str,delim:str,cols:list)->pd.DataFrame:
    
    """
    Creates an input dataframe based on the file name, and file configs passed
    """
    try:
        current_path  = os.getcwd()
        path = os.path.join(current_path,'ml-100k',file_name)
        data_df = pd.read_csv(filepath_or_buffer = path,\
            sep = delim,header=None, names = cols,encoding='latin1')
        return data_df

    except IOError as e:
        logger.info('Write operation failed with error: ',e)

    finally:
        pass

def write_output_dataframe(output_df:pd.DataFrame,filename:str, format:str,header:bool=True)->None:

    """
    Writes an output dataframe to a file which is of the specified format
    """
    current_path  = os.getcwd()
    path = os.path.join(current_path,'target',filename)

    try:

        if format=='csv':
            output_df.to_csv(path_or_buf=path,index=False,header=header)
        elif format=='parquet':
            output_df.to_parquet(path=path,index=False)

    except Exception as e:
        logger.info('Write operation failed with error: ',e) 
    finally:
        pass

def perform_etl_A()->None:
    """
    Defines the sequence of operations to be performed 
    to get performed required operation as per question A.
    Generates a CSV file containing list of users with no of movies
    they rated and average rating per user.
    """
    
    logger.info("Starting process A")

    try:
        input_df = read_input_dataframe(file_name='u.data',delim='\t',\
                    cols=data_columns)
        
        #Count of movies with avg. rating aggregated over users
        output_df = input_df.groupby(by=['Userid'],sort=False)\
        .agg(func = {'Itemid':'count','Rating':'mean'})

        output_df.rename(columns = {'Itemid':'No of Movies','Rating':'Average Rating'},\
            inplace = True)
    except Exception as e:
        logger.error('ETL operation A failed with error: ',e)

    finally:
        logger.info("Completed process A")

    write_output_dataframe(output_df = output_df.reset_index(),filename='output_A.csv',format='csv',header=False)

def perform_etl_B()->None:
    """
    Defines the sequence of operations to be performed 
    to get performed required operation as per question B.
    Generates a CSV file containing unique genres and no of movies
    under each genres.
    """
    try:
        logger.info("Starting process B")

        input_df = read_input_dataframe(file_name='u.item',delim='|',\
                    cols=item_columns)
        cleaned_df = input_df.drop(columns = \
            ["movie title","release date","video release date","IMDb URL"])

        output_df = cleaned_df.set_index(keys=["movie id"]).sum().to_frame().reset_index()

        output_df.columns=['Genre', 'No of Movies']

        write_output_dataframe(output_df = output_df,filename='output_B.csv',format='csv',header=False)

    except Exception as e:
        logger.error('ETL operation B failed with error: ',e)

    finally:
        logger.info("Completed process B")

def perform_etl_C()->None:
    """
    Defines the sequence of operations to be performed 
    to get performed required operation as per question C.
    Generates a Parquet file that contains the top 100 movies 
    based on their ratings.
    """
    logger.info("Starting process C")

    try:
        input_df1 = read_input_dataframe(file_name='u.data',delim='\t',\
                cols=data_columns)
        
        input_df2 = read_input_dataframe(file_name='u.item',delim='|',\
                    cols=item_columns)

        movie_df = input_df2[['movie id','movie title']]

        movie_rating_df = input_df1.drop(columns = ['Userid','Timestamp']).groupby(by=['Itemid'],sort=False).mean().reset_index()

        merged_df = pd.merge(movie_rating_df,movie_df, how='inner', left_on = 'Itemid', right_on = 'movie id')

        #Sorting on rating
        sorted_df = merged_df.sort_values(by='Rating',ascending=False)

        sorted_top100_df = sorted_df.head(100)

        #Resetting index to 1 to calculate rank
        sorted_top100_df.index = pd.RangeIndex(start=1, stop=101, step=1)
        sorted_top100_ranked_df = sorted_top100_df.reset_index()
        sorted_top100_ranked_df.rename(columns = {'index':'Rank (1-100)'},inplace=True)
        output_df = sorted_top100_ranked_df.reindex(columns=['Rank (1-100)', 'Movie Id', 'Title', 'Average Rating'])

        
        write_output_dataframe(output_df = output_df,filename='output_C.parquet',format='parquet')

    except Exception as e:
        logger.error('ETL operation C failed with error: ',e)

    finally:
        logger.info("Completed process C")

if __name__=="__main__":

    print("Starting the ETL process>>>>>>>>>>>>>>>>>>>>> ")
    start_time = time.time()

    perform_etl_A()
    perform_etl_B()
    perform_etl_C()

    print("Completed all the ETL operations in", time.time()-start_time , "seconds")

    print("Printing contents of output directory >>>>>>>")
    for files in os.walk(os.path.join(os.getcwd(),'target'),topdown=True):
        for file in files:
            print(file)