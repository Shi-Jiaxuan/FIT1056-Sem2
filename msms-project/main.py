# main.py - The View Layer
from app.schedule import ScheduleManager

print(" Imports worked!")

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    daily_lessons = manager.get_daily_lessons(day)
    print(f"\n--- Daily Roster for {day} ---")
    if not daily_lessons:
        print("No lessons scheduled for this day.")
        return
    # Notice: This code does not need to change. It doesn't care where the Course class lives.
    # It only talks to the manager.
    # TODO: Call a method on the manager to get the day's lessons and print them.
    for i, lesson in enumerate(daily_lessons, 1):
        print(f"\nLesson {i}:")
        print(f"  Course: {lesson['course_name']} ({lesson['instrument']})")
        print(f"  Teacher: {lesson['teacher']}")
        print(f"  Time: {lesson['time']}")
        print(f"  Students: {', '.join(lesson['students']) if lesson['students'] else 'None'}")


def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager()  # Create ONE instance of the application brain.

    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        # TODO: Create a menu for the new PST3 functions.
        # Get user input and call the appropriate view function, passing 'manager' to it.
        print("1. View daily roster")
        print("2. Student check-in")
        print("3. Switch course")
        print("Q. Quit")
        choice = input("Enter choice: ")
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)
        elif choice == '2':
            sid = int(input("Enter student ID: "))
            cid = int(input("Enter course ID: "))
            manager.check_in(sid, cid)
        elif choice == '3':
            sid = int(input("Enter student ID: "))
            from_cid = int(input("Enter course ID to leave: "))
            to_cid = int(input("Enter course ID to join: "))
            manager.switch_course(sid, from_cid, to_cid)
        elif choice.lower() == 'q':
            break
        else:
            print("Error: Invalid choice.")


if __name__ == "__main__":
    main()