
    SELECT
        p.Id AS [Post_ID],
        p.Title AS [Post_Title],
        p.Body AS [Post_Body],
        p.Tags AS [Post_Tags],
        p.CreationDate AS [Post_Date],
        p.Score AS [Post_Score],
        p.ViewCount AS [Post_View_Count],
        p.AnswerCount AS [Answer_Count],
        p.CommentCount AS [Comment_Count],
        pu.Id AS [Post_User_ID],
        pu.Reputation AS [Post_User_Reputation],
        pu.Location AS [Post_User_Location],
        pu.Views AS [Post_User_Views],
        pu.UpVotes AS [Post_User_Upvotes],
        pu.DownVotes AS [Post_User_Downvotes],
        c.Id AS [Comment_ID],
        c.Text AS [Comment_Text],
        c.Score AS [Comment_Score],
        c.CreationDate AS [Comment_Date],
        cu.Id AS [Comment_User_ID],
        cu.Reputation AS [Comment_User_Reputation],
        cu.Location AS [Comment_User_Location],
        cu.Views AS [Comment_User_Views],
        cu.UpVotes AS [Comment_User_Upvotes],
        cu.DownVotes AS [Comment_User_Downvotes]
    FROM
        Comments c
    JOIN
        Users cu ON c.UserId = cu.Id 
    JOIN
        Posts p ON c.PostId = p.Id
    JOIN
        Users pu ON p.OwnerUserId = pu.Id -- Join to get post user details
    WHERE
        c.CreationDate >= '2024-04-29' AND c.CreationDate < '2024-05-05'
        AND p.CreationDate < '2024-04-29' -- Ensure post creation date is not within the specified range
        AND (p.Tags LIKE '%python%' OR
            p.Tags LIKE '%java%' OR
            p.Tags LIKE '%javascript%' OR
            p.Tags LIKE '%php%' OR
            p.Tags LIKE '%sql%' OR
            p.Tags LIKE '%postgres%' OR
            p.Tags LIKE '%rand%' OR
            p.Tags LIKE '%ruby%' OR
            p.Tags LIKE '%c++%' OR
            p.Tags LIKE '%c#%' OR
            p.Tags LIKE '%html%' OR
            p.Tags LIKE '%css%' OR
            p.Tags LIKE '%r%') -- Filter for programming language tags
    ORDER BY c.CreationDate;
    