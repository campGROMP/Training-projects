#!/usr/bin/env python
# coding: utf-8

# # First Project - Dataquest.io
# 
# **The project is about:**
# App usage in the 'Google Play store' and the 'App Store'.
# 
# **The project goal is:**
# The goal is to help our developers understand what type of apps are likely to attract more users. The company creates revenue from advertisements in the apps so the focus is on free apps where we can run these ads.

# In[1]:


from csv import reader
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
apple = list(read_file)
apple_header = apple[0]
apple_base = apple[1:]

opened_file_b = open('googleplaystore.csv')
read_file_b = reader(opened_file_b)
google = list(read_file_b)
google_header = google[0]
google_base = google[1:]



# ## Data exploration

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[3]:


apple_expl = explore_data(apple, 0, 5)


# In[4]:


google_expl = explore_data(google,0,5)


# In[5]:


# print the first rows of both data sets to identify the different variables
print(apple[0:1])
print('\n')
print(google[0:1])


# In[6]:


# select what variables are suitable for analysis


# # Data Cleaning

# according to the discussion section of the google play data set, entry 10472 has a missing rating causing the columns to shift, lets check this out;

# In[7]:


print(google[0])
print(google[10473])


# The row is missing the data for the 'category' variable. The easiest solution is to just remove the record all together since we can't fill in the category ourselves with the usual methods such as average, mean etc.

# In[8]:


del google[10473]


# Let us now look into the applestore data.
# 
# In the discussion forum of the Applestore data set, note is made about a extra column in the header row. Lets investigate this further

# In[9]:


print(apple[0:2])


# In[10]:


print(len(apple[0]))
print(len(apple[6]))


# As we can clearly see based on the lengths of the header row and row 7, there is no difference in length. We checked this for several records and no difference was found so we can conclude that this issue, mentioned in the discussion, has already been resolved in the version of the dataset that we are using.

# In[11]:


duplicate_apps_google = []
unique_apps_google = []

for i in google[1:]:
    name = i[0]
    if name in unique_apps_google:
        duplicate_apps_google.append(name)
    else:
        unique_apps_google.append(name)
print('Number of duplicate apps: ', len(duplicate_apps_google))
print('\n')
print('Number of unique apps: ', len(unique_apps_google))


# In[12]:


duplicate_apps_apple = []
unique_apps_apple = []

for j in apple[1:]:
    track = j[1]
    if track in unique_apps_apple:
        duplicate_apps_apple.append(track)
    else:
        unique_apps_apple.append(track)
print('Number of duplicate apps: ', len(duplicate_apps_apple))
print('\n')
print('Number of unique apps: ', len(unique_apps_apple))


# By looking at the result of the previous two code blocks we know that there are a lot of duplicates. When we try to perform analysis, these duplicates will influence our results so we should remove them. We could remove duplicates at random but there are probably some differences in rating, version or other variable. We should think of a criterion for removing the duplicates.

# In[13]:


print(duplicate_apps_google[0:4])


# In[14]:


print(duplicate_apps_apple)


# In[15]:


def print_duplicate(datas,app_name):
    for app in datas:
        name = app[0]
        if name == app_name:
            print(app)
        


# In[16]:


PDF_scan = print_duplicate(google,'Quick PDF Scanner + OCR FREE')


# Above check shows us that there are multiple, exact duplicates, in the google dataset. In order to remove these, we should first determine what criteria to use. In case there is a difference in last_version date or last update, this could show which record is most recent. Best practice would be to only take the most recent version into account

# For the apple dataset we don't have any date's to use so we could look into
# the amount of install to get an idea of what record we should retain and what 
# duplicates to remove

# Below we will remove the duplicates from the 'google' dataset. We will go about his by creating a dictionary. Dictionaries, by definition, can only contain unique keys. In order to be able to hash a list of lists into a dictionary we need to prepare it first. This means taking out the attribute we will use as a key (the app name) and take out the information important, in our case the number of reviews. Because the record with the most reviews will give you the most information (more rating = more accurate)

# In[17]:


reviews_max = {} #create empty dictionary
for app in google[1:]:
    name = app[0] #name of the app
    n_reviews = float(app[3]) #number of reviews in float format
    # first check if name of app is already in our dictionary and if so 
    # check if the number of reviews for the record in the dictionary
    # is greater than the number of ratings from the now read record
    if name in reviews_max and reviews_max[name] < n_reviews: 
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
len(reviews_max)
        
    


# In[18]:


reviews_max


# In[19]:


google_clean = []
already_added = []

for app in google[1:]:
    name = app[0]
    n_reviews = float(app[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        google_clean.append(app)
        already_added.append(name)
        
        


# In[20]:


len(google_clean) #to check if we have the same number of records as previously 


# In[21]:


google_clean[0][0]


# In[22]:


# Mannequin Challenge', 'VR Roller Coaster'
for track in apple[1:]:
    if track[1] == 'Mannequin Challenge':
        print(track)
        print('\n')
    elif track[1] == 'VR Roller Coaster':
        print(track)
        print('\n')


# In[23]:


# apple total rating count = [5]
ratings_max = {} #create empty dictionary
for track in apple[1:]:
    name = track[1] #name of the app
    n_ratings = float(track[5]) #number of ratings in float format
    # first check if name of app is already in our dictionary and if so 
    # check if the number of reviews for the record in the dictionary
    # is greater than the number of ratings from the now read record
    if name in ratings_max and ratings_max[name] < n_ratings: 
        ratings_max[name] = n_ratings
    elif name not in ratings_max:
        ratings_max[name] = n_ratings
        
len(ratings_max)


# In[24]:


apple_clean = []
already_in_apple = []

for track in apple[1:]:
    name = track[1]
    n_ratings = float(track[5])
    if n_ratings == ratings_max[name] and name not in already_in_apple:
        apple_clean.append(track)
        already_in_apple.append(name)
print(' the amount of records in the clean data set: ',len(apple_clean))  
print('\n')
print(apple_clean[0:5])


# We only want to focus on English apps. In order to identify the apps with names not belonging to the english language, we can use the ASCII code. The numbers corresponding to the characters we commonly use in an English text are all in the range 0 to 127, according to the ASCII (American Standard Code for Information Interchange) system. Based on this number range, we can build a function that detects whether a character belongs to the set of common English characters or not.

# In[25]:


def english_check(string):
    count_weird = 0
    for a in string:
        if ord(a) > 127:
            count_weird += 1
            if count_weird > 3:
                return False
    return True
        

Test2 = english_check('爱奇艺PPS -《欢乐颂2》电视剧热播')
Test3 = english_check('Docs To Go™ Free Office Suite')


print(Test2)
print(Test3)



# In[26]:


google_eng = []


for item in google_clean:
    x = english_check(item[0])
    if x == True:
        google_eng.append(item)
        


# In[27]:


google_eng[0]


# In[28]:


print(len(google_eng))


# In[29]:


apple_eng = []
for item in apple_clean:
    x = english_check(item[1])
    if x == True:
        apple_eng.append(item)


# In[30]:


final_apple = []
for i in apple_eng:
    if float(i[4]) == 0:
        final_apple.append(i)
        


# In[31]:


print('The total amount of apps after cleaning:',len(apple_clean))
print('the amount of free apps: ', len(final_apple))


# In[32]:


google_eng[1]


# In[33]:


final_google = []
for i in google_eng:
    if i[6] == 'Free':
        final_google.append(i)


# In[34]:


print('The total amount of apps after cleaning:',len(google_eng))
print('the amount of free apps: ', len(final_google))


# In[35]:


import matplotlib as plt
get_ipython().magic('matplotlib inline')

google_full = len(google)
google_clean = len(google_clean)
google_f = len(final_google)
google_list = [google_full, google_clean, google_f]
x = ('google_full','google_clean','google_f')
y = (2,4,6)
print(google_list)
plt.pyplot.bar(y,google_list,tick_label=x, bottom = 5, align = 'center')
#This graph shows how the total amount of data available changed after 
#the dataset.


# Alright, we have finished most of our data cleaning. As the graph above shows, we still have a sufficient enough dataset altough somewhat reduced. Our goal now is to find the most lucrative apps. We are focusing on only the free to play apps since the business model utilized by the business is based on ad-revenue. So we want to find the type of free apps that are played most. 
# 
# In addition, development for the apple store is more complicated than for the android(google) market. Therefore we want to first see whether an app is profitable in the first six months on the android platform before starting on the apple market.
# 

# Genres could be a good starting point to look into how many apps are developed in that genre and how many people use/downloaded these apps. In addition, we should look to the mean rating associated with the genres to identify which genres are more liked by the user.

# In[36]:


print(google_header)
print(apple_header)


# In[37]:


unique_genre = []
duplicate_genre = []
for i in final_google:
    genre = i[1]
    if genre in unique_genre:
        duplicate_genre.append(genre)
    else:
        unique_genre.append(genre)


# In[38]:


def freq_table(dataset, index):
    freq_dic = {}
    for i in dataset:
        data_point = i[index]
        if data_point in freq_dic:
            freq_dic[data_point] += 1
        else:
            freq_dic[data_point] = 1
    return freq_dic


# In[39]:


# helper function to create a frequency table

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[40]:


google_genres_freq = freq_table(final_google,-4) # genre
apple_prime_genre_freq = freq_table(final_apple, -5) # prime_genre
google_category_freq_table = freq_table(final_google,1) #category


# Based on the result above, we can clearly see that the 'Categories'  of 'Tools' and 'Entertainment' are the most prolific in the google data set.
# 
# When we go through the list of genres, we notice that some genres should be aggregated into 1, such as 'Educational;Education' and 'Educational' and 'Education;Education'

# In[42]:


for genre in apple_prime_genre_freq:
    total = 0
    len_genre = 0
    for app in final_apple:
        genre_app = app[-5]
        if genre_app in genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre +=1
    avg_rating = total // len_genre
    print(genre, ':', avg_rating)


# Above result shows us that 'navigation', 'social networking' and 'reference' app get the most ratings, our proxy for users/installs. If we take this number at face value we should recommend these types for app developement for the apple store. However, if we think a bit deeper about the market for these types of apps we stumble upon some issues. These genres are dominated by a few 'giant' apps. Navigation is probably dominated by a few apps with an enormous user base such as google apps, waze, etc.
# 
# lets check this out.
#         

# In[44]:


for app in final_apple:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5])


# It's clear that the most ratings are coming from Waze and google maps, as predicted. The 3rd place is for Geocoaching with only 3% of the ratings of the waze. 

# Let us do the same for networking:

# In[45]:


for app in final_apple:
    if app[-5] == 'Social Networking':
        print(app[1], ':', app[5])


# In the case of social networking apps, the market is a bit more populated but we see a similar pattern. Facebook and Pinterest dominate the market with  over a million ratings while the others are in the 100K-500K range. A significant difference.

# Our conclusions can therfore not just be based on the amount of ratings/installs per genre. Genres can be dominated ba a few apps therefore making our future app absolete.

# In[53]:


google_cat = {}
for i in google_category_freq_table:
    total = 0
    len_category = 0
    for j in final_google:
        category_app = j[1]
        if i == category_app:
            numb_installs = j[5]
            numb_installs= numb_installs.replace('+','')
            numb_installs = numb_installs.replace(',','')
            total += float(numb_installs)
            len_category += 1 
    avg_numb_installs = total / len_category
    google_cat.update({i:total})              


# In[63]:


tuple = sorted(google_cat.items(),reverse = True, key = lambda x : x[1])
'''
We created a tuple where we sorted above created dictionary based
on the values present in the dictionary. We also added the 'reverse' input
and set it to True, this way the first item has the highest total
'''



# In[64]:


print(tuple)


# In[66]:


for genre in google_genres_freq:
    total = 0
    len_genre = 0
    for app in final_google:
        genre_app = app[-4]
        if genre_app in genre:
            n_installs = float(app[5])
            total += n_installs
            len_genre +=1
    avg_installs = total // len_genre
    print(genre, ':', n_installs) 


# In[69]:


google_gen = {}
for i in google_genres_freq:
    total = 0
    len_category = 0
    for j in final_google:
        genre = j[-4]
        if i == genre:
            numb_installs = j[5]
            numb_installs= numb_installs.replace('+','')
            numb_installs = numb_installs.replace(',','')
            total += float(numb_installs)
            len_category += 1 
    avg_numb_installs = total / len_category
    google_gen.update({i:total})  


# In[70]:


tuple = sorted(google_gen.items(),reverse = True, key = lambda x : x[1])
print(tuple)


# Based on these results, and taking into account what we found for the apple store, we would recommend to develop 
