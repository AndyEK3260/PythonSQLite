INSERT INTO STATUS (StatusID, StatusName) VALUES
(1, 'Scheduled'),
(2, 'Boarding'),
(3, 'Departed'),
(4, 'In Transit'),
(5, 'Arrived'),
(6, 'Delayed'),
(7, 'Cancelled'),
(8, 'Completed'),
(9, 'Diverted'),
(10, 'Maintenance');

INSERT INTO AIRPORT (AirportID, AirportCode, City, Country) VALUES
(1, 'LHR', 'London', 'United Kingdom'),
(2, 'JFK', 'New York', 'United States'),
(3, 'LAX', 'Los Angeles', 'United States'),
(4, 'CDG', 'Paris', 'France'),
(5, 'NRT', 'Tokyo', 'Japan'),
(6, 'SIN', 'Singapore', 'Singapore'),
(7, 'SYD', 'Sydney', 'Australia'),
(8, 'DXB', 'Dubai', 'United Arab Emirates'),
(9, 'HKG', 'Hong Kong', 'Hong Kong'),
(10, 'FRA', 'Frankfurt', 'Germany');

INSERT INTO PILOT
(PilotID, FullName, LicenseNumber, HireDate)
VALUES
(1, 'James Smith', 'LIC001', '2018-03-15'),
(2, 'Emily Johnson', 'LIC002', '2019-06-20'),
(3, 'Michael Brown', 'LIC003', '2017-01-10'),
(4, 'Sarah Davis', 'LIC004', '2020-09-01'),
(5, 'Daniel Wilson', 'LIC005', '2016-11-25'),
(6, 'Laura Taylor', 'LIC006', '2021-04-12'),
(7, 'Robert Anderson', 'LIC007', '2018-08-30'),
(8, 'Anna Thomas', 'LIC008', '2022-02-18'),
(9, 'David Moore', 'LIC009', '2019-12-05'),
(10, 'Sophia Martin', 'LIC010', '2020-07-22');

INSERT INTO FLIGHT
(FlightID, FlightNumber, OriginAirportID, DestAirportID,
 PilotID, StatusID, DepartureTime, ArrivalTime)
VALUES
(1, 'BA101', 1, 2, 1, 1, '2026-10-01 08:00', '2026-10-01 11:00'),
(2, 'BA202', 1, 4, 2, 1, '2026-10-01 09:30', '2026-10-01 12:00'),
(3, 'AA301', 2, 3, 3, 1, '2026-10-01 10:00', '2026-10-01 13:30'),
(4, 'JL401', 5, 6, 4, 2, '2026-10-01 11:00', '2026-10-01 17:00'),
(5, 'SQ501', 6, 7, 5, 1, '2026-10-02 07:00', '2026-10-02 15:00'),
(6, 'EK601', 8, 1, NULL, 6, '2026-10-02 12:00', '2026-10-02 17:00'),
(7, 'CX701', 9, 5, 6, 3, '2026-10-02 14:00', '2026-10-02 20:00'),
(8, 'LH801', 10, 8, 7, 1, '2026-10-03 06:30', '2026-10-03 13:00'),
(9, 'BA102', 1, 5, 8, 1, '2026-10-03 09:00', '2026-10-04 07:00'),
(10, 'AA302', 2, 1, 9, 7, '2026-10-03 15:00', '2026-10-04 04:00');