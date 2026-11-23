-- Analysts: Gold only
GRANT USE CATALOG ON CATALOG workspace TO `shopnova_analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA workspace.gold TO `shopnova_analysts`;
GRANT USE CATALOG ON CATALOG workspace TO `shopnova_analysts_sp`;
GRANT USE SCHEMA, SELECT ON SCHEMA workspace.gold TO `shopnova_analysts_sp`;

-- Data scientists: Silver and Gold (masked identifiers)
GRANT USE CATALOG ON CATALOG workspace TO `shopnova_data_scientists`;
GRANT USE SCHEMA, SELECT ON SCHEMA workspace.silver TO `shopnova_data_scientists`;
GRANT USE SCHEMA, SELECT ON SCHEMA workspace.gold TO `shopnova_data_scientists`;

-- Compliance: read everything, unmasked
GRANT USE CATALOG ON CATALOG workspace TO `shopnova_compliance`;
GRANT USE SCHEMA, SELECT ON SCHEMA workspace.bronze TO `shopnova_compliance`;
GRANT USE SCHEMA, SELECT ON SCHEMA workspace.silver TO `shopnova_compliance`;
GRANT USE SCHEMA, SELECT ON SCHEMA workspace.gold TO `shopnova_compliance`;

-- Engineers: build and operate the pipeline layers and landing zone
GRANT USE CATALOG ON CATALOG workspace TO `shopnova_engineers`;
GRANT ALL PRIVILEGES ON SCHEMA workspace.bronze TO `shopnova_engineers`;
GRANT ALL PRIVILEGES ON SCHEMA workspace.silver TO `shopnova_engineers`;
GRANT ALL PRIVILEGES ON SCHEMA workspace.gold TO `shopnova_engineers`;
GRANT READ VOLUME, WRITE VOLUME ON VOLUME workspace.landing.raw TO `shopnova_engineers`;
