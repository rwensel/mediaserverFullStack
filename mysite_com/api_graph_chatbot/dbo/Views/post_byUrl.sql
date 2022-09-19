CREATE VIEW [dbo].[posted_byUrl]
AS
SELECT
 r.guid
,r.author
,r.subreddit
,r.title
,r.url
,r.permalink
,r.full_link
,r.num_comments
,r.over_18
,r.score
,r.date
,r.hash
,s.[post_id]
,s.[id]
,s.[status_code]
,s.[JSON]
,s.[response_time]
,s.[execution_time]
FROM (
	SELECT replace(replace(replace(value, '%', ''), '3A2F2F', '://'), '2F', '/') as 'fb_posturl', *
	FROM fb_post
		CROSS APPLY string_split(post_url, '=')
		WHERE replace(replace(value, '%', ''), '3A2F2F', '://') LIKE '%.[jp][pn]g'
) s

JOIN redd r ON r.[url] = s.fb_posturl
GO