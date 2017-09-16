-- note that all this user's tweets must have been deleted first
delete from USERS where USER_ID="{user_id}";

delete from FOLLOWER_RELATIONS where FOLLOWER_ID="{user_id}";

delete from FOLLOWER_RELATIONS where FOLLOWEE_ID="{user_id}";