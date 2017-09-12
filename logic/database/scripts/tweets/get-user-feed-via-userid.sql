-- get the tweet content and timestamp, dropping the ID information
select HANDLE,CONTENT,TIMESTAMP from (
-- get the handles for all those ID's
    select HANDLE, FOLLOWEE_ID from (
-- get the ID's of all followers
        select FOLLOWEE_ID from FOLLOWERS where FOLLOWER_ID=?
    ) inner join USERS on USERS.USER_ID=FOLLOWEE_ID
) inner join TWEETS on FOLLOWEE_ID=TWEETS.USER_ID order by TIMESTAMP desc;