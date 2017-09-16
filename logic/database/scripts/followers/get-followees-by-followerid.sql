-- given a user, returns followees with their handle and id
select HANDLE, FOLLOWEE_ID from (
	select FOLLOWEE_ID from FOLLOWERS where FOLLOWER_ID=?
) inner join USERS on FOLLOWEE_ID=USER_ID;