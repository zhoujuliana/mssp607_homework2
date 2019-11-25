# Import packages
import pandas as pd
import json
import numpy as np

# Import businesses and reviews datafiles
with open('PA_businesses.json', "r") as read_file:
    ratings = json.load(read_file) 
    
with open('PA_reviews_full.json', "r") as read_file:
    reviews = json.load(read_file)  
 
def q1_yelp(data1,data2):
    # Part one
    df = pd.DataFrame(data1['businesses']) #Saving as dataframe 
    stars = df['stars'] #Extracting stars/ratings and saving as pandas series 
    star_percentages = stars.value_counts()/len(stars)*100 #Value counts gives you counts for each star 

    answer1 = pd.DataFrame(star_percentages).sort_index() # Sorting the answers by index
    
    # Part two
    reviews_df = pd.DataFrame(data2['reviews']) # Extract the dataframe and save it to a more digestible form 
    reviews_df['text'] = reviews_df['text'].str.split(' ') # Split reviews by white space to get array of words 
    reviews_df['word_count'] = reviews_df['text'].apply(lambda x: len(x)) # Create new column for wordcount
    #for each row, count how many words (take length)
    answer2 = pd.DataFrame(reviews_df.groupby(['stars']).mean()['word_count'])
    
    return answer1, answer2

answer1a, answer1b = q1_yelp(ratings,reviews)
print(q1_yelp(ratings,reviews))

def q2_yelp(data1):
    #Part 1
    df = pd.DataFrame(data1['businesses'])
    df['categories'] = df['categories'].str.split(',').apply(lambda x: [i.strip().lower() for i in x]) 
    #Split categories by commas to get list of labels, remove white space at the start and end for all values, 
    #standardise so all the strings are in the same case

    s = df.apply(lambda x: pd.Series(x['categories']),axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'label'
    #create a variable to count unique category lables
    #apply pd.Series to each row to turn list of categories into a big data frame,
    #with columns corresponding to each category
    #Stack into one big column of all labels and use set to identify unique 

    df_unstacked = df.drop('categories', axis=1).join(s)
    #remove category label from column and combine with s
  
    answer2a = len(set(df_unstacked['label']))
    
    # Part 2 & 3
    # Create a dataframe that contains by use of zip two columns: label and mean stars with column names etc 
    label_df = pd.DataFrame(list(zip(df_unstacked.groupby('label').mean()['stars'],df_unstacked.groupby('label').count()['business_id'])),columns = ['mean_stars','counts'])
    
    label_df.index = df_unstacked.groupby('label').mean()['stars'].index
    #for some reason index dispappeated
    #relabel index using label names 
    
    answer2b = label_df
    
    return answer2a,answer2b

answer2a, answer2b = q2_yelp(ratings)
print(q2_yelp(ratings))

def q3_yelp(data):
    df = pd.DataFrame(data['businesses'])

    # Create empty dataframe
    dataframe = pd.DataFrame() 
    
    # For each rating, extract attributes and add them to dataframe as a formatted column
    for i in range(len(ratings['businesses'])): 
        dataframe = dataframe.append(pd.DataFrame(ratings['businesses'][i]['attributes'],index=[i]))
        
    # Pull stars data into datafram as well 
    dataframe['stars'] = df[['stars']]
    
    higher_ratings = dataframe[dataframe['stars']>3.5] #take values that are 4 or higher 
    
    # Get summary statistics of attributes to determine counts
    descriptive = higher_ratings.drop(['stars'],axis=1).describe() #get rid of the stars 
    
    # Take names of attributes of which we have more than 500 ratings because some ratings only exists once or twice
    descriptive_keys = (descriptive.loc['count'][descriptive.loc['count']>1000]).keys()
    
    ratings_filtered = higher_ratings[descriptive_keys]
    
    # Print descriptive statistics for each attribute 
    for i in ratings_filtered.columns:
        print(i.upper())
        print(ratings_filtered[i].value_counts() )
        print()

#This command takes a while to run
print(q3_yelp(ratings))

## PART TWO: WIKIPEDIA
# To import this function you will need to install the lxml library using Conda.
from wiki_api import page_text
import re

# Pulling 
wiki_html = page_text("Wikipedia:Featured articles", "html")
wiki_text = page_text("Wikipedia:Featured articles", "text")
wiki_list = page_text("Wikipedia:Featured articles", "list")

# Part 2, Question 1
def get_featured_biographies(list):
    print(f"There are {len(wiki_list)} items in the object wiki_list.")
    final_list = []
    boolean = False
    title = []
    for title in wiki_list:
        if ('[edit]' in title) and ('Autobiographies' in title):
            boolean = False 
            continue 
        elif ('[edit]' in title) and (('biographies' in title) or ('Biographies' in title)):
            boolean = True 
            continue 
        elif ('[edit]' in title) and ('biographies' not in title):
            boolean = False 
            
        if boolean:
            final_list = final_list + [title]
        else:
            continue 
        
    # Clean data: remove blank elements
    while("" in final_list): 
        final_list.remove("") 
        
    # Delete final element off of list, "Cleanup listing for this project is available. 
    # See also the tool's wiki page and the index of WikiProjects."
    del final_list[-1]
    
    print(f"There are {len(final_list)} biographies in the Wikipedia featured articles page.")
    return final_list

final_list = get_featured_biographies(wiki_list)
print(final_list)

def get_first_paragraph(list):
    all_first_p = []
    i = 0
    n = 0
    successes = 0
    fails = 0
    for i in final_list:
        #Extract first paragraph from each element in final_list
        biography = page_text(final_list[i],'html')
        p_start = biography.find("<p>")
        biography = biography[p_start+3:]

        p_break = biography.find("</p>")
        biography = biography[0:p_break]
    
        # Clean raw text: remove HTML tags and breaks in each HTML string of first paragraph extracted
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        clean_bio = re.sub(cleanr, '', biography)
        clean_bio = clean_bio.replace('\\n','')
        clean_bio = clean_bio.replace('\\','')
    
        try:
            all_first_p.append(clean_bio)
            successes += 1
            n+=1
        except:
            fails += 1
            n+=1
            continue

    print(f'There were {successes} successes.')
    print(f'There were {fails} fails.')
   
    return all_first_p

print(get_first_paragraph(final_list))

def get_pronouns(text):
    male_counts = []
    female_counts = []
    neutral_counts = []
    
    male = "(\s+He\s|\s+he\s|\s+him\s|\s+his\s|\s+His\s)"
    female = "(\s+She\s|\s+she\s|\s+her\s\|\s+Her\s\|\s+hers\s)"
    gender_neutral = "(\s+They\s|\s+they\s|\s+them\s|\s+Their\s|\s+their\s)"
    
    for text in df.loc[:, "text"]: #What dataframe?
        male_pattern = re.compile(male)
        female_pattern = re.compile(female)
        neutral_pattern = re.compile(gender_neutral)
        
        male_mentions = re.findall(male_pattern, text)
        female_mentions = re.findall(female_pattern, text)
        neutral_mentions = re.findall(neutral_pattern, text)
        
        #max_pronoun = max(len(male_mentions), len(female_mentions), len(neutral_mentions))
        if female_mentions:
            female_counts.append(len(female_mentions))
        if not female_mentions: 
            female_counts.append(0)
        
        if neutral_mentions: 
            neutral_counts.append(len(neutral_mentions))
        if not neutral_mentions:
            neutral_counts.append(len(neutral_mentions))
        
        if male_mentions: 
            male_counts.append(len(male_mentions))
        if not male_mentions:
            male_counts.append(0)
 
    bio_df['male_pronouns'] = male_counts
    bio_df['female_pronouns'] = female_counts
    bio_df['neutral_pronouns'] = neutral_counts
    
    bio_df['Max'] = bio_df[["male_pronouns","female_pronouns","neutral_pronouns"]].idxmax(axis=1)
    bio_df['Max_Value'] = bio_df[["male_pronouns","female_pronouns","neutral_pronouns"]].max(axis=1)
    
    print(bio_df['Max'].value_counts())
    print(bio_df.loc[bio_df['Max_Value'] == 0])

def additional_analysis():
    pass

def export_dataset(df):
    pass

def get_birth_and_death(infobox):
    pass

if __name__ == "__main__":
    pass