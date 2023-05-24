CREATE OR REPLACE TABLE votingadaproject.party_member
(
  id INTEGER NOT NULL,
  first_name STRING NOT NULL,
  last_name STRING NOT NULL,
  status STRING NOT NULL,
  uuid STRING NOT NULL,
  party_id INTEGER NOT NULL
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
) AS
SELECT *
FROM dataset.table