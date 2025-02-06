-- SQLite

-- UPDATE backup_folder
-- SET status = 1  -- Set the status to '2' (added_folder)
-- WHERE id = 5;   -- Update the row where the id is 1


-- ALTER TABLE backup_folder
-- ADD COLUMN category_index INTEGER;

-- UPDATE backup_folder
-- SET category_index = 1  -- Set the status to '2' (added_folder)
-- WHERE id = 5;   -- Update the row where the id is 1


-- ALTER TABLE available_coin_sets
-- ADD COLUMN category_index INTEGER;

-- UPDATE available_coin_sets
-- SET category_index = 1  -- Set the status to '2' (added_folder)
-- WHERE set_number = 5;   -- Update the row where the id is 1

-- INSERT INTO backup_folder (
--     ticker, 
--     set_number, 
--     contract_address, 
--     searched_from_date_time, 
--     searched_to_date_time, 
--     from_signature, 
--     to_signature, 
--     from_block_timestamp, 
--     to_block_timestamp, 
--     low_value, 
--     peak_value, 
--     description, 
--     priority, 
--     txns, 
--     file_name, 
--     category_index, 
--     status
-- ) 
-- VALUES (
--     'NEUR',              -- ticker
--     6,                  -- set_number
--     '3N2ETvNpPNAxhcaXgkhKoY1yDnQfs41Wnxsx5qNJpump',  -- contract_address
--     '2024-12-23T21:00:00.000Z',          -- searched_from_date_time
--     '2024-12-23T21:20:00.000Z',          -- searched_to_date_time
--     '3NBsoGPhakyrdB4GDbdCVdQVo7M31EoFZCXtSy8wTEUYNNHvzLL4sQUUyvwJC3A2ZjaF3ydM4dNSoUWjQnYSi8z5',         -- from_signature
--     '3Jamwcvo6z5nSMDb7TdBztb5i5UTfETtchq4cKd46DQ8tqf7tXuPSeBbSVu3Mh3BQrV8XCTSvufWHmEkAn3QzZKN',           -- to_signature
--     '2024-12-23T21:05:19.000Z',          -- from_block_timestamp
--     '2024-12-23T21:19:59.000Z',          -- to_block_timestamp
--     1,                         -- low_value
--     60,                         -- peak_value
--     'pumpfun bonding',      -- description
--     'buy',                            -- priority
--     10626,                              -- txns
--     '3N2ETvNpPNAxhcaXgkhKoY1yDnQfs41Wnxsx5qNJpump_2024-12-23T21:05:19.000Z_to_2024-12-23T21:19:59.000Z.json',             -- file_name
--     0,                               -- category_index (0 - PumpfunBonding Gained Coin)
--     1                                -- status (example: 1 for active, or any status code)
-- );
