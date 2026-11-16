# --- Text (string) ---
first_name = "Hasnaad"
city = "London"

# --- Whole number (integer) ---
years_experience = 19

# --- Decimal number (float) ---
day_rate = 450.50

# --- True / False (boolean) ---
is_sc_eligible = True

# --- List: several values in order ---
skills = ["VBA", "SQL", "Python"]

# --- Dictionary: labelled values, like a lookup ---
course = {"provider": "ITC", "weeks": 9}

# Use the variables
print(f"My Name is: {first_name} and I am from {city}")
print(f"Experience: {years_experience} years")
print(f"Day rate: £{day_rate}")
print(f"SC eligible: {is_sc_eligible}")
print(f"Skills: {skills}")
print(f"First skill: {skills[0]}")
print(f"Course: {course['provider']} for {course['weeks']} weeks")

# Change a variable
years_experience = years_experience + 1
skills.append("Pandas")
print(f"Next year: {years_experience} years, skills: {skills}")

# See what type each variable is
print(type(first_name), type(years_experience), type(day_rate), type(is_sc_eligible))