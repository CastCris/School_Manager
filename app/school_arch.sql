PRAGMA foreign_keys=ON;

--
CREATE TABLE IF NOT EXISTS Site(
    ID      CHAR(20) PRIMARY KEY,
    Name    VARCHAR(81) UNIQUE NOT NULL
    
);

CREATE TABLE IF NOT EXISTS Sector(
    ID      CHAR(20) PRIMARY KEY,
    Name    VARCHAR(81) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Sector_Sites(
    ID_Site    CHAR(20),
    ID_Sector  CHAR(20),

    --
    CONSTRAINT FK_ID_Site
        FOREIGN KEY(ID_Site) REFERENCES Site(ID),

    CONSTRAINT FK_ID_Sector
        FOREIGN KEY(ID_Sector) REFERENCES Sector(ID)
);

-- 
CREATE TABLE IF NOT EXISTS Person(
    -- CPF max len plus 1
    CPF     CHAR(12) PRIMARY KEY,       
     -- CEP max len plus 1
    CEP     CHAR(9) NOT NULL,

    Name    VARCHAR(81) NOT NULL   -- Max len name on passport plus 1
);

CREATE TABLE IF NOT EXISTS Phone(
    CPF     CHAR(12),
    Digits  VARCHAR(20) NOT NULL,

    --
    CONSTRAINT FK_CPF
        FOREIGN KEY(CPF) REFERENCES Person(CPF)

);

--
CREATE TABLE IF NOT EXISTS Agreement(
    ID         CHAR(20) PRIMARY KEY,
    ID_Sector  CHAR(20),
    CPF        CHAR(12),

    SALARY  INTEGER NOT NULL,

    --
    CONSTRAINT FK_ID_Sector
        FOREIGN KEY(ID_Sector) REFERENCES Sector(ID),

    CONSTRAINT FK_CPF
        FOREIGN KEY(CPF) REFERENCES Person(CPF) 
);

CREATE TABLE IF NOT EXISTS Task_niche(
    ID          CHAR(20) PRIMARY KEY,
    ID_Site     CHAR(20),

    Niche_name  VARCHAR(81) NOT NULL,

    CONSTRAINT FK_ID_Site
        FOREIGN KEY(ID_Site) REFERENCES Site(ID)
);


CREATE TABLE IF NOT EXISTS Task(
    ID              CHAR(20) PRIMARY KEY,
    ID_Task_niche   CHAR(20),
    ID_Agreement    CHAR(20),

    CONSTRAINT FK_ID_Task_niche
        FOREIGN KEY(ID_Task_niche) REFERENCES Task_niche(ID),
    
    CONSTRAINT FK_ID_Agreement
        FOREIGN KEY(ID_Agreement) REFERENCES Agreement(ID)
);

CREATE TABLE IF NOT EXISTS Term(
    ID      CHAR(20) PRIMARY KEY,
    ID_Task CHAR(20),

    CONSTRAINT FK_ID_Task
        FOREIGN KEY(ID_Task)  REFERENCES Task(ID)
);

--
CREATE TABLE IF NOT EXISTS Bulletin(
    ID      CHAR(20) PRIMARY KEY,
    ID_Task CHAR(20),

    CONSTRAINT FK_ID_Task
        FOREIGN KEY(ID_Task)  REFERENCES Task(ID)
);

