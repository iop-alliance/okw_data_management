-- Open-Know-Where Initiative Distributed Resources Data Schema
-- Schema for managing distributed resources data.
-- Author: The Internet of Production Alliance, Antonio de Jesus Anaya Hernandez
-- License: CC BY-SA 4.0
-- 2024, The Internet of Production Alliance.
-- https://map.internetofproduction.org
-- https://github.com/iop-alliance

-- Table storing addresses
CREATE TABLE Address (
  address_id INT PRIMARY KEY,
  street VARCHAR(255),
  number VARCHAR(50),
  locality VARCHAR(100),
  region VARCHAR(100),
  postcode INTEGER,
  country VARCHAR(100),
  latitude FLOAT,
  longitude FLOAT
);

-- Table storing contact information
CREATE TABLE Contact (
  contact_id INT PRIMARY KEY,
  social VARCHAR(255),
  email VARCHAR(255),
  website VARCHAR(255)
);

-- Table storing database source metadata
CREATE TABLE DatabaseSourceMetadata (
  source_id INT PRIMARY KEY,
  name VARCHAR(255),
  description TEXT,
  source_type VARCHAR(50),
  source_url VARCHAR(255),
  license VARCHAR(100),
  version VARCHAR(50),
  creation_date DATETIME,
  update_date DATETIME,
  keywords VARCHAR(255),
  publisher VARCHAR(255),
  contributor VARCHAR(255),
  language VARCHAR(50)
);

-- Table storing distributed resources
CREATE TABLE DistributedResource (
  resource_id INT PRIMARY KEY,
  address_id INT,
  contact_id INT,
  verification BOOLEAN,
  verificator_id INT,
  source_id INT,
  FOREIGN KEY (address_id) REFERENCES Address(address_id),
  FOREIGN KEY (contact_id) REFERENCES Contact(contact_id),
  FOREIGN KEY (verificator_id) REFERENCES DataVerificator(verificator_id),
  FOREIGN KEY (source_id) REFERENCES DatabaseSourceMetadata(source_id)
);

-- Table storing data verificators
CREATE TABLE DataVerificator (
  verificator_id INT PRIMARY KEY,
  name VARCHAR(255),
  description TEXT,
  contact_id INT,
  address_id INT,
  FOREIGN KEY (contact_id) REFERENCES Contact(contact_id),
  FOREIGN KEY (address_id) REFERENCES Address(address_id)
);

-- Table storing manufacturing facilities
CREATE TABLE ManufacturingFacility (
  facility_id INT PRIMARY KEY,
  resource_id INT,
  name VARCHAR(255),
  description TEXT,
  type VARCHAR(100),
  capacity INT,
  capabilities TEXT,
  source_id INT,
  FOREIGN KEY (resource_id) REFERENCES DistributedResource(resource_id),
  FOREIGN KEY (source_id) REFERENCES DatabaseSourceMetadata(source_id)
);

-- Table storing manufacturing equipment
CREATE TABLE ManufacturingEquipment (
  equipment_id INT PRIMARY KEY,
  resource_id INT,
  brand VARCHAR(255),
  model VARCHAR(255),
  type VARCHAR(100),
  description TEXT,
  source_id INT,
  FOREIGN KEY (resource_id) REFERENCES DistributedResource(resource_id),
  FOREIGN KEY (source_id) REFERENCES DatabaseSourceMetadata(source_id)
);

-- Table storing manufacturing services
CREATE TABLE ManufacturingService (
  service_id INT PRIMARY KEY,
  resource_id INT,
  type VARCHAR(100),
  description TEXT,
  source_id INT,
  FOREIGN KEY (resource_id) REFERENCES DistributedResource(resource_id),
  FOREIGN KEY (source_id) REFERENCES DatabaseSourceMetadata(source_id)
);

-- Table storing manufacturing skills
CREATE TABLE ManufacturingSkill (
  skill_id INT PRIMARY KEY,
  resource_id INT,
  name VARCHAR(255),
  bio TEXT,
  skills TEXT,
  source_id INT,
  FOREIGN KEY (resource_id) REFERENCES DistributedResource(resource_id),
  FOREIGN KEY (source_id) REFERENCES DatabaseSourceMetadata(source_id)
);

-- Table storing findable projects
CREATE TABLE FindableProject (
  project_id INT PRIMARY KEY,
  resource_id INT,
  name VARCHAR(255),
  description TEXT,
  source_id INT,
  FOREIGN KEY (resource_id) REFERENCES DistributedResource(resource_id),
  FOREIGN KEY (source_id) REFERENCES DatabaseSourceMetadata(source_id)
);
