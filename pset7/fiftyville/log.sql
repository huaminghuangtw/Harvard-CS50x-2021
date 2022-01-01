-- Keep a log of any SQL queries you execute as you solve the mystery

-- Step 1: Find the id and description of the theft
SELECT id, description FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28 AND street = "Chamberlin Street";

-- Step 2: Find more clues from the transcripts of interviews on July 28, 2020
SELECT id, name, transcript FROM interviews WHERE year = 2020 AND month = 7 AND day = 28 AND transcript LIKE "%courthouse%";

-- Step 3: Utilize information we have to find:

-- 1) Who the thief is
SELECT name FROM
WHERE
id IN
(
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN
    (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"
    )
)
AND
license_plate IN
(
    SELECT license_plate
    FROM courthouse_security_logs
    WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25
)
AND
phone_number IN
(
    SELECT caller
    FROM phone_calls
    WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60
)
AND
passport_number IN
(
    SELECT passport_number
    FROM passengers
    WHERE flight_id =
    (
        SELECT id
        FROM flights
        WHERE year = 2020 AND month = 7 AND day = 29 AND origin_airport_id =
        (
            SELECT id
            FROM airports
            WHERE city = "Fiftyville"
        )
        ORDER BY hour, minute
        LIMIT 1
    )
);

-- 2) What city the thief escaped to
SELECT city FROM airports
WHERE id IN
(
    SELECT destination_airport_id
    FROM flights
    WHERE year = 2020 AND month = 7 AND day = 29 AND origin_airport_id =
    (
        SELECT id
        FROM airports
        WHERE city = "Fiftyville"
    )
    ORDER BY hour, minute
    LIMIT 1
);


-- 3) Who the thief’s accomplice is who helped them escape
SELECT name FROM people
WHERE
name != "Ernest"
AND
phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60 AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE name = "Ernest"
    )
);