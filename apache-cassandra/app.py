import cassandra.cluster

cluster = cassandra.cluster.Cluster(["localhost"], port=9042)
session = cluster.connect()

session.set_keyspace("mykeyspace")
rows = session.execute("SELECT * FROM users")
for row in rows:
    print(row)

cluster.shutdown()
