CREATE TABLE `moods`(
    `id` Integer PRIMARY KEY AUTOINCREMENT,
    `label` TEXT
    )

DROP TABLE JournalEntries

CREATE TABLE `JournalEntries` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`	TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
	`date` TEXT NOT NULL,
    `mood_id` INT NOT NULL,
    FOREIGN KEY (`mood_id`) REFERENCES `moods` (`id`)
);
    

SELECT * FROM JournalEntries

INSERT INTO JournalEntries
VALUES
    ( null, "Apple", "i ate an apple today", "5/5/12", 4, "[1,2]")


INSERT INTO moods
VALUES
    ( null, "ok" )

CREATE TABLE Tags(
    id Integer PRIMARY KEY AUTOINCREMENT,
    label VARCHAR);

SELECT * FROM Tags

CREATE TABLE EntryTags(
    id Integer PRIMARY KEY AUTOINCREMENT,
    entry_id INT,
    tag_id INT,
    FOREIGN KEY (`entry_id`) REFERENCES JournalEntries(`id`),
    FOREIGN KEY (`tag_id`) REFERENCES Tags(`id`)
    );


INSERT INTO Tags
VALUES 
    (null, "Working day")


INSERT INTO EntryTags
VALUES 
    (null, 1 , 2)

SELECT * FROM EntryTags


SELECT * FROM JournalEntries


SELECT id
FROM JournalEntries j
WHERE j.entry LIKE "%asd%"

SELECT *
FROM moods


SELECT
    j.id,
    j.concept,
    j.entry,
    j.date,
    j.mood_id,
    m.label mood_label

FROM JournalEntries j
JOIN moods m
ON m.id = j.mood_id 
            
