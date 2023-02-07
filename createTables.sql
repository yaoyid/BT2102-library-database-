CREATE TABLE Membership(  
     memberID    VARCHAR(10)    NOT NULL,
     name       VARCHAR(100)   NOT NULL,
     faculty    VARCHAR(15),
     telNo      VARCHAR(15),
     eMail      VARCHAR(25),
	 PRIMARY KEY (memberID)); 
CREATE TABLE Book(
     accessionNo    VARCHAR(10)    NOT NULL,
     title       VARCHAR(100),
     isbn       VARCHAR(15),
     publisher    VARCHAR(100),
	yearPublished   YEAR,
	PRIMARY KEY (accessionNo)); 
     
CREATE TABLE Author(
     accessionNo     VARCHAR(10)    NOT NULL,
     name       VARCHAR(100),
     PRIMARY KEY (accessionNo, name),
     FOREIGN KEY (accessionNo)    REFERENCES Book(accessionNo)    ON DELETE CASCADE
																  ON UPDATE CASCADE);
     
CREATE TABLE BookLoan( 
     accessionNo     VARCHAR(10)    NOT NULL,
     borrowDate      DATE          NOT NULL,
     dueDate         DATE          NOT NULL,
     memberID    VARCHAR(10)    NOT NULL,
     PRIMARY KEY (accessionNo, memberID),
     FOREIGN KEY (accessionNo)    REFERENCES Book(accessionNo)    ON DELETE CASCADE
     														      ON UPDATE CASCADE,
     FOREIGN KEY (memberID)    REFERENCES Membership(memberID)    ON DELETE CASCADE
																  ON UPDATE CASCADE); 
    
     
     CREATE TABLE BookReservation( 
     accessionNo     VARCHAR(10)    NOT NULL,
     reserveDate      DATE,
     memberID    VARCHAR(10)    NOT NULL,
     PRIMARY KEY (accessionNo, memberID),
     FOREIGN KEY (accessionNo)    REFERENCES Book(accessionNo)    ON DELETE CASCADE
     														      ON UPDATE CASCADE,
     FOREIGN KEY (memberID)    REFERENCES Membership(memberID)    ON DELETE CASCADE
     														      ON UPDATE CASCADE); 
     
CREATE TABLE Fine( 
     memberID    VARCHAR(10)    NOT NULL,
     paymentDate    DATE,
	 amount     DECIMAL(6,2)    NOT NULL DEFAULT 0,
     PRIMARY KEY (memberID),
     FOREIGN KEY (memberID)    REFERENCES Membership(memberID)    ON DELETE CASCADE
     														      ON UPDATE CASCADE); 
     

     
