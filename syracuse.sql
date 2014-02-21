--DROP TABLE syracuse;
CREATE TABLE syracuse
(
	stats_entry_id INTEGER PRIMARY KEY,
	player_id int,
	team_id int,
	player_name varchar(25),
	team_name varchar(25),
	game_date varchar(25),
	vs_team varchar(25),
	outcome varchar(25),
	min int,
	fgm_fga varchar(7),
	fg_per FLOAT(4),
	threem_threea varchar(7),
	three_per FLOAT(4),
	ftm_fta varchar(7),
	ft_per FLOAT(4),
	rebounds int,
	assists int, 
	blocks int,
	steals int,
	fouls int,
	turnovers int,
	points int
);


INSERT INTO syracuse(	stats_entry_id,
					player_id,
					team_id,
					player_name,
					team_name,
					game_date,
					vs_team,
					outcome,
					min,
					fgm_fga,
					fg_per,
					threem_threea,
					three_per,
					ftm_fta,
					ft_per,
					rebounds,
					assists, 
					blocks,
					steals,
					fouls,
					turnovers,
					points)
SELECT * 
FROM player_game_stats
WHERE team_name LIKE '%Syracuse%'
ORDER BY player_name;

