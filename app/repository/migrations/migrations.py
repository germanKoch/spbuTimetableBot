def version_1():
    return 'CREATE TABLE subscription(id bigserial, chat_id bigint, state text, division_alias text, ' \
           'level text, program text, year text, program_id text, group_id int)'


def version_2():
    return "INSERT INTO subscription(chat_id, state, division_alias, level, program, year, program_id, group_id)" \
           "VALUES (1000, '1', 'PHYS', 'lev', 'prog', '2021', 'prog_id', 100)"


def version_3():
    return "DELETE FROM subscription WHERE id=1"
