--given a tag field, get:
--user handle
--tweet content
--timestamp
--count

-- get the actual user handle and such
select CONTENT, HANDLE, TIMESTAMP, TWEET_ID, _USER_ID, TAG_COUNT from (
	-- Get the actual tweet content, user_id of the tweeter, timestamp, etc. from the tweets
	select USER_ID as _USER_ID, TWEET_ID, TAG_COUNT, CONTENT, TIMESTAMP from (
		-- get the different tweet ID's
		select TWEET_ID as _TWEET_ID, TAG_COUNT from (
			-- get the tag ID and count
			select TAG_ID as TAGS_TAG_ID, COUNT as TAG_COUNT from TAGS where FIELD=?
		) inner join TAG_TWEET on TAG_TWEET.TAG_ID=TAGS_TAG_ID
	) inner join TWEETS on TWEETS.TWEET_ID=_TWEET_ID
) inner join USERS on USERS.USER_ID=_USER_ID;