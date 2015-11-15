DROP SCHEMA IF EXISTS `datamob` ;
CREATE SCHEMA IF NOT EXISTS `datamob` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `datamob` ;

-- -----------------------------------------------------
-- Table `datamob`.`Types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `datamob`.`Types` ;

CREATE TABLE IF NOT EXISTS `datamob`.`Types` (
  `type_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `datamob`.`Features`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `datamob`.`Features` ;

CREATE TABLE IF NOT EXISTS `datamob`.`Features` (
  `feature_id` INT NOT NULL AUTO_INCREMENT,
  `namespace` VARCHAR(255) NULL,
  `type_id` INT NOT NULL,
  PRIMARY KEY (`feature_id`),
  INDEX `fk_Features_Types_idx` (`type_id` ASC),
  CONSTRAINT `fk_Features_Types`
    FOREIGN KEY (`type_id`)
    REFERENCES `datamob`.`Types` (`type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `datamob`.`Datasets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `datamob`.`Datasets` ;

CREATE TABLE IF NOT EXISTS `datamob`.`Datasets` (
  `feature_id` INT NOT NULL,
  `datahub_id` VARCHAR(45) NULL,
  `metaurl` VARCHAR(255) NULL,
  `name` VARCHAR(45) NULL,
  `url` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `modified_at` DATETIME NULL,
  PRIMARY KEY (`feature_id`),
  INDEX `fk_Datasets_1_idx` (`feature_id` ASC),
  CONSTRAINT `fk_Datasets_1`
    FOREIGN KEY (`feature_id`)
    REFERENCES `datamob`.`Features` (`feature_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `datamob`.`Resources`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `datamob`.`Resources` ;

CREATE TABLE IF NOT EXISTS `datamob`.`Resources` (
  `resource_id` INT NOT NULL AUTO_INCREMENT,
  `format` VARCHAR(45) NULL,
  `url` VARCHAR(255) NULL,
  `source` VARCHAR(255) NULL,
  `description` VARCHAR(255) NULL,
  `is_online` TINYINT NULL,
  `feature_id` INT NOT NULL,
  PRIMARY KEY (`resource_id`),
  INDEX `fk_Resources_Datasets1_idx` (`feature_id` ASC),
  CONSTRAINT `fk_Resources_Datasets1`
    FOREIGN KEY (`feature_id`)
    REFERENCES `datamob`.`Datasets` (`feature_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `datamob`.`Dataset_Features`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `datamob`.`Dataset_Features` ;

CREATE TABLE IF NOT EXISTS `datamob`.`Dataset_Features` (
  `ds_feature_id` INT NOT NULL,
  `ft_feature_id` INT NOT NULL,
  `count` INT NULL,
  `resource_id` INT NOT NULL,
  PRIMARY KEY (`ds_feature_id`, `ft_feature_id`),
  INDEX `fk_Dataset_has_Features_Features1_idx` (`ft_feature_id` ASC),
  INDEX `fk_Dataset_Features_Resources1_idx` (`resource_id` ASC),
  CONSTRAINT `fk_Dataset_has_Features_Dataset1`
    FOREIGN KEY (`ds_feature_id`)
    REFERENCES `datamob`.`Datasets` (`feature_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Dataset_has_Features_Features1`
    FOREIGN KEY (`ft_feature_id`)
    REFERENCES `datamob`.`Features` (`feature_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Dataset_Features_Resources1`
    FOREIGN KEY (`resource_id`)
    REFERENCES `datamob`.`Resources` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
