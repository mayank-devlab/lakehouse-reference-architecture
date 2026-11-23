CREATE SCHEMA IF NOT EXISTS workspace.governance;

-- Column mask: raw ID for privileged groups, stable hash for everyone else
CREATE OR REPLACE FUNCTION workspace.governance.mask_id(v STRING)
RETURN CASE
  WHEN is_account_group_member('shopnova_engineers')
    OR is_account_group_member('shopnova_compliance') THEN v
  ELSE CONCAT('id_', SUBSTRING(SHA2(v, 256), 1, 12))
END;

-- Column mask: coarsen the zip prefix for everyone except privileged groups
CREATE OR REPLACE FUNCTION workspace.governance.mask_zip(v STRING)
RETURN CASE
  WHEN is_account_group_member('shopnova_engineers')
    OR is_account_group_member('shopnova_compliance') THEN v
  ELSE CONCAT(SUBSTRING(v, 1, 2), '***')
END;

-- Row filter: regional analysts see only the state of SP
CREATE OR REPLACE FUNCTION workspace.governance.state_filter(state STRING)
RETURN NOT is_account_group_member('shopnova_analysts_sp') OR state = 'SP';
