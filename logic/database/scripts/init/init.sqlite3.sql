--TWEETS table
create table TWEETS(USER_ID integer,
                   TWEET_ID integer,
                   CONTENT varchar(150),
                   TIMESTAMP integer);

--User table
create table USERS(USER_ID integer,
                   HANDLE varchar(50));

--All tags and their UUID's
create table TAGS(TAG_ID integer,
                  FIELD integer,
                  COUNT integer);

--tag <-> tweet intersection table
create table TAG_TWEET(TAG_ID integer,
                       TWEET_ID integer);

--Followers table
create table FOLLOWER_RELATIONS(FOLLOWER_ID integer,
                       FOLLOWEE_ID integer);