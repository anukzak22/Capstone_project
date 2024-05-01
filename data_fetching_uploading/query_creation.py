import datetime
import sys

def get_week_boundaries(date=None):
    if date is None:
        date = datetime.date.today()
    # Calculate the starting date of the week containing the provided/specified date (Monday)
    start_of_week = date - datetime.timedelta(days=date.weekday())
    # Calculate the ending date of the week containing the provided/specified date (Sunday)
    end_of_week = start_of_week + datetime.timedelta(days=6)
    return start_of_week, end_of_week

def generate_query_1(start_date, end_date):
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    query = f"""
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
        Posts p
    JOIN
        Users pu ON p.OwnerUserId = pu.Id
    LEFT JOIN
        Comments c ON p.Id = c.PostId
    LEFT JOIN
        Users cu ON c.UserId = cu.Id
    WHERE
        p.CreationDate >= '{start_date_str}' AND p.CreationDate < '{end_date_str}'
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
                p.Tags LIKE '%css%') -- Filter for programming language tags
    ORDER BY
        p.CreationDate, c.CreationDate;
    """
    return query


def generate_query_2(start_date, end_date):
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    query = f"""
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
        c.CreationDate >= '{start_date_str}' AND c.CreationDate < '{end_date_str}'
        AND p.CreationDate < '{start_date_str}' -- Ensure post creation date is not within the specified range
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
    """
    return query


if __name__ == "__main__":
    # Check if a specific date is provided as command-line argument
    if len(sys.argv) > 1:
        specific_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    else:
        specific_date = None

    # Get week boundaries
    start_date, end_date = get_week_boundaries(specific_date)

    # Generate query
    query_1 = generate_query_1(start_date, end_date)
    query_2 = generate_query_2(start_date, end_date)

    # Save query to query.sql
    with open("query_post.sql", "w") as file:
        file.write(query_1)

    with open("query_comment.sql", "w") as file:
        file.write(query_2)

    print("Queries saved to files.")
