CREATE TABLE Art_Events(
	Eid CHAR(60),
	title CHAR(60),
	e_image TEXT,
	seatmap TEXT,
	PRIMARY KEY (Eid));

CREATE TABLE Artist(
	Aid CHAR(20),
	artist_name CHAR(40),
	info CHAR(255),
	PRIMARY KEY (Aid));

CREATE TABLE Perform(
	Eid CHAR(20),
	Aid CHAR(40),
	PRIMARY KEY (Eid, Aid),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid),
	FOREIGN KEY (Aid) REFERENCES Artist(Aid));

CREATE TABLE Location(
	Lid CHAR(20),
	longitude CHAR(30),
	latitude CHAR(30),
	address CHAR(100),
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
	PRIMARY KEY (Tid,Eid),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid) ON DELETE CASCADE);

CREATE TABLE Time(
	time_serial CHAR(20),
	date_YMD CHAR(20),
	PRIMARY KEY (time_serial));

CREATE TABLE T_on(
	Eid CHAR(20),
	time_serial CHAR(20),
	PRIMARY KEY (Eid, time_serial),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid),
	FOREIGN KEY (time_serial) REFERENCES Time(time_serial),
	CHECK (COUNT(DISTINCT Eid) = (SELECT COUNT(DISTINCT Eid) FROM Art_Events))
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
	background TEXT,
	PRIMARY KEY (Eid),
	FOREIGN KEY (Eid) REFERENCES Art_Events(Eid) ON DELETE CASCADE);

CREATE TABLE Subscription(
	Sid CHAR(100),
	email CHAR(100),
	s_name CHAR(100),
	PRIMARY KEY (Sid));

CREATE TABLE Payment(
	Pid CHAR(20),
	address CHAR(200),
	fname CHAR(50),
	lname CHAR(50),
	ticket_num CHAR(20),
	total_price CHAR(20),
	PRIMARY KEY (Pid));

CREATE TABLE buy(
	Pid CHAR(20),
	Tid CHAR(20),
	Eid CHAR(20),
	PRIMARY KEY (Pid, Tid, Eid),
	FOREIGN KEY (Pid) REFERENCES Payment(Pid),
	FOREIGN KEY (Tid) REFERENCES Ticket_has(Tid),
	FOREIGN KEY (Eid) REFERENCES Ticket_has(Eid)
);
