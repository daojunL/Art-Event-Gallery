CREATE TABLE Art_Events(
	Eid CHAR(20),
	title CHAR(40),
	PRIMARY KEY (Eid));

CREATE TABLE Artist(
	Aid CHAR(20),
	artist_name CHAR(20),
	info CHAR(50),
	PRIMARY KEY (Aid));

CREATE TABLE Perform(
	Eid CHAR(20),
	Aid CHAR(20),
	PRIMARY KEY (Eid, Aid),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid),
	FOREIGN KEY (Aid) REFERENCES Artist(Aid));

CREATE TABLE Address(
	Lid CHAR(20),
	city CHAR(20),
	street CHAR(20),
	venue CHAR(20),
	zipcode CHAR(20),
	PRIMARY KEY (Lid));

CREATE TABLE held(
	Eid CHAR(20),
	Lid CHAR(20),
	PRIMARY KEY (Eid, Lid),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid),
	FOREIGN KEY (Lid) REFERENCES Location(Lid));

CREATE TABLE Ticket_has(
	Tid CHAR(20),
	Eid CHAR(20),
	price INTEGER,
	amount INTEGER,
	refund_policy CHAR(20),
	PRIMARY KEY Tid,
	UNIQUE(Eid),
	FOREIGN KEY (Eid) REFERENCES  Art_Events(Eid));

CREATE TABLE Time(
	time_serial CHAR(20),
	Tmonth INTEGER,
	Tday INTEGER,
	Tyear INTEGER,
	PRIMARY KEY (time_serial));

CREATE TABLE T_on(
	Eid CHAR(20),
	time_serial CHAR(20),
	PRIMARY KEY (Eid, time_serial),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid),
	FOREIGN KEY (time_serial) REFERENCES Time(time_serial),
	CHECK (COUNT(DISTINCT Eid) = (SELECT COUNT(DISTINCT Eid) FROM Art_Events))
	CHECK (COUNT(DISTINCT time_serial) = (SELECT COUNT(DISTINCT time_serial) FROM Time))
);

CREATE TABLE Concert(
	Eid CHAR(20),
	concert_type CHAR(20),
	PRIMARY KEY (Eid),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid) ON DELETE CASCADE);

CREATE TABLE Theater(
	Eid CHAR(20),
	genre CHAR(20),
	PRIMARY KEY (Eid),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid) ON DELETE CASCADE);

CREATE TABLE Exhibition(
	Eid CHAR(20),
	background CHAR(20),
	PRIMARY KEY (Eid),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid) ON DELETE CASCADE);



insert into Art_Events(Eid, title) values ('0001', 'BTS_concert');
insert into Art_Events(Eid, title) values ('0002', 'Tayler_concert');
insert into Art_Events(Eid, title) values ('0003', 'Finding_Neverand');
insert into Art_Events(Eid, title) values ('0004', 'Shear_Madness');
insert into Art_Events(Eid, title) values ('0005', 'Sum_GIRL');

INSERT into Artist(Aid, artist_name, info) VALUES ('I0001', 'Bangtan_Boys', 'seven-member_Korean_band');
INSERT into Artist(Aid, artist_name, info) VALUES ('S0001', 'Tayler_swify', 'American singer-songwriter');
INSERT into Artist(Aid, artist_name, info) VALUES ('T0001', 'Joe', 'Actor');
INSERT into Artist(Aid, artist_name, info) VALUES ('T0002', 'Lily', 'Actress');
INSERT into Artist(Aid, artist_name, info) VALUES ('T0003', 'John', 'Actor');

INSERT into Concert(Eid, concert_type) VALUES ('0001', 'Kpop');
INSERT into Concert(Eid, concert_type) VALUES ('0002', 'Country');

INSERT into Exhibition(Eid, background) VALUES ('0005', 'Crushes_12*12');

INSERT into Address(Lid, city, street, venue, zipcode) VALUES ('MA001', 'Worcester', 'Park_Ave', 'Lin_Hall', '01608');
INSERT into Address(Lid, city, street, venue, zipcode) VALUES ('MA002', 'Worcester', 'Highland_st', 'Morgan_Hall', '01609');
INSERT into Address(Lid, city, street, venue, zipcode) VALUES ('CT001', 'Mashantucket', 'Foxwoods_st', 'The_Fox_Theater', '06338');
INSERT into Address(Lid, city, street, venue, zipcode) VALUES ('MA003', 'Boston', 'Charls_st', 'Charls_Playhouse', '02109');
INSERT into Address(Lid, city, street, venue, zipcode) VALUES ('MA004', 'Worcester', 'Harlow_st', 'Sprinkler_Factory', '01609');

INSERT INTO held(Eid, Lid) VALUES ('0001', 'MA001');
INSERT INTO held(Eid, Lid) VALUES ('0002', 'MA002');
INSERT INTO held(Eid, Lid) VALUES ('0003', 'CT001');
INSERT INTO held(Eid, Lid) VALUES ('0004', 'MA003');
INSERT INTO held(Eid, Lid) VALUES ('0005', 'MA004');

INSERT INTO Perform(Eid, Aid) VALUES ('0001', 'I0001');
INSERT INTO Perform(Eid, Aid) VALUES ('0002', 'S0001');
INSERT INTO Perform(Eid, Aid) VALUES ('0003', 'T0001');
INSERT INTO Perform(Eid, Aid) VALUES ('0003', 'T0002');
INSERT INTO Perform(Eid, Aid) VALUES ('0004', 'T0003');

INSERT INTO Theater(Eid, genre) VALUES ('0003', 'Cultural');
INSERT INTO Theater(Eid, genre) VALUES ('0004', 'Music');

INSERT INTO Ticket_has(Eid, Tid, price, amount, refund_policy) VALUES ('0001', 'A001', 1000, 500, 'Never');
INSERT INTO Ticket_has(Eid, Tid, price, amount, refund_policy) VALUES ('0002', 'C001', 500, 10, 'As_you_wish');
INSERT INTO Ticket_has(Eid, Tid, price, amount, refund_policy) VALUES ('0002', 'A001', 1000, 80, 'Two_days_before');
INSERT INTO Ticket_has(Eid, Tid, price, amount, refund_policy) VALUES ('0003', 'A001', 100, 1500, 'Never');
INSERT INTO Ticket_has(Eid, Tid, price, amount, refund_policy) VALUES ('0004', 'A001', 50, 8000, 'One_day_before');

INSERT INTO Time_on(Eid, time_serial, Tmonth, Tday, Tyear) VALUES ('0001', '01', 04, 06, 2020);
INSERT INTO Time_on(Eid, time_serial, Tmonth, Tday, Tyear) VALUES ('0002', '02', 05, 17, 2020);
INSERT INTO Time_on(Eid, time_serial, Tmonth, Tday, Tyear) VALUES ('0003', '03', 07, 06, 2020);
INSERT INTO Time_on(Eid, time_serial, Tmonth, Tday, Tyear) VALUES ('0004', '04', 09, 06, 2020);
INSERT INTO Time_on(Eid, time_serial, Tmonth, Tday, Tyear) VALUES ('0005', '05', 12, 31, 2020);
