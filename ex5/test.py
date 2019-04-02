import sqlalchemy as db

engine = db.create_engine('sqlite:///data3.db')

conn = engine.connect()

# engine.execute('create table if not exists users (id INTEGER PRIMARY KEY, name text, age INTEGER )')

# engine.execute('insert into users values (?, ?, ?)', (1, 'Gene', 35))
# engine.execute('insert into users values (?, ?, ?)', (2, 'Mike', 5))
# engine.execute('insert into users values (?, ?, ?)', (3, 'Meli', 3))

results = engine.execute('select * from users')

for row in results.fetchall():
    print(row)

conn.close()