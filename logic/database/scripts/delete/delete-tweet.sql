-- you must update the count
-- delete tag_tweet entries
delete from TAG_TWEET where TWEET_ID=?;

-- delete tweet row
delete from TWEETS where TWEET_ID=?;