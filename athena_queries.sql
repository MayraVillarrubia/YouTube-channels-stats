WITH STATS AS(
    SELECT createdat, channelname,
       subscribers, lag(subscribers, 1) over (order by createdat) as subs_prev,
       totalviews, lag(totalviews, 1) over (order by createdat) as totalviews_prev,
       videocount, lag(videocount, 1) over (order by createdat) as videocount_prev
    FROM "yt_channel_stats"."demo_output_youtube_stats" -- databaseName.bucketNameInputData
    where channelname = 'WhatTheChic' -- channelName
    order by createdat desc
    )
    
SELECT channelname,
        subscribers - subs_prev as diff_subs,
        ((cast(subscribers as decimal(16,5)) / cast(subs_prev as decimal(16,5))) -1 ) *100 as grow_subs,
       totalviews - totalviews_prev as diff_views,
       ((cast(totalviews as decimal(16,5)) / cast(totalviews_prev as decimal(16,5))) -1 ) *100 as grow_views,
       createdat
FROM STATS;
