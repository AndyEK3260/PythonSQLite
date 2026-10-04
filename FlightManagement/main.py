from database import get_connection

# ============================================================
# 1. ADD A NEW FLIGHT
# ============================================================

def add_flight():
    print("\n--- Add New Flight ---")

    flight_number = input("Flight number: ").strip()

    if not flight_number:
        print("Flight number cannot be empty.")
        return

    origin_code = input("Origin airport code: ").strip().upper()
    destination_code = input("Destination airport code: ").strip().upper()

    pilot_input = input(
        "Pilot ID (press Enter if unassigned): "
    ).strip()

    status_input = input("Status ID: ").strip()
    departure_time = input(
        "Departure time (YYYY-MM-DD HH:MM): "
    ).strip()
    arrival_time = input(
        "Arrival time (YYYY-MM-DD HH:MM): "
    ).strip()

    # Convert optional pilot ID
    pilot_id = None

    if pilot_input:
        try:
            pilot_id = int(pilot_input)
        except ValueError:
            print("Invalid Pilot ID.")
            return

    # Convert status ID
    try:
        status_id = int(status_input)
    except ValueError:
        print("Invalid Status ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Find origin airport
        cursor.execute(
            """
            SELECT AirportID
            FROM AIRPORT
            WHERE AirportCode = ?
            """,
            (origin_code,)
        )

        origin = cursor.fetchone()

        if origin is None:
            print(f"Origin airport '{origin_code}' does not exist.")
            return

        origin_id = origin[0]

        # Find destination airport
        cursor.execute(
            """
            SELECT AirportID
            FROM AIRPORT
            WHERE AirportCode = ?
            """,
            (destination_code,)
        )

        destination = cursor.fetchone()

        if destination is None:
            print(
                f"Destination airport "
                f"'{destination_code}' does not exist."
            )
            return

        destination_id = destination[0]

        # Check pilot if provided
        if pilot_id is not None:
            cursor.execute(
                """
                SELECT PilotID
                FROM PILOT
                WHERE PilotID = ?
                """,
                (pilot_id,)
            )

            if cursor.fetchone() is None:
                print("Pilot does not exist.")
                return

        # Check status
        cursor.execute(
            """
            SELECT StatusID
            FROM STATUS
            WHERE StatusID = ?
            """,
            (status_id,)
        )

        if cursor.fetchone() is None:
            print("Status does not exist.")
            return

        # Insert flight
        cursor.execute(
            """
            INSERT INTO FLIGHT (
                FlightNumber,
                OriginAirportID,
                DestAirportID,
                PilotID,
                StatusID,
                DepartureTime,
                ArrivalTime
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                flight_number,
                origin_id,
                destination_id,
                pilot_id,
                status_id,
                departure_time,
                arrival_time
            )
        )

        conn.commit()

        print("Flight added successfully.")

    except sqlite3.IntegrityError as error:
        print(f"Unable to add flight: {error}")

    finally:
        conn.close()


# ============================================================
# 2. VIEW FLIGHTS BY CRITERIA
# ============================================================

def view_flights():
    print("\n--- View Flights ---")

    print("1. By destination")
    print("2. By status")
    print("3. By departure date")
    print("4. View all flights")

    choice = input("Choose search criteria: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if choice == "1":

            destination = input(
                "Enter destination airport code: "
            ).strip().upper()

            cursor.execute(
                """
                SELECT
                    f.FlightID,
                    f.FlightNumber,
                    origin.AirportCode,
                    destination.AirportCode,
                    s.StatusName,
                    f.DepartureTime,
                    f.ArrivalTime
                FROM FLIGHT f
                JOIN AIRPORT origin
                    ON f.OriginAirportID = origin.AirportID
                JOIN AIRPORT destination
                    ON f.DestAirportID = destination.AirportID
                JOIN STATUS s
                    ON f.StatusID = s.StatusID
                WHERE destination.AirportCode = ?
                ORDER BY f.DepartureTime
                """,
                (destination,)
            )

        elif choice == "2":

            status = input("Enter status: ").strip()

            cursor.execute(
                """
                SELECT
                    f.FlightID,
                    f.FlightNumber,
                    origin.AirportCode,
                    destination.AirportCode,
                    s.StatusName,
                    f.DepartureTime,
                    f.ArrivalTime
                FROM FLIGHT f
                JOIN AIRPORT origin
                    ON f.OriginAirportID = origin.AirportID
                JOIN AIRPORT destination
                    ON f.DestAirportID = destination.AirportID
                JOIN STATUS s
                    ON f.StatusID = s.StatusID
                WHERE s.StatusName = ?
                ORDER BY f.DepartureTime
                """,
                (status,)
            )

        elif choice == "3":

            date = input(
                "Enter departure date (YYYY-MM-DD): "
            ).strip()

            cursor.execute(
                """
                SELECT
                    f.FlightID,
                    f.FlightNumber,
                    origin.AirportCode,
                    destination.AirportCode,
                    s.StatusName,
                    f.DepartureTime,
                    f.ArrivalTime
                FROM FLIGHT f
                JOIN AIRPORT origin
                    ON f.OriginAirportID = origin.AirportID
                JOIN AIRPORT destination
                    ON f.DestAirportID = destination.AirportID
                JOIN STATUS s
                    ON f.StatusID = s.StatusID
                WHERE date(f.DepartureTime) = ?
                ORDER BY f.DepartureTime
                """,
                (date,)
            )

        elif choice == "4":

            cursor.execute(
                """
                SELECT
                    f.FlightID,
                    f.FlightNumber,
                    origin.AirportCode,
                    destination.AirportCode,
                    s.StatusName,
                    f.DepartureTime,
                    f.ArrivalTime
                FROM FLIGHT f
                JOIN AIRPORT origin
                    ON f.OriginAirportID = origin.AirportID
                JOIN AIRPORT destination
                    ON f.DestAirportID = destination.AirportID
                JOIN STATUS s
                    ON f.StatusID = s.StatusID
                ORDER BY f.DepartureTime
                """
            )

        else:
            print("Invalid option.")
            return

        flights = cursor.fetchall()

        if not flights:
            print("No flights found.")
            return

        print(
            "\nID | Flight | Origin | Destination | "
            "Status | Departure | Arrival"
        )

        print("-" * 100)

        for flight in flights:
            print(
                f"{flight[0]} | "
                f"{flight[1]} | "
                f"{flight[2]} | "
                f"{flight[3]} | "
                f"{flight[4]} | "
                f"{flight[5]} | "
                f"{flight[6]}"
            )

    finally:
        conn.close()


# ============================================================
# 3. UPDATE FLIGHT INFORMATION
# ============================================================

def update_flight():
    print("\n--- Update Flight Information ---")

    flight_input = input("Enter Flight ID: ").strip()

    try:
        flight_id = int(flight_input)
    except ValueError:
        print("Invalid Flight ID.")
        return

    print("\n1. Change departure time")
    print("2. Change arrival time")
    print("3. Change status")

    choice = input("Choose what to update: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Check whether flight exists
        cursor.execute(
            """
            SELECT FlightNumber
            FROM FLIGHT
            WHERE FlightID = ?
            """,
            (flight_id,)
        )

        flight = cursor.fetchone()

        if flight is None:
            print("Flight not found.")
            return

        if choice == "1":

            new_time = input(
                "New departure time (YYYY-MM-DD HH:MM): "
            ).strip()

            cursor.execute(
                """
                UPDATE FLIGHT
                SET DepartureTime = ?
                WHERE FlightID = ?
                """,
                (new_time, flight_id)
            )

        elif choice == "2":

            new_time = input(
                "New arrival time (YYYY-MM-DD HH:MM): "
            ).strip()

            cursor.execute(
                """
                UPDATE FLIGHT
                SET ArrivalTime = ?
                WHERE FlightID = ?
                """,
                (new_time, flight_id)
            )

        elif choice == "3":

            new_status = input("New Status ID: ").strip()

            try:
                new_status = int(new_status)
            except ValueError:
                print("Invalid Status ID.")
                return

            cursor.execute(
                """
                SELECT StatusID
                FROM STATUS
                WHERE StatusID = ?
                """,
                (new_status,)
            )

            if cursor.fetchone() is None:
                print("Status does not exist.")
                return

            cursor.execute(
                """
                UPDATE FLIGHT
                SET StatusID = ?
                WHERE FlightID = ?
                """,
                (new_status, flight_id)
            )

        else:
            print("Invalid option.")
            return

        conn.commit()

        print("Flight updated successfully.")

    finally:
        conn.close()


# ============================================================
# 4. ASSIGN PILOT TO FLIGHT
# ============================================================

def assign_pilot():
    print("\n--- Assign Pilot to Flight ---")

    flight_input = input("Enter Flight ID: ").strip()
    pilot_input = input("Enter Pilot ID: ").strip()

    try:
        flight_id = int(flight_input)
        pilot_id = int(pilot_input)
    except ValueError:
        print("Flight ID and Pilot ID must be numbers.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Check flight
        cursor.execute(
            """
            SELECT FlightNumber
            FROM FLIGHT
            WHERE FlightID = ?
            """,
            (flight_id,)
        )

        flight = cursor.fetchone()

        if flight is None:
            print("Flight not found.")
            return

        # Check pilot
        cursor.execute(
            """
            SELECT FullName
            FROM PILOT
            WHERE PilotID = ?
            """,
            (pilot_id,)
        )

        pilot = cursor.fetchone()

        if pilot is None:
            print("Pilot not found.")
            return

        # Assign pilot
        cursor.execute(
            """
            UPDATE FLIGHT
            SET PilotID = ?
            WHERE FlightID = ?
            """,
            (pilot_id, flight_id)
        )

        conn.commit()

        print(
            f"Pilot {pilot[0]} successfully assigned "
            f"to flight {flight[0]}."
        )

    finally:
        conn.close()


# ============================================================
# 5. VIEW PILOT SCHEDULE
# ============================================================

def view_pilot_schedule():
    print("\n--- View Pilot Schedule ---")

    pilot_input = input("Enter Pilot ID: ").strip()

    try:
        pilot_id = int(pilot_input)
    except ValueError:
        print("Invalid Pilot ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Get pilot name
        cursor.execute(
            """
            SELECT FullName
            FROM PILOT
            WHERE PilotID = ?
            """,
            (pilot_id,)
        )

        pilot = cursor.fetchone()

        if pilot is None:
            print("Pilot not found.")
            return

        print(f"\nPilot: {pilot[0]}")

        cursor.execute(
            """
            SELECT
                f.FlightNumber,
                origin.AirportCode,
                destination.AirportCode,
                s.StatusName,
                f.DepartureTime,
                f.ArrivalTime
            FROM FLIGHT f
            JOIN AIRPORT origin
                ON f.OriginAirportID = origin.AirportID
            JOIN AIRPORT destination
                ON f.DestAirportID = destination.AirportID
            JOIN STATUS s
                ON f.StatusID = s.StatusID
            WHERE f.PilotID = ?
            ORDER BY f.DepartureTime
            """,
            (pilot_id,)
        )

        flights = cursor.fetchall()

        if not flights:
            print("No flights assigned to this pilot.")
            return

        print(
            "\nFlight | Origin | Destination | "
            "Status | Departure | Arrival"
        )

        print("-" * 90)

        for flight in flights:
            print(
                f"{flight[0]} | "
                f"{flight[1]} | "
                f"{flight[2]} | "
                f"{flight[3]} | "
                f"{flight[4]} | "
                f"{flight[5]}"
            )

    finally:
        conn.close()


# ============================================================
# 6. DESTINATION MANAGEMENT
# ============================================================

def manage_destinations():
    while True:

        print("\n--- Destination Management ---")
        print("1. View destinations")
        print("2. Update destination")
        print("0. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_destinations()

        elif choice == "2":
            update_destination()

        elif choice == "0":
            break

        else:
            print("Invalid option.")


def view_destinations():
    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                AirportID,
                AirportCode,
                City,
                Country
            FROM AIRPORT
            ORDER BY AirportCode
            """
        )

        airports = cursor.fetchall()

        print("\nID | Code | City | Country")
        print("-" * 50)

        for airport in airports:
            print(
                f"{airport[0]} | "
                f"{airport[1]} | "
                f"{airport[2]} | "
                f"{airport[3]}"
            )

    finally:
        conn.close()


def update_destination():
    print("\n--- Update Destination ---")

    airport_code = input(
        "Enter airport code: "
    ).strip().upper()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT AirportID, City, Country
            FROM AIRPORT
            WHERE AirportCode = ?
            """,
            (airport_code,)
        )

        airport = cursor.fetchone()

        if airport is None:
            print("Airport not found.")
            return

        print(
            f"Current city: {airport[1]}"
        )

        print(
            f"Current country: {airport[2]}"
        )

        new_city = input(
            "New city: "
        ).strip()

        new_country = input(
            "New country: "
        ).strip()

        if not new_city or not new_country:
            print("City and country cannot be empty.")
            return

        cursor.execute(
            """
            UPDATE AIRPORT
            SET City = ?, Country = ?
            WHERE AirportCode = ?
            """,
            (new_city, new_country, airport_code)
        )

        conn.commit()

        print("Destination updated successfully.")

    finally:
        conn.close()


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():

    while True:

        print("\n================================")
        print("   FLIGHT MANAGEMENT SYSTEM")
        print("================================")

        print("1. Add New Flight")
        print("2. View Flights by Criteria")
        print("3. Update Flight Information")
        print("4. Assign Pilot to Flight")
        print("5. View Pilot Schedule")
        print("6. View/Update Destination Information")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_flight()

        elif choice == "2":
            view_flights()

        elif choice == "3":
            update_flight()

        elif choice == "4":
            assign_pilot()

        elif choice == "5":
            view_pilot_schedule()

        elif choice == "6":
            manage_destinations()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()