#!/usr/bin/env python
# coding: utf-8

# # First Project - Dataquest.io
# 
# **The project is about:**
# App usage in the 'Google Play store' and the 'App Store'.
# 
# **The project goal is:**
# The goal is to help our developers understand what type of apps are likely to attract more users.

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
google_header = [0]
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


apple_eng[0:2]


# In[31]:


final_apple = []
for i in apple_eng:
    if float(i[4]) == 0:
        final_apple.append(i)
        


# In[32]:


print('The total amount of apps after cleaning:',len(apple_clean))
print('the amount of free apps: ', len(final_apple))


# In[33]:


google_eng[1]


# In[34]:


final_google = []
for i in google_eng:
    if i[6] == 'Free':
        final_google.append(i)


# In[35]:


print('The total amount of apps after cleaning:',len(google_eng))
print('the amount of free apps: ', len(final_google))


# In[ ]:




