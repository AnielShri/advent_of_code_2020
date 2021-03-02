# Day 7.1

## Parsing rules

Parsing rules is done once, so not a lot of thought was put into it. Input text is processed using a combination of `string.split` and `regex`. Each line is split up into the container bag and its contents. These are then added to a `sqlite` database. The table structure of the database is shown below:

```sql
CREATE TABLE "input_data" (
				id	INTEGER,
				root_color	TEXT NOT NULL UNIQUE,
				nbr_1	INTEGER DEFAULT 0,
				color_1	TEXT,
				nbr_2	INTEGER DEFAULT 0,
				color_2	TEXT,
				nbr_3	INTEGER DEFAULT 0,
				color_3	TEXT,
				nbr_4	INTEGER DEFAULT 0,
				color_4	TEXT,
				nbr_bags	INTEGER DEFAULT 0,
				PRIMARY KEY(id AUTOINCREMENT)
			)
```

## Looking up data

```sql
SELECT * FROM input_data 
	WHERE root_color = "shiny gold" 
		OR color_1 = "shiny gold" 
		OR color_2 = "shiny gold" 
		OR color_3 = "shiny gold" 
		OR color_4 = "shiny gold"
```

| id  | root_color         | nbr_1 | color_1      | nbr_2 | color_2          | nbr_3 | color_3     | nbr_4 | color_4      |
|-----|--------------------|-------|--------------|-------|------------------|-------|-------------|-------|--------------|
| 64  | light chartreuse   | 2     | dull silver  | 5     | faded maroon     | 5     | drab purple | 5     | **shiny gold**   |
| 223 | striped beige      | 5     | shiny yellow | 5     | striped magenta  | 1     | **shiny gold**  | 2     | dotted tan   |
| 300 | **shiny gold**         | 1     | plaid orange | 2     | striped lavender | 4     | pale brown  | 5     | wavy blue    |
| 494 | vibrant chartreuse | 1     | dim indigo   | 1     | drab purple      | 2     | **shiny gold**  | 3     | faded salmon |
| 543 | dotted lavender    | 2     | light gold   | 3     | **shiny gold**       | 3     | dim tan     |       |              |	

## Unuptimized query

```sql
SELECT * FROM input_data 
	WHERE root_color = "shiny gold"
		OR color_1 = "shiny gold" 
		OR color_2 = "shiny gold"
		OR color_3 = "shiny gold"
		OR color_4 = "shiny gold"
		OR color_1 = (SELECT root_color FROM input_data WHERE color_1 = "shiny gold" OR color_2 = "shiny gold" OR color_3 = "shiny gold" OR color_4 = "shiny gold") 
		OR color_2 = (SELECT root_color FROM input_data WHERE color_1 = "shiny gold" OR color_2 = "shiny gold" OR color_3 = "shiny gold" OR color_4 = "shiny gold") 
		OR color_3 = (SELECT root_color FROM input_data WHERE color_1 = "shiny gold" OR color_2 = "shiny gold" OR color_3 = "shiny gold" OR color_4 = "shiny gold")  
		OR color_4 = (SELECT root_color FROM input_data WHERE color_1 = "shiny gold" OR color_2 = "shiny gold" OR color_3 = "shiny gold" OR color_4 = "shiny gold") 
```

```sql
WITH const AS (SELECT 'shiny gold' AS name)
INSERT OR IGNORE INTO bag_holder (bag)
SELECT root_color
FROM input_data, const
WHERE 
	input_data.color_1 = const.name OR
	input_data.color_2 = const.name OR
	input_data.color_3 = const.name OR
	input_data.color_4 = const.name
```

```
WITH const AS 
	(
	SELECT container_color FROM recursive_bags WHERE id > 1 LIMIT 1
	)
INSERT OR IGNORE INTO recursive_bags (container_color)
SELECT input_data.root_color
FROM input_data, const
WHERE 
	input_data.color_1 = const.container_color OR
	input_data.color_2 = const.container_color OR
	input_data.color_3 = const.container_color OR
	input_data.color_4 = const.container_color
```

```sql
WITH const AS 
	(
	SELECT container_color FROM recursive_bags WHERE id > 0 LIMIT 1
	)
INSERT OR IGNORE INTO recursive_bags (container_color, child_color)
SELECT input_data.root_color, const.container_color
FROM input_data, const
WHERE
	input_data.color_1 = const.container_color OR
	input_data.color_2 = const.container_color OR
	input_data.color_3 = const.container_color OR
	input_data.color_4 = const.container_color
```

```sql
WITH const AS (SELECT "shiny gold" AS name)
INSERT OR IGNORE INTO recursive_bags (container_color, child_color)
SELECT input_data.root_color, const.name
FROM input_data, const
WHERE 
	input_data.color_1 = const.name OR
	input_data.color_2 = const.name OR
	input_data.color_3 = const.name OR
	input_data.color_4 = const.name
```