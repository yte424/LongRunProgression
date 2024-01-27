from datetime import datetime, timedelta

def calculate_weeks_between_dates(start_date, end_date):
    """
    Calculate the number of weeks between two dates.
    """
    return (end_date - start_date).days // 7

def create_training_week(date, long_run_distance, is_rest_week, weekly_increase):
    """
    Create a dictionary representing a training week.
    """
    if is_rest_week:
        return {
            "Datum": date.strftime("%Y-%m-%d"),
            "Langer Lauf (km)": long_run_distance * 0.5,
            "Dienstag Lauf (km)": 5,
            "Donnerstag Lauf (km)": 5,
            "Gesamtwochenkilometer": long_run_distance * 0.5 + 10
        }
    else:
        return {
            "Datum": date.strftime("%Y-%m-%d"),
            "Langer Lauf (km)": long_run_distance,
            "Dienstag Lauf (km)": 10,
            "Donnerstag Lauf (km)": 10,
            "Gesamtwochenkilometer": long_run_distance + 20
        }

def generate_training_plan(start_date, end_date, start_distance, increase, rest_interval):
    """
    Generate a training plan between two dates.
    """
    total_weeks = calculate_weeks_between_dates(start_date, end_date)
    training_plan = []
    long_run_distance = start_distance

    for week in range(total_weeks):
        is_rest_week = (week + 1) % rest_interval == 0
        training_week = create_training_week(start_date, long_run_distance, is_rest_week, increase)
        training_plan.append(training_week)
        start_date += timedelta(weeks=1)
        if not is_rest_week:
            long_run_distance += increase

    return training_plan

def limit_long_runs(training_plan, max_distance):
    """
    Limit the long runs in the training plan to a maximum distance.
    """
    for week in training_plan:
        if week["Langer Lauf (km)"] > max_distance:
            week["Langer Lauf (km)"] = max_distance

def training_plan_to_markdown(training_plan):
    """
    Convert the training plan into a Markdown formatted table.
    """
    headers = "| Woche Beginnend am | Langer Lauf (km) | Dienstag Lauf (km) | Donnerstag Lauf (km) | Gesamtwochenkilometer |\n"
    separator = "|--------------------|------------------|--------------------|----------------------|-----------------------|\n"
    rows = [headers, separator]
    for week in training_plan:
        rows.append("| {Datum} | {Langer Lauf (km)} | {Dienstag Lauf (km)} | {Donnerstag Lauf (km)} | {Gesamtwochenkilometer} |\n".format(**week))
    return ''.join(rows)

# Definierung der Daten
start_date = datetime(2024, 1, 8)
end_date = datetime(2024, 3, 25)

# Generierung des Trainingsplans
training_plan = generate_training_plan(start_date, end_date, 17, 2, 4)
limit_long_runs(training_plan, 35)

# Ausgabe des Trainingsplans in Markdown
print(training_plan_to_markdown(training_plan))
