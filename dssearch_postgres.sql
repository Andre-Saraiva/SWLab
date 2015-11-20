DROP TABLE IF EXISTS check_voids;
DROP TABLE IF EXISTS dataset_features;
DROP TABLE IF EXISTS resources;
DROP TABLE IF EXISTS datasets;
DROP TABLE IF EXISTS features;
DROP TABLE IF EXISTS types;

CREATE TABLE types (
  type_id SERIAL NOT NULL,
  name VARCHAR(45),
  PRIMARY KEY (type_id)
);


CREATE TABLE features (
  feature_id SERIAL NOT NULL,
  namespace VARCHAR(2083),
  type_id INTEGER NOT NULL,
  PRIMARY KEY (feature_id),
  CONSTRAINT fk_features_types FOREIGN KEY(type_id) REFERENCES types (type_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE datasets (
  feature_id INTEGER NOT NULL,
  meta VARCHAR(45),
  meta_id VARCHAR(45),
  meta_url VARCHAR(2083),
  name VARCHAR(150),
  url VARCHAR(2083),
  created_at TIMESTAMP WITHOUT TIME ZONE,
  modified_at TIMESTAMP WITHOUT TIME ZONE,
  PRIMARY KEY (feature_id),
  CONSTRAINT fk_datasets_features FOREIGN KEY(feature_id) REFERENCES features (feature_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE resources (
  resource_id SERIAL NOT NULL,
  format VARCHAR(500),
  url VARCHAR(10000),
  source VARCHAR(45),
  description VARCHAR(5000),
  is_online BOOLEAN,
  feature_id INTEGER,
  PRIMARY KEY (resource_id),
  CONSTRAINT fk_resources_features FOREIGN KEY(feature_id) REFERENCES features (feature_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);


CREATE TABLE dataset_features (
  ds_feature_id INTEGER NOT NULL,
  ft_feature_id INTEGER NOT NULL,
  count INTEGER,
  resource_id INTEGER,
  PRIMARY KEY (ds_feature_id, ft_feature_id, resource_id),
  CONSTRAINT fk_dataset_features_datasets FOREIGN KEY(ds_feature_id) REFERENCES datasets (feature_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_dataset_features_features FOREIGN KEY(ft_feature_id) REFERENCES features (feature_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_dataset_features_resources FOREIGN KEY(resource_id) REFERENCES resources (resource_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE check_voids (
  check_void_id SERIAL NOT NULL,
  content_type VARCHAR(255),
  url VARCHAR(2083),
  source VARCHAR(45),
  feature_id INTEGER,
  content BYTEA,
  encoding VARCHAR(255),
  hash VARCHAR(255),
  PRIMARY KEY (check_void_id),
  CONSTRAINT fk_check_voids_features FOREIGN KEY(feature_id) REFERENCES features (feature_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE resource_cache (
  resource_id INTEGER NOT NULL,
  hash VARCHAR(255),
  content BYTEA,
  content_type VARCHAR(255),
  PRIMARY KEY (resource_id),
  encoding VARCHAR(255),
  CONSTRAINT fk_resource_cache_resources FOREIGN KEY(resource_id) REFERENCES resources (resource_id) ON DELETE NO ACTION ON UPDATE NO ACTION
)

INSERT INTO types (name) VALUES ('dataset');
INSERT INTO types (name) VALUES ('property');
INSERT INTO types (name) VALUES ('class');
INSERT INTO types (name) VALUES ('vocabulary');
