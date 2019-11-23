# Import packages
import pandas as pd
import json
import numpy as np

# Import businesses and reviews datafiles
with open('PA_businesses.json', "r") as read_file:
    ratings = json.load(read_file) 
    
with open('PA_reviews_full.json', "r") as read_file:
    reviews = json.load(read_file)  

# Saving as dataframe 
df = pd.DataFrame(ratings['businesses']) 
# print(df.head()) #Check 

def q1_yelp():
    pass

def q2_yelp():
    pass

def q3_yelp():
    pass

# To import this function you will need to install the lxml library using Conda.
from wiki_api import page_text

# Pulling 
if __name__ == '__main__':
    wiki_html = page_text("Wikipedia:Featured articles", "html")
    wiki_text = page_text("Wikipedia:Featured articles", "text")
    wiki_list = page_text("Wikipedia:Featured articles", "list")

    print(wiki_list[0:500])

# Part 2, Question 1
def get_featured_biographies():
    print(f"There are {len(wiki_list)} items in the object wiki_list.")
    final = []
    boolean = False
    title = []
    for title in titles:
        if ('[edit]' in title) and ('Autobiographies' in title):
            boolean = False 
            continue 
        elif ('[edit]' in title) and (('biographies' in title) or ('Biographies' in title)):
            boolean = True 
            continue 
        elif ('[edit]' in title) and ('biographies' not in title):
            boolean = False 
            
        if boolean:
            final = final + [title]
        else:
            continue 
            
    final

    get_featured_biographies()

def get_first_paragraph(page):
    pass

def get_pronouns(text):
    pass

def additional_analysis():
    pass

def export_dataset(df):
    pass

if __name__ == "__main__":
    pass