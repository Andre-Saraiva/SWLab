--
-- Table structure for table "Dataset_Features"
--

DROP TABLE IF EXISTS "Dataset_Features";
CREATE TABLE "Dataset_Features" (
  "ds_feature_id" int(11) NOT NULL,
  "ft_feature_id" int(11) NOT NULL,
  "count" int(11) DEFAULT NULL,
  "resource_id" int(11) NOT NULL,
  PRIMARY KEY ("ds_feature_id","ft_feature_id"),
  KEY "fk_Dataset_has_Features_Features1_idx" ("ft_feature_id"),
  KEY "fk_Dataset_Features_Resources1_idx" ("resource_id"),
  CONSTRAINT "fk_Dataset_has_Features_Dataset1" FOREIGN KEY ("ds_feature_id") REFERENCES "Datasets" ("feature_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "fk_Dataset_has_Features_Features1" FOREIGN KEY ("ft_feature_id") REFERENCES "Features" ("feature_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "fk_Dataset_Features_Resources1" FOREIGN KEY ("resource_id") REFERENCES "Resources" ("resource_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

--
-- Dumping data for table "Dataset_Features"
--

LOCK TABLES "Dataset_Features" WRITE;
UNLOCK TABLES;

--
-- Table structure for table "Datasets"
--

DROP TABLE IF EXISTS "Datasets";
CREATE TABLE "Datasets" (
  "feature_id" int(11) NOT NULL,
  "datahub_id" varchar(45) DEFAULT NULL,
  "metaurl" varchar(255) DEFAULT NULL,
  "name" varchar(45) DEFAULT NULL,
  "url" varchar(255) DEFAULT NULL,
  "created_at" datetime DEFAULT NULL,
  "modified_at" datetime DEFAULT NULL,
  PRIMARY KEY ("feature_id"),
  KEY "fk_Datasets_1_idx" ("feature_id"),
  CONSTRAINT "fk_Datasets_1" FOREIGN KEY ("feature_id") REFERENCES "Features" ("feature_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

--
-- Dumping data for table "Datasets"
--

LOCK TABLES "Datasets" WRITE;
UNLOCK TABLES;

--
-- Table structure for table "Features"
--

DROP TABLE IF EXISTS "Features";
CREATE TABLE "Features" (
  "feature_id" int(11) NOT NULL,
  "namespace" varchar(255) DEFAULT NULL,
  "type_id" int(11) NOT NULL,
  PRIMARY KEY ("feature_id"),
  KEY "fk_Features_Types_idx" ("type_id"),
  CONSTRAINT "fk_Features_Types" FOREIGN KEY ("type_id") REFERENCES "Types" ("type_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

--
-- Dumping data for table "Features"
--

LOCK TABLES "Features" WRITE;
UNLOCK TABLES;

--
-- Table structure for table "Resources"
--

DROP TABLE IF EXISTS "Resources";
CREATE TABLE "Resources" (
  "resource_id" int(11) NOT NULL,
  "format" varchar(45) DEFAULT NULL,
  "url" varchar(255) DEFAULT NULL,
  "source" varchar(255) DEFAULT NULL,
  "description" varchar(255) DEFAULT NULL,
  "is_online" tinyint(4) DEFAULT NULL,
  "feature_id" int(11) NOT NULL,
  PRIMARY KEY ("resource_id"),
  KEY "fk_Resources_Datasets1_idx" ("feature_id"),
  CONSTRAINT "fk_Resources_Datasets1" FOREIGN KEY ("feature_id") REFERENCES "Datasets" ("feature_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

--
-- Dumping data for table "Resources"
--

LOCK TABLES "Resources" WRITE;
UNLOCK TABLES;

--
-- Table structure for table "Types"
--

DROP TABLE IF EXISTS "Types";
CREATE TABLE "Types" (
  "type_id" int(11) NOT NULL,
  "name" varchar(45) DEFAULT NULL,
  PRIMARY KEY ("type_id")
);

--
-- Dumping data for table "Types"
--

LOCK TABLES "Types" WRITE;
UNLOCK TABLES;
