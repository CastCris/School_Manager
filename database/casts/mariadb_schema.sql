CREATE TABLE `LocalWork`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hashed_name` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `cipher_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `LocalWork` ADD INDEX `localwork_hashed_id_index`(`hashed_id`);
ALTER TABLE
    `LocalWork` ADD UNIQUE `localwork_hashed_name_unique`(`hashed_name`);
CREATE TABLE `Departament`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hashed_name` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `cipher_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `Departament` ADD UNIQUE `departament_hashed_name_unique`(`hashed_name`);
CREATE TABLE `Departament_LocalWork`(
    `dek` CHAR(255) NOT NULL,
    `hashed_localWorkId` CHAR(255) NOT NULL,
    `hashed_departamentId` CHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_departamentId`)
);
ALTER TABLE
    `Departament_LocalWork` ADD INDEX `departament_localwork_hashed_localworkid_index`(`hashed_localWorkId`);
ALTER TABLE
    `Departament_LocalWork` ADD UNIQUE `departament_localwork_hashed_localworkid_unique`(`hashed_localWorkId`);
CREATE TABLE `PersonInfos`(
    `dek` CHAR(255) NOT NULL,
    `hashed_personId` BIGINT NOT NULL,
    `hashed_cpf` CHAR(255) NOT NULL,
    `hashed_cep` BIGINT NOT NULL,
    `hashed_email` CHAR(255) NOT NULL,
    `hashed_phone` CHAR(255) NOT NULL,
    `cipher_cpf` BIGINT NOT NULL,
    `cipher_cep` BIGINT NOT NULL,
    `cipher_email` VARCHAR(255) NOT NULL,
    `cipher_phone` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_cpf`)
);
ALTER TABLE
    `PersonInfos` ADD INDEX `personinfos_hashed_cep_index`(`hashed_cep`);
ALTER TABLE
    `PersonInfos` ADD INDEX `personinfos_hashed_email_index`(`hashed_email`);
ALTER TABLE
    `PersonInfos` ADD INDEX `personinfos_hashed_phone_index`(`hashed_phone`);
CREATE TABLE `Person`(
    `dek` CHAR(255) NOT NULL,
    `id` CHAR(255) NOT NULL,
    `hashed_registerId` CHAR(255) NOT NULL,
    `hashed_name` CHAR(255) NOT NULL,
    `cipher_name` VARCHAR(255) NOT NULL,
    `password` CHAR(255) NOT NULL,
    `permissions` INT NOT NULL,
    PRIMARY KEY(`id`)
);
ALTER TABLE
    `Person` ADD INDEX `person_hashed_registerid_index`(`hashed_registerId`);
ALTER TABLE
    `Person` ADD INDEX `person_hashed_name_index`(`hashed_name`);
CREATE TABLE `Register`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `data_register` DOUBLE NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
CREATE TABLE `Student`(
    `hashed_registerId` CHAR(255) NOT NULL,
    `hashed_courseId` CHAR(255) NOT NULL,
    `IRA` INT NOT NULL,
    `status` INT NOT NULL,
    PRIMARY KEY(`hashed_registerId`)
);
ALTER TABLE
    `Student` ADD INDEX `student_hashed_courseid_index`(`hashed_courseId`);
CREATE TABLE `Agreement`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hasehd_termPath` BIGINT NOT NULL,
    `hashed_departamentId` CHAR(255) NOT NULL,
    `hashed_registerId` CHAR(255) NOT NULL,
    `hashed_tagTimeId` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `cipher_termPath` VARCHAR(255) NULL,
    `type` INT NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `Agreement` ADD INDEX `agreement_hashed_departamentid_index`(`hashed_departamentId`);
ALTER TABLE
    `Agreement` ADD INDEX `agreement_hashed_registerid_index`(`hashed_registerId`);
ALTER TABLE
    `Agreement` ADD INDEX `agreement_hashed_tagtimeid_index`(`hashed_tagTimeId`);
CREATE TABLE `Task`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hashed_taskNicheId` CHAR(255) NOT NULL,
    `hashed_agreementId` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `Task` ADD INDEX `task_hashed_tasknicheid_hashed_agreementid_index`(
        `hashed_taskNicheId`,
        `hashed_agreementId`
    );
ALTER TABLE
    `Task` ADD UNIQUE `task_hashed_tasknicheid_unique`(`hashed_taskNicheId`);
ALTER TABLE
    `Task` ADD UNIQUE `task_hashed_agreementid_unique`(`hashed_agreementId`);
CREATE TABLE `TaskNiche`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hashed_name` CHAR(255) NOT NULL,
    `hashed_departamentId` CHAR(255) NOT NULL,
    `hashed_tagTimeId` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `cipher_name` VARCHAR(255) NOT NULL,
    `type` INT NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `TaskNiche` ADD INDEX `taskniche_hashed_name_index`(`hashed_name`);
ALTER TABLE
    `TaskNiche` ADD INDEX `taskniche_hashed_departamentid_index`(`hashed_departamentId`);
ALTER TABLE
    `TaskNiche` ADD INDEX `taskniche_hashed_tagtimeid_index`(`hashed_tagTimeId`);
CREATE TABLE `TagTime`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hashed_name` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `cipher_name` VARCHAR(255) NOT NULL,
    `time_init` DOUBLE NOT NULL,
    `time_end` DOUBLE NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
CREATE TABLE `Bulletin`(
    `hashed_agreementId` CHAR(255) NOT NULL,
    `hashed_bulletinGeneralId` CHAR(255) NOT NULL,
    `grade` INT NOT NULL,
    `status` INT NOT NULL,
    PRIMARY KEY(`hashed_agreementId`)
);
ALTER TABLE
    `Bulletin` ADD INDEX `bulletin_hashed_agreementid_hashed_bulletingeneralid_index`(
        `hashed_agreementId`,
        `hashed_bulletinGeneralId`
    );
CREATE TABLE `BulletinGeneral`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hashed_studentId` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `average` INT NOT NULL,
    `status` INT NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `BulletinGeneral` ADD INDEX `bulletingeneral_hashed_studentid_index`(`hashed_studentId`);
CREATE TABLE `Course`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hashed_name` VARCHAR(255) NOT NULL,
    `hashed_tagTimeId` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `cipher_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `Course` ADD INDEX `course_hashed_name_index`(`hashed_name`);
ALTER TABLE
    `Departament_LocalWork` ADD CONSTRAINT `departament_localwork_hashed_departamentid_foreign` FOREIGN KEY(`hashed_departamentId`) REFERENCES `Departament`(`hashed_id`);
ALTER TABLE
    `TaskNiche` ADD CONSTRAINT `taskniche_hashed_tagtimeid_foreign` FOREIGN KEY(`hashed_tagTimeId`) REFERENCES `TagTime`(`hashed_id`);
ALTER TABLE
    `Task` ADD CONSTRAINT `task_hashed_agreementid_foreign` FOREIGN KEY(`hashed_agreementId`) REFERENCES `Agreement`(`hashed_id`);
ALTER TABLE
    `Course` ADD CONSTRAINT `course_hashed_tagtimeid_foreign` FOREIGN KEY(`hashed_tagTimeId`) REFERENCES `TagTime`(`hashed_id`);
ALTER TABLE
    `Person` ADD CONSTRAINT `person_hashed_registerid_foreign` FOREIGN KEY(`hashed_registerId`) REFERENCES `Register`(`hashed_id`);
ALTER TABLE
    `Student` ADD CONSTRAINT `student_hashed_courseid_foreign` FOREIGN KEY(`hashed_courseId`) REFERENCES `Course`(`hashed_id`);
ALTER TABLE
    `Task` ADD CONSTRAINT `task_hashed_tasknicheid_foreign` FOREIGN KEY(`hashed_taskNicheId`) REFERENCES `TaskNiche`(`hashed_id`);
ALTER TABLE
    `Departament_LocalWork` ADD CONSTRAINT `departament_localwork_hashed_localworkid_foreign` FOREIGN KEY(`hashed_localWorkId`) REFERENCES `LocalWork`(`hashed_id`);
ALTER TABLE
    `TaskNiche` ADD CONSTRAINT `taskniche_hashed_departamentid_foreign` FOREIGN KEY(`hashed_departamentId`) REFERENCES `Departament_LocalWork`(`hashed_departamentId`);
ALTER TABLE
    `Bulletin` ADD CONSTRAINT `bulletin_hashed_bulletingeneralid_foreign` FOREIGN KEY(`hashed_bulletinGeneralId`) REFERENCES `BulletinGeneral`(`hashed_id`);
ALTER TABLE
    `BulletinGeneral` ADD CONSTRAINT `bulletingeneral_hashed_studentid_foreign` FOREIGN KEY(`hashed_studentId`) REFERENCES `Student`(`hashed_registerId`);
ALTER TABLE
    `Agreement` ADD CONSTRAINT `agreement_hashed_departamentid_foreign` FOREIGN KEY(`hashed_departamentId`) REFERENCES `Departament_LocalWork`(`hashed_departamentId`);
ALTER TABLE
    `Agreement` ADD CONSTRAINT `agreement_hashed_tagtimeid_foreign` FOREIGN KEY(`hashed_tagTimeId`) REFERENCES `TagTime`(`hashed_id`);
ALTER TABLE
    `Student` ADD CONSTRAINT `student_hashed_registerid_foreign` FOREIGN KEY(`hashed_registerId`) REFERENCES `Register`(`hashed_id`);
ALTER TABLE
    `Agreement` ADD CONSTRAINT `agreement_hashed_registerid_foreign` FOREIGN KEY(`hashed_registerId`) REFERENCES `Register`(`hashed_id`);
ALTER TABLE
    `Bulletin` ADD CONSTRAINT `bulletin_hashed_agreementid_foreign` FOREIGN KEY(`hashed_agreementId`) REFERENCES `Agreement`(`hashed_id`);
ALTER TABLE
    `PersonInfos` ADD CONSTRAINT `personinfos_hashed_personid_foreign` FOREIGN KEY(`hashed_personId`) REFERENCES `Person`(`id`);