-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports  -- crime raports from from this day on this street
   ...> WHERE day=28 AND month=7 AND
   ...> street LIKE '%Humphrey Street%';

SELECT * FROM interviews  -- interviews of 3 witnesses from crime place
   ...> WHERE day=28 AND month=7 AND transcript LIKE '%bakery%';

SELECT * FROM bakery_security_logs -- checking security logs within 10 minutes when crime happened to see who got away
   ...> WHERE month=7 AND day=28 AND hour=10 AND minute <= 25 and minute >= 15 AND activity='exit';

SELECT * FROM people  -- checking the people who left bakery within 10 minutes
   ...> WHERE license_plate='4328GD8';

SELECT * FROM people
   ...> WHERE license_plate='G412CB7';

--etc...

-- 10:16 license_plate: 5P2BI95 - name: -nevermind, clear
-- 10:18 license_plate: 94KL13X - name: Bruce , id: 686048 - sus
-- 10:18 license_plate: 6P58WS2 - name: - nevermind - clear
-- 10:19 license_plate: 4328GD8 - name: Luca , id: 467400 -sus
-- 10:20 license_plate: G412CB7 - name: Sofia , id: 398010 -clear
-- 10:21 license_plate: L93JTIZ - name: Iman , id: 396669 -sus
-- 10:23 license_plate: 322W7JE - name: Diana , id: 514354 -sus
-- 10:23 license_plate: 0NTHK55 - name: Kelsey , id: 560886 -clear

SELECT * FROM atm_transactions -- to see account numbers of people withdrawing money this day as witness 2 said
   ...> WHERE month=7 AND day=28 AND transaction_type='withdraw' AND atm_location='Leggett Street';

--account_numbers:
--| 28500762       |
--| 28296815       |
--| 76054385       |
--| 49610011       |
--| 16153065       |
--| 25506511       |
--| 81061156       |
--| 26013199       |

SELECT * FROM people -- after next research :
   ...> JOIN bank_accounts ON people.id=bank_accounts.person_id
   ...> WHERE people.license_plate IN
   ...> (SELECT license_plate FROM bakery_security_logs WHERE month=7 AND day=28 AND hour=10 and activity='exit')
   ...> AND bank_accounts.account_number IN
   ...> (SELECT account_number  FROM atm_transactions
   ...> WHERE month=7 AND day=28 AND transaction_type='withdraw' AND atm_location='Leggett Street');

-- main suspects are:
-- 10:18 license_plate: 94KL13X - name: Bruce , id: 686048 - sus
-- 10:19 license_plate: 4328GD8 - name: Luca , id: 467400 -sus
-- 10:21 license_plate: L93JTIZ - name: Iman , id: 396669 -sus
-- 10:23 license_plate: 322W7JE - name: Diana , id: 514354 -sus

SELECT * FROM people
   ...> JOIN bank_accounts ON people.id=bank_accounts.person_id
   ...> WHERE people.license_plate IN
   ...> (SELECT license_plate FROM bakery_security_logs WHERE month=7 AND day=28 AND hour=10 and activity='exit')
   ...> AND bank_accounts.account_number IN
   ...> (SELECT account_number  FROM atm_transactions
   ...> WHERE month=7 AND day=28 AND transaction_type='withdraw' AND atm_location='Leggett Street')
   ...> AND phone_number IN
   ...> (SELECT caller FROM phone_calls WHERE month=7 AND day=28 and duration<=60);

   -- MAIN SUSPECTs:
   -- Diana id: 514354, phone_number=(770) 555-1861, passport_number=3592750733
   -- Bruce id: 686048, phone_number=(367) 555-5533, passport_number=5773159633

-- checking id of Fiftyville airport, id=8
SELECT *  FROM airports where city='Fiftyville';

-- finding earliest flight from Fiftyville tomorrow:
SELECT * FROM flights
   ...> WHERE origin_airport_id=8
   ...> AND day=29 AND month=7
   ...> ORDER BY hour ASC, minute ASC
   ...> LIMIT 1;

-- flight from Fiftyville (id=8) to New York City(id=4) , flight id=36

SELECT * FROM people -- finally found out who the thief was
   ...> JOIN bank_accounts ON people.id=bank_accounts.person_id
   ...> WHERE people.license_plate IN
   ...> (SELECT license_plate FROM bakery_security_logs WHERE month=7 AND day=28 AND hour=10 and activity='exit')
   ...> AND bank_accounts.account_number IN
   ...> (SELECT account_number  FROM atm_transactions
   ...> WHERE month=7 AND day=28 AND transaction_type='withdraw' AND atm_location='Leggett Street')
   ...> AND phone_number IN
   ...> (SELECT caller FROM phone_calls WHERE month=7 AND day=28 and duration<=60)
   ...> AND people.passport_number IN
   ...> (SELECT passport_number FROM passengers WHERE flight_id=36);

-- thief: Bruce pphone_number = (367) 555-5533
-- they wanted to escape to New York City

SELECT * FROM people --finding out to who thief telephoned
   ...> WHERE phone_number IN
   ...> (SELECT receiver FROM phone_calls WHERE month=7 AND day=28 and duration<=60 AND caller='(367) 555-5533');

-- helper: Robin
