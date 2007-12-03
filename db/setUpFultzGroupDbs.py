#put all the scattering data into a postgresql database
import pgdb
con = sqlite.connect('/home/brandon/fultzGroupScattering.db')
cur = con.cursor()
statement='''create table lrmecs (description varchar(1000), filename varchar(100))'''
cur.execute(statement)

cur.execute('insert into lrmecs (description, filename) values ('1671 R. Osborn            White Beam Vanadium 20-40meV 30HzT0', 'lrcs1671.run')')
