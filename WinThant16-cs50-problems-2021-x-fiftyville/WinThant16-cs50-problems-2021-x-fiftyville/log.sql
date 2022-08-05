-- Keep a log of any SQL queries you execute as you solve the mystery.
--We have to find the crime scene report firstly
SELECT * FROM crime_scene_reports
WHERE year="2020" AND month ="7" AND day ="28" AND
street="Chamberlin Street";

--What we discovered after checking crime_scene_reports was that it took place at the Chamberlin Street Courthouse.
--there were three witnesses who were present, and all mention courthouse
--It was also discovered that the theft took place at 10:15am
--The next course of action was to check their interview transcripts

SELECT * FROM interviews
WHERE year="2020" AND month="7" AND day="28";

--Reading transcripts we discover interview_ids for three witnesses were 161,162,and 163
--id161 claims the thief left in a car in the courthouse after 10 mins, which is around 10:25am
--id162 claims the thief was withdrawing money at an ATM on Fifer Street earlier in the morning
--id163 claims the thief was talking to someone as he was getting in the car
--it was also mentioned they were taking the earliest flight out of Fiftyville the next day(i.e July 29)

--Checking courthouse security log for thief's car:
SELECT * FROM courthouse_security_logs
WHERE year="2020" AND month="7" AND day="28"
AND hour="10" AND activity="exit";

--Looking at the log, we narrow down the suspect's car to around 9 cars

--Running the license_plates, we can find info about owners of these cars:

SELECT people.id,people.name,people.phone_number,people.passport_number,people.license_plate FROM courthouse_security_logs
JOIN people ON people.license_plate=courthouse_security_logs.license_plate
WHERE (
courthouse_security_logs.year="2020" AND
courthouse_security_logs.month="7" AND
courthouse_security_logs.day="28" AND
courthouse_security_logs.hour="10" AND
courthouse_security_logs.activity="exit");

--AND finding a link with the atm_transactions from Fifer street:
SELECT * FROM atm_transactions
JOIN bank_accounts ON atm_transactions.account_number=bank_accounts.account_number
JOIN people ON people.id=person_id
WHERE
(atm_transactions.year="2020" AND atm_transactions.month="7" AND atm_transactions.day="28"
AND atm_transactions.atm_location="Fifer Street"
AND transaction_type="withdraw");



--we find out the thief is Ernest by comparing the atm_transactions query with the courthouse_security_log, as we find that Ernest was found to have been the guilty one
--now all we need to do is check the call logs of Ernest and find his pesky friend
SELECT * FROM phone_calls 
JOIN people ON people.phone_number=phone_calls.receiver
WHERE
(Caller="(367) 555-5533" AND        --entering Ernest's number as the caller
phone_calls.year="2020" AND
phone_calls.month="7" AND
phone_calls.day="28");

--we find four receivers during that day: Berthold, Deborah, Gregory and Carl.
--However, the witness saidd the duration was less than a minute, which means the accomplice is Berthold
--The last step is to find where they escaped to


--Checking the info of the culprit and accomplice, we find Berthold has no passport num but Ernest does
SELECT * FROM people
WHERE name="Berthold";
SELECT * FROM people
WHERE name="Ernest";


--Finding the flights booked with Ernest's passport number, we see:
SELECT* FROM passengers
JOIN people ON passengers.passport_number=people.passport_number
JOIN flights ON flights.id=passengers.flight_id
JOIN airports ON airports.id=flights.destination_airport_id
WHERE passengers.passport_number =
(SELECT people.passport_number FROM people
WHERE people.name="Ernest");

--After running the query, we find out that the thief has decided to run away to London.