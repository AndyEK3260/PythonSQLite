SELECT
    f.FlightNumber,
    a.AirportCode AS Destination,
    a.City,
    s.StatusName,
    f.DepartureTime
FROM FLIGHT f
JOIN AIRPORT a
    ON f.DestAirportID = a.AirportID
JOIN STATUS s
    ON f.StatusID = s.StatusID
WHERE a.AirportCode = 'JFK';

SELECT
    f.FlightNumber,
    s.StatusName,
    f.DepartureTime
FROM FLIGHT f
JOIN STATUS s
    ON f.StatusID = s.StatusID
WHERE s.StatusName = 'Scheduled';

SELECT
    FlightNumber,
    DepartureTime,
    ArrivalTime
FROM FLIGHT
WHERE date(DepartureTime) = '2026-10-01';