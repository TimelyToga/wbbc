CREATE TABLE player_game_stats
(
	stats_entry_id INTEGER PRIMARY KEY,
	player_id int,
	player_name varchar(25),
	team_id int,
	team_name varchar(25),
	game_date varchar(25)
);