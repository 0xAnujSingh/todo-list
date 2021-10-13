import sqlite3

conn = sqlite3.connect('todolist.db')

c = conn.cursor()

c.execute("""CREATE TABLE item(
	id integer primary key autoincrement not null,
	description varchar(120) not null,
	done boolean default false,
	list_id integer not null,
	created_at timestamp default CURRENT_TIMESTAMP
);""")

c.execute("""CREATE TABLE list(
	id integer primary key autoincrement not null,
	title varchar(120) not null unique,
	description varchar(255) not null,
	created_at timestamp default CURRENT_TIMESTAMP
);""")

conn.commit()


conn.close()