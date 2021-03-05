# Day 7

## Parsing data

Parsing rules is done once, so not a lot of thought was put into it. Input text is processed using a combination of `string.split` and `regex`. Each line is split up into the container bag and its contents. These are then added to a `sqlite` database. The table structure of the database is shown below:

```sql
CREATE TABLE "input_data" (
    "id"	INTEGER,
    "root_color"	TEXT NOT NULL UNIQUE,
    "nbr_1"	INTEGER DEFAULT 0,
    "color_1"	TEXT,
    "nbr_2"	INTEGER DEFAULT 0,
    "color_2"	TEXT,
    "nbr_3"	INTEGER DEFAULT 0,
    "color_3"	TEXT,
    "nbr_4"	INTEGER DEFAULT 0,
    "color_4"	TEXT,
    PRIMARY KEY("id" AUTOINCREMENT)
)
```

# Part 1

A table is create to store the results of part 1

```sql
CREATE TABLE "part1_bags" (
    "id"                INTEGER,
    "container_color"   TEXT UNIQUE,
    "child_color"       TEXT,
    PRIMARY KEY("id" AUTOINCREMENT)
)
```

The algorithm starts by looking up the bags that contain a `shiny gold` bag and insert the results in `part1_bags`

```sql
WITH search_bag AS (SELECT "shiny gold" AS color)
INSERT OR IGNORE INTO part1_bags (container_color, child_color)
SELECT input_data.root_color, search_bag.color
FROM input_data, search_bag
WHERE 
    input_data.color_1 = search_bag.color OR
    input_data.color_2 = search_bag.color OR
    input_data.color_3 = search_bag.color OR
    input_data.color_4 = search_bag.color
```

For my given data, the results were:

| id  | container_color    | child_color |
|-----|--------------------|-------------|
| 1   | light chartreuse   | shiny gold  |
| 2   | striped beige      | shiny gold  |
| 3   | vibrant chartreuse | shiny gold  |
| 4   | dotted lavender    | shiny gold  |

The next step is to figure out which bags contain the ones found in the previous setp. We start with `light chartreuse` and work our way down. Each result is added to the table and a psuedo-recursive search is done by, until we reach the end of the table. The query used for this is:

```sql
WITH search_bag AS 
    (
    SELECT container_color as color FROM part1_bags WHERE id = ? LIMIT 1
    )
INSERT OR IGNORE INTO part1_bags (container_color, child_color)
SELECT input_data.root_color, search_bag.color
FROM input_data, search_bag
WHERE 
    input_data.color_1 = search_bag.color OR
    input_data.color_2 = search_bag.color OR
    input_data.color_3 = search_bag.color OR
    input_data.color_4 = search_bag.color
```

# Part 2

```sql
CREATE TABLE "part2_bags" (
    "id"	INTEGER,
    "root_color"	TEXT,
    "mult_factor"	INTEGER DEFAULT 1,
    "num_children"	INTEGER DEFAULT 0,
    "tot_bags"      INTEGER DEFAULT 0,
    PRIMARY KEY("id" AUTOINCREMENT)
)
```

```sql
SELECT 
    input_data.root_color, 
    input_data.color_1,  
    input_data.color_2, 
    input_data.color_3, 
    input_data.color_4,
    input_data.nbr_1,
    input_data.nbr_2,
    input_data.nbr_3,
    input_data.nbr_4,
    (
        input_data.nbr_1 + input_data.nbr_2 + 
        input_data.nbr_3 + input_data.nbr_4
    ) as nbr_total
FROM input_data
WHERE root_color = "shiny gold"
LIMIT 1
```

```sql
SELECT 
    input_data.root_color, 
    input_data.color_1,  
    input_data.color_2, 
    input_data.color_3, 
    input_data.color_4,
    input_data.nbr_1,
    input_data.nbr_2,
    input_data.nbr_3,
    input_data.nbr_4,
    (
        input_data.nbr_1 + input_data.nbr_2 + 
        input_data.nbr_3 + input_data.nbr_4
    ) as nbr_total
FROM input_data
WHERE root_color = (
    SELECT root_color FROM part2_bags WHERE id = ? LIMIT 1
    )
LIMIT 1
```