-- Gets a user feed via their handle, but only returning all tweets after timestamp
-- Parameters (username, timestamp)

select HANDLE, CONTENT, TIMESTAMP, FOLLOWEE_ID, TWEET_ID from (
    select FOLLOWEE_ID, CONTENT, TIMESTAMP, TWEET_ID from (
        -- get followee id's
        select FOLLOWEE_ID from (
            -- get user id
            select USER_ID from USERS where HANDLE=?
        ) inner join FOLLOWER_RELATIONS on FOLLOWER_RELATIONS.FOLLOWER_ID=USER_ID
    ) inner join TWEETS on USER_ID=FOLLOWEE_ID where TIMESTAMP > ?
) inner join USERS on USER_ID=FOLLOWEE_ID order by TIMESTAMP desc;