-- given a username, get the ID and handles of that user's followees

select HANDLE, USER_ID from (
    select FOLLOWEE_ID from (
        select USER_ID as MY_ID from USERS where HANDLE=?
    ) inner join FOLLOWER_RELATIONS on MY_ID=FOLLOWER_ID
) inner join USERS on USER_ID=FOLLOWEE_ID;