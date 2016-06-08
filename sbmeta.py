# Scraper for Steamie threads on /r/glasgow.

import praw,datetime

r = praw.Reddit('SteamieBMeta')


# Function to return a list of thread IDs. Do this by scraping SteamieBot's submitted threads.

def getThreadIDs():
    numberofthreads = 182 # number of days worth of Steamie threads to go back through.
    IDList = []
    steamie = r.get_redditor('SteamieBot')
    steamiePosts = steamie.get_submitted(limit=numberofthreads)
    for post in steamiePosts:
        if "steamie" in post.url:
            IDList.append(post.id)
        else:
            pass
    return IDList



# Function to get comments from a thread by ID.

def getComments(ThreadID):
    thread = r.get_submission(submission_id=ThreadID)

    threadDate = datetime.datetime.utcfromtimestamp(thread.created_utc) # Get a parsable date...
    print("Working on "+str(threadDate.day)+str(threadDate.month)+str(threadDate.year)) # ...so we know it's actually doing something
    
    thread.replace_more_comments(limit=None, threshold=0) # Reveal all comments in thread
    flat_comments = praw.helpers.flatten_tree(thread.comments)
    return flat_comments


# Function that writes two files; a CSV containing each comment with its date, time, author, score and URL,
# and another which just dumps all the comments to a text file to use in a word cloud (maybe automate this with Python
# at some point rather than just using web services to do it)

def fileWriter(flat_comments):
    with open("steamie.csv", "a") as steamiecsv:
        for comment in flat_comments:
            # CSV STRINGS: ASSEMBLE!
            parsed_date = datetime.datetime.utcfromtimestamp(comment.created_utc)
            datestring = str(parsed_date.day) + "/" + str(parsed_date.month) + "/" + str(parsed_date.year)
            timestring = str(parsed_date.hour) + ":" +str(parsed_date.minute)
            daystring = str(parsed_date.strftime("%A"))
            commentAuthor = str(comment.author)
            commentBody = u''.join((comment.body)).encode('utf-8') # Oh Python, how I love your unicode pickiness.
            commentBodyNaked = commentBody.translate(None, ',"') # Strip out commas and quotes as we don't care about them and they mess with the CSV formatting. No, I'm not proud of that.
            commentScore = str(comment.score)
            commentURL = str(comment.permalink)

            # Write the steamie.csv and steamiecomments.txt to the CWD.
            steamiecsv.write('"'+daystring+'","'+datestring+'","'+timestring+'","'+commentAuthor+'","'+commentScore+'","'+commentBodyNaked+'","'+commentURL+'"\n')
            with open("steamiecomments.txt","a") as steamiecommentsfile:
                      steamiecommentsfile.write(commentBody+" ")

def main():
    threadIDlist = getThreadIDs()
    with open("steamie.csv","a") as steamiecsv:
        steamiecsv.write("Day,Date,Time,Comment Author,Comment Score,Comment Text,Comment Url\n")
    for ID in threadIDlist:
        threadComments = getComments(ID)
        fileWriter(threadComments)

    
        

