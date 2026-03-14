def get_doctors(location):

    doctors = {
        "hyderabad": [
            {"name": "Dr. Ramesh", "hospital": "Apollo Hospital"},
            {"name": "Dr. Priya", "hospital": "Yashoda Hospital"}
        ],
        "chennai": [
            {"name": "Dr. Kumar", "hospital": "MIOT Hospital"}
        ]
    }

    return doctors.get(location.lower(), [])