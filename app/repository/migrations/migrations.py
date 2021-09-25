def version_1():
    return 'CREATE TABLE subscription(chat_id bigint primary key , state text, division_alias text, ' \
           'level text, program text, year text, program_id int, group_id int)'


def version_2():
    return 'ALTER TABLE subscription ADD COLUMN is_active bool default true'
