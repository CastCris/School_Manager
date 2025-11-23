PRAGMA foreign_keys = ON;

CREATE TABLE LocalWork (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    hashed_name TEXT NOT NULL UNIQUE,
    cipher_id TEXT NOT NULL,
    cipher_name TEXT NOT NULL
);

CREATE TABLE Departament (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    hashed_name TEXT NOT NULL UNIQUE,
    cipher_id TEXT NOT NULL,
    cipher_name TEXT NOT NULL
);

CREATE TABLE Departament_LocalWork (
    dek TEXT NOT NULL,
    hashed_localWorkId TEXT NOT NULL UNIQUE,
    hashed_departamentId TEXT NOT NULL PRIMARY KEY,
    FOREIGN KEY(hashed_departamentId) REFERENCES Departament(hashed_id),
    FOREIGN KEY(hashed_localWorkId) REFERENCES LocalWork(hashed_id)
);
CREATE INDEX idx_departament_localwork_hashed_localworkid ON Departament_LocalWork(hashed_localWorkId);

CREATE TABLE PersonInfos (
    dek TEXT NOT NULL,
    hashed_personId INTEGER NOT NULL,
    hashed_cpf TEXT NOT NULL PRIMARY KEY,
    hashed_cep INTEGER NOT NULL,
    hashed_email TEXT NOT NULL,
    hashed_phone TEXT NOT NULL,
    cipher_cpf INTEGER NOT NULL,
    cipher_cep INTEGER NOT NULL,
    cipher_email TEXT NOT NULL,
    cipher_phone TEXT NOT NULL,
    FOREIGN KEY(hashed_personId) REFERENCES Person(id)
);
CREATE INDEX idx_personinfos_hashed_cep ON PersonInfos(hashed_cep);
CREATE INDEX idx_personinfos_hashed_email ON PersonInfos(hashed_email);
CREATE INDEX idx_personinfos_hashed_phone ON PersonInfos(hashed_phone);

CREATE TABLE Person (
    dek TEXT NOT NULL,
    id TEXT NOT NULL PRIMARY KEY,
    hashed_registerId TEXT NOT NULL,
    hashed_name TEXT NOT NULL,
    cipher_name TEXT NOT NULL,
    password TEXT NOT NULL,
    permissions INTEGER NOT NULL,
    FOREIGN KEY(hashed_registerId) REFERENCES Register(hashed_id)
);
CREATE INDEX idx_person_hashed_registerId ON Person(hashed_registerId);
CREATE INDEX idx_person_hashed_name ON Person(hashed_name);

CREATE TABLE Register (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    cipher_id TEXT NOT NULL,
    data_register REAL NOT NULL
);

CREATE TABLE Student (
    hashed_registerId TEXT NOT NULL PRIMARY KEY,
    hashed_courseId TEXT NOT NULL,
    IRA INTEGER NOT NULL,
    status INTEGER NOT NULL,
    FOREIGN KEY(hashed_courseId) REFERENCES Course(hashed_id),
    FOREIGN KEY(hashed_registerId) REFERENCES Register(hashed_id)
);
CREATE INDEX idx_student_hashed_courseId ON Student(hashed_courseId);

CREATE TABLE Agreement (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    hasehd_termPath INTEGER NOT NULL,
    hashed_departamentId TEXT NOT NULL,
    hashed_registerId TEXT NOT NULL,
    hashed_tagTimeId TEXT NOT NULL,
    cipher_id TEXT NOT NULL,
    cipher_termPath TEXT,
    type INTEGER NOT NULL,
    FOREIGN KEY(hashed_departamentId) REFERENCES Departament_LocalWork(hashed_departamentId),
    FOREIGN KEY(hashed_registerId) REFERENCES Register(hashed_id),
    FOREIGN KEY(hashed_tagTimeId) REFERENCES TagTime(hashed_id)
);
CREATE INDEX idx_agreement_hashed_departamentId ON Agreement(hashed_departamentId);
CREATE INDEX idx_agreement_hashed_registerId ON Agreement(hashed_registerId);
CREATE INDEX idx_agreement_hashed_tagTimeId ON Agreement(hashed_tagTimeId);

CREATE TABLE Task (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    hashed_taskNicheId TEXT NOT NULL UNIQUE,
    hashed_agreementId TEXT NOT NULL UNIQUE,
    cipher_id TEXT NOT NULL,
    FOREIGN KEY(hashed_taskNicheId) REFERENCES TaskNiche(hashed_id),
    FOREIGN KEY(hashed_agreementId) REFERENCES Agreement(hashed_id)
);
CREATE INDEX idx_task_hashed_taskNicheId_hashed_agreementId ON Task(hashed_taskNicheId, hashed_agreementId);

CREATE TABLE TaskNiche (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    hashed_name TEXT NOT NULL,
    hashed_departamentId TEXT NOT NULL,
    hashed_tagTimeId TEXT NOT NULL,
    cipher_id TEXT NOT NULL,
    cipher_name TEXT NOT NULL,
    type INTEGER NOT NULL,
    FOREIGN KEY(hashed_departamentId) REFERENCES Departament_LocalWork(hashed_departamentId),
    FOREIGN KEY(hashed_tagTimeId) REFERENCES TagTime(hashed_id)
);
CREATE INDEX idx_taskniche_hashed_name ON TaskNiche(hashed_name);
CREATE INDEX idx_taskniche_hashed_departamentId ON TaskNiche(hashed_departamentId);
CREATE INDEX idx_taskniche_hashed_tagTimeId ON TaskNiche(hashed_tagTimeId);

CREATE TABLE TagTime (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    hashed_name TEXT NOT NULL,
    cipher_id TEXT NOT NULL,
    cipher_name TEXT NOT NULL,
    time_init REAL NOT NULL,
    time_end REAL NOT NULL
);

CREATE TABLE Bulletin (
    hashed_agreementId TEXT NOT NULL PRIMARY KEY,
    hashed_bulletinGeneralId TEXT NOT NULL,
    grade INTEGER NOT NULL,
    status INTEGER NOT NULL,
    FOREIGN KEY(hashed_agreementId) REFERENCES Agreement(hashed_id),
    FOREIGN KEY(hashed_bulletinGeneralId) REFERENCES BulletinGeneral(hashed_id)
);
CREATE INDEX idx_bulletin_hashed_agreementId_bulletinGeneralId ON Bulletin(hashed_agreementId, hashed_bulletinGeneralId);

CREATE TABLE BulletinGeneral (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    hashed_studentId TEXT NOT NULL,
    cipher_id TEXT NOT NULL,
    average INTEGER NOT NULL,
    status INTEGER NOT NULL,
    FOREIGN KEY(hashed_studentId) REFERENCES Student(hashed_registerId)
);
CREATE INDEX idx_bulletinGeneral_hashed_studentId ON BulletinGeneral(hashed_studentId);

CREATE TABLE Course (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    hashed_name TEXT NOT NULL,
    hashed_tagTimeId TEXT NOT NULL,
    cipher_id TEXT NOT NULL,
    cipher_name TEXT NOT NULL,
    FOREIGN KEY(hashed_tagTimeId) REFERENCES TagTime(hashed_id)
);
CREATE INDEX idx_course_hashed_name ON Course(hashed_name);
