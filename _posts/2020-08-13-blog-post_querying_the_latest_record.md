---
title: "Querying the Latest Record"
date: 2020-08-13
layout: posts
permalink: posts/2020/08/13/querying_the_latest_record
categories: 
  - coding
tags:
  - SQL
  - join
---

In this gist, I show how to get the latest record or a user based on a datetime column.

```sql
SELECT t1.row_id
  ,DATE(t1.start_dt)
  ,DATE(t1.end_dt)
FROM schema.table t1
INNER JOIN (
  SELECT row_id
    ,max(start_dt) AS MaxStartDate
    ,max(end_dt) AS MaxEndDate
  FROM schema.table
  GROUP BY  row_id
  ) t2
  ON t1.row_id = t2.row_id
    AND (t1.end_dt = t2.MaxEndDate OR t1.end_dt IS NULL AND t2.MaxEndDate is NULL)
    AND t1.start_dt = t2.MaxStartDate
```

# References

[https://stackoverflow.com/questions/2411559/how-do-i-query-sql-for-a-latest-record-date-for-each-user/2411763#2411763](https://stackoverflow.com/questions/2411559/how-do-i-query-sql-for-a-latest-record-date-for-each-user/2411763#2411763)