SET collation_connection = 'utf8_general_ci';
ALTER DATABASE pytt CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE pytt_cell CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE pytt_department CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE pytt_group CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE pytt_subgroup CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE pytt_subject CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE pytt_teacher CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE pytt_parityreference CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
