# Open-Know-Where Initiative Distributed Resources Data Schema

## Introduction

The Open-Know-Where Initiative Distributed Resources Data Schema is designed to manage information about distributed resources, such as manufacturing facilities, equipment, services, and skills. This schema provides a structured format for storing and organizing data related to these resources, enabling efficient management and analysis.

## Attributions

- **Authors:** The Internet of Production Alliance, Antonio de Jesus Anaya Hernandez
- **Year:** 2024
- **Publisher:** The Internet of Production Alliance
- **Sources:**
  - [Official Website](https://map.internetofproduction.org)
  - [GitHub Repository](https://github.com/iop-alliance)

## License

This schema is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt the schema for any purpose under the condition that you give appropriate credit to the authors and distribute any derivative works under the same license.


### Table: Address

Description: This table stores information about addresses.

| Field      | Type     | Description           |
|------------|----------|-----------------------|
| address_id | int      | Unique identifier for the address |
| street     | string   | Street name |
| number     | string   | House or building number |
| locality   | string   | Locality or district |
| region     | string   | Region or state |
| postcode   | integer  | Postal code |
| country    | string   | Country |
| latitude   | float    | Latitude coordinate |
| longitude  | float    | Longitude coordinate |

---

### Table: Contact

Description: This table stores contact information.

| Field       | Type     | Description           |
|-------------|----------|-----------------------|
| contact_id  | int      | Unique identifier for the contact |
| social      | string   | Social media handle |
| email       | string   | Email address |
| website     | string   | Website URL |

---

### Table: DatabaseSourceMetadata

Description: This table stores metadata information about database sources.

| Field         | Type     | Description           |
|---------------|----------|-----------------------|
| source_id     | int      | Unique identifier for the database source |
| name          | string   | Name or identifier of the database source |
| description   | string   | Description of the database source |
| source_type   | string   | Type of the database source (e.g., CSV, API, Database) |
| source_url    | string   | URL or location of the source (if applicable) |
| license       | string   | License information (e.g., CC-BY) |
| version       | string   | Version of the database source |
| creation_date | datetime | Date when the source was created |
| update_date   | datetime | Date of the last update |
| keywords      | string   | Keywords or tags describing the source |
| publisher     | string   | Publisher of the source |
| contributor   | string   | Contributor of the source |
| language      | string   | Language of the source |

---

### Table: DistributedResource

Description: This table stores information about distributed resources.

| Field          | Type     | Description           |
|----------------|----------|-----------------------|
| resource_id    | int      | Unique identifier for the resource |
| address_id     | int      | Reference to the address of the resource |
| contact_id     | int      | Reference to the contact information of the resource |
| verification   | bool     | Verification status of the resource |
| verificator_id | int      | Reference to the data verificator |
| source_id      | int      | Reference to the metadata of the source |

---

### Table: DataVerificator

Description: This table stores information about data verificators.

| Field           | Type     | Description           |
|-----------------|----------|-----------------------|
| verificator_id  | int      | Unique identifier for the verificator |
| name            | string   | Name of the verificator |
| description     | string   | Description of the verificator |
| contact_id      | int      | Reference to the contact information of the verificator |
| address_id      | int      | Reference to the address of the verificator |

---

### Table: ManufacturingFacility

Description: This table stores information about manufacturing facilities.

| Field         | Type     | Description           |
|---------------|----------|-----------------------|
| facility_id   | int      | Unique identifier for the facility |
| resource_id   | int      | Reference to the distributed resource |
| name          | string   | Name of the facility |
| description   | string   | Description of the facility |
| type          | string   | Type of the facility |
| capacity      | int      | Capacity of the facility |
| capabilities  | string   | Capabilities of the facility |
| source_id     | int      | Reference to the metadata of the source |

---

### Table: ManufacturingEquipment

Description: This table stores information about manufacturing equipment.

| Field         | Type     | Description           |
|---------------|----------|-----------------------|
| equipment_id  | int      | Unique identifier for the equipment |
| resource_id   | int      | Reference to the distributed resource |
| brand         | string   | Brand of the equipment |
| model         | string   | Model of the equipment |
| type          | string   | Type of the equipment |
| description   | string   | Description of the equipment |
| source_id     | int      | Reference to the metadata of the source |

---

### Table: ManufacturingService

Description: This table stores information about manufacturing services.

| Field       | Type     | Description           |
|-------------|----------|-----------------------|
| service_id  | int      | Unique identifier for the service |
| resource_id | int      | Reference to the distributed resource |
| type        | string   | Type of the service |
| description | string   | Description of the service |
| source_id   | int      | Reference to the metadata of the source |

---

### Table: ManufacturingSkill

Description: This table stores information about manufacturing skills.

| Field      | Type     | Description           |
|------------|----------|-----------------------|
| skill_id   | int      | Unique identifier for the skill |
| resource_id| int      | Reference to the distributed resource |
| name       | string   | Name of the skill |
| bio        | string   | Biography of the skill |
| skills     | string   | Skills associated with the skill |
| source_id  | int      | Reference to the metadata of the source |

---

### Table: FindableProject

Description: This table stores information about findable projects.

| Field        | Type     | Description           |
|--------------|----------|-----------------------|
| project_id   | int      | Unique identifier for the project |
| resource_id  | int      | Reference to the distributed resource |
| name         | string   | Name of the project |
| description  | string   | Description of the project |
| source_id    | int      | Reference to the metadata of the source |

For contributions please reach out to @iop-alliance in Github.