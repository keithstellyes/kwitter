select TWEET_ID, CONTENT, TIMESTAMP from (
    select USER_ID as uUSER_ID from USERS where HANDLE=?
) inner join TWEETS on uUSER_ID=TWEETS.USER_ID;