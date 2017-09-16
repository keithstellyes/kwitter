-- note that all this user's tweets must have been deleted first
delete from USERS where USER_ID="{user_id}";

delete from FOLLOWERS where FOLLOWER_ID="{user_id}";

delete from FOLLOWERS where FOLLOWEE_ID="{user_id}";