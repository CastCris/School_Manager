CREATE TABLE `LocalWork`(
    `dek` CHAR(255) NOT NULL,
    `hashed_Id` CHAR(255) NOT NULL,
    `hashed_Name` CHAR(255) NOT NULL,
    `cipher_Id` CHAR(255) NOT NULL,
    `cipher_Name` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_Id`)
);
ALTER TABLE
    `LocalWork` ADD UNIQUE `localwork_hashed_name_unique`(`hashed_Name`);
CREATE TABLE `Departament`(
    `dek` CHAR(255) NOT NULL,
    `hashed_Id` CHAR(255) NOT NULL,
    `hashed_Name` CHAR(255) NOT NULL,
    `cipher_Id` CHAR(255) NOT NULL,
    `cipher_Name` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_Id`)
);
ALTER TABLE
    `Departament` ADD UNIQUE `departament_hashed_name_unique`(`hashed_Name`);
CREATE TABLE `Departament_LocalWork`(
    `dek` CHAR(255) NOT NULL,
    `LocalWork_id` CHAR(255) NOT NULL,
    `Departament_id` CHAR(255) NOT NULL,
    PRIMARY KEY(`Departament_id`)
);
ALTER TABLE
    `Departament_LocalWork` ADD UNIQUE `departament_localwork_localwork_id_unique`(`LocalWork_id`);
CREATE TABLE `Person_infos`(
    `dek` CHAR(255) NOT NULL,
    `Person_cpf` CHAR(255) NOT NULL,
    `hashed_email` CHAR(255) NOT NULL,
    `hashed_phone` CHAR(255) NOT NULL,
    `cipher_email` VARCHAR(255) NOT NULL,
    `cipher_phone` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`Person_cpf`)
);
ALTER TABLE
    `Person_infos` ADD INDEX `person_infos_hashed_email_index`(`hashed_email`);
ALTER TABLE
    `Person_infos` ADD INDEX `person_infos_hashed_phone_index`(`hashed_phone`);
CREATE TABLE `Person`(
    `dek` CHAR(255) NOT NULL,
    `Register_id` CHAR(255) NOT NULL,
    `hashed_cpf` CHAR(255) NOT NULL,
    `hashed_cep` CHAR(255) NOT NULL,
    `hashed_name` CHAR(255) NOT NULL,
    `cipher_cpf` CHAR(255) NOT NULL,
    `cipher_cep` CHAR(255) NOT NULL,
    `cipher_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_cpf`)
);
ALTER TABLE
    `Person` ADD INDEX `person_register_id_index`(`Register_id`);
ALTER TABLE
    `Person` ADD INDEX `person_hashed_cep_index`(`hashed_cep`);
ALTER TABLE
    `Person` ADD INDEX `person_hashed_name_index`(`hashed_name`);
CREATE TABLE `Register`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `data_register` TIMESTAMP NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
CREATE TABLE `Student`(
    `Register_id` CHAR(255) NOT NULL,
    `Course_id` CHAR(255) NOT NULL,
    `IRA` INT NOT NULL,
    `status` INT NOT NULL,
    PRIMARY KEY(`Register_id`)
);
ALTER TABLE
    `Student` ADD INDEX `student_course_id_index`(`Course_id`);
CREATE TABLE `Agreement`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `Departament_id` CHAR(255) NOT NULL,
    `Register_id` CHAR(255) NOT NULL,
    `TagTime_id` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `term_path` VARCHAR(255) NULL,
    `type` INT NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `Agreement` ADD INDEX `agreement_departament_id_index`(`Departament_id`);
ALTER TABLE
    `Agreement` ADD INDEX `agreement_register_id_index`(`Register_id`);
ALTER TABLE
    `Agreement` ADD INDEX `agreement_tagtime_id_index`(`TagTime_id`);
CREATE TABLE `Task`(
    `TaskNiche_id` CHAR(255) NOT NULL,
    `Agreeement_id` CHAR(255) NOT NULL,
    PRIMARY KEY(`TaskNiche_id`)
);
ALTER TABLE
    `Task` ADD PRIMARY KEY(`Agreeement_id`);
CREATE TABLE `TaskNiche`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hashed_name` CHAR(255) NOT NULL,
    `Departament_id` CHAR(255) NOT NULL,
    `TagTime_id` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `cipher_name` VARCHAR(255) NOT NULL,
    `type` INT NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `TaskNiche` ADD INDEX `taskniche_hashed_name_index`(`hashed_name`);
ALTER TABLE
    `TaskNiche` ADD INDEX `taskniche_departament_id_index`(`Departament_id`);
ALTER TABLE
    `TaskNiche` ADD INDEX `taskniche_tagtime_id_index`(`TagTime_id`);
CREATE TABLE `TagTime`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `time_init` TIMESTAMP NOT NULL,
    `time_end` TIMESTAMP NOT NULL
);
CREATE TABLE `Bulletin`(
    `Agreement_id` CHAR(255) NOT NULL,
    `GeneralBulletin_id` CHAR(255) NOT NULL,
    `grade` INT NOT NULL,
    `status` INT NOT NULL,
    PRIMARY KEY(`Agreement_id`)
);
ALTER TABLE
    `Bulletin` ADD PRIMARY KEY(`GeneralBulletin_id`);
CREATE TABLE `GeneralBulletin`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `Student_id` CHAR(255) NOT NULL,
    `cipher_id` CHAR(255) NOT NULL,
    `average` INT NOT NULL,
    `status` INT NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `GeneralBulletin` ADD INDEX `generalbulletin_student_id_index`(`Student_id`);
CREATE TABLE `Course`(
    `dek` CHAR(255) NOT NULL,
    `hashed_id` CHAR(255) NOT NULL,
    `hashed_name` VARCHAR(255) NOT NULL,
    `TagTime_id` CHAR(255) NOT NULL,
    `cipher_id` BIGINT NOT NULL,
    `cipher_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`hashed_id`)
);
ALTER TABLE
    `Course` ADD INDEX `course_hashed_name_index`(`hashed_name`);
ALTER TABLE
    `Task` ADD CONSTRAINT `task_agreeement_id_foreign` FOREIGN KEY(`Agreeement_id`) REFERENCES `Agreement`(`hashed_id`);
ALTER TABLE
    `TaskNiche` ADD CONSTRAINT `taskniche_departament_id_foreign` FOREIGN KEY(`Departament_id`) REFERENCES `Departament_LocalWork`(`Departament_id`);
ALTER TABLE
    `Student` ADD CONSTRAINT `student_course_id_foreign` FOREIGN KEY(`Course_id`) REFERENCES `Course`(`hashed_id`);
ALTER TABLE
    `Person` ADD CONSTRAINT `person_register_id_foreign` FOREIGN KEY(`Register_id`) REFERENCES `Register`(`hashed_id`);
ALTER TABLE
    `Agreement` ADD CONSTRAINT `agreement_tagtime_id_foreign` FOREIGN KEY(`TagTime_id`) REFERENCES `TagTime`(`id`);
ALTER TABLE
    `Departament` ADD CONSTRAINT `departament_hashed_id_foreign` FOREIGN KEY(`hashed_Id`) REFERENCES `Departament_LocalWork`(`Departament_id`);
ALTER TABLE
    `Agreement` ADD CONSTRAINT `agreement_departament_id_foreign` FOREIGN KEY(`Departament_id`) REFERENCES `Departament_LocalWork`(`Departament_id`);
ALTER TABLE
    `Departament_LocalWork` ADD CONSTRAINT `departament_localwork_localwork_id_foreign` FOREIGN KEY(`LocalWork_id`) REFERENCES `LocalWork`(`hashed_Id`);
ALTER TABLE
    `Agreement` ADD CONSTRAINT `agreement_register_id_foreign` FOREIGN KEY(`Register_id`) REFERENCES `Register`(`hashed_id`);
ALTER TABLE
    `Person` ADD CONSTRAINT `person_hashed_cpf_foreign` FOREIGN KEY(`hashed_cpf`) REFERENCES `Person_infos`(`Person_cpf`);
ALTER TABLE
    `TaskNiche` ADD CONSTRAINT `taskniche_tagtime_id_foreign` FOREIGN KEY(`TagTime_id`) REFERENCES `TagTime`(`id`);
ALTER TABLE
    `Register` ADD CONSTRAINT `register_hashed_id_foreign` FOREIGN KEY(`hashed_id`) REFERENCES `Student`(`Register_id`);
ALTER TABLE
    `Bulletin` ADD CONSTRAINT `bulletin_agreement_id_foreign` FOREIGN KEY(`Agreement_id`) REFERENCES `Agreement`(`hashed_id`);
ALTER TABLE
    `Bulletin` ADD CONSTRAINT `bulletin_generalbulletin_id_foreign` FOREIGN KEY(`GeneralBulletin_id`) REFERENCES `GeneralBulletin`(`hashed_id`);
ALTER TABLE
    `Task` ADD CONSTRAINT `task_taskniche_id_foreign` FOREIGN KEY(`TaskNiche_id`) REFERENCES `TaskNiche`(`hashed_id`);
ALTER TABLE
    `Course` ADD CONSTRAINT `course_tagtime_id_foreign` FOREIGN KEY(`TagTime_id`) REFERENCES `TagTime`(`id`);
ALTER TABLE
    `GeneralBulletin` ADD CONSTRAINT `generalbulletin_student_id_foreign` FOREIGN KEY(`Student_id`) REFERENCES `Student`(`Register_id`);