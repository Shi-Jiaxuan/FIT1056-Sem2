import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course


class ScheduleManager:
    """The main controller for all business logic and data handling."""

    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # TODO: Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        # ... (next_id counters) ...
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # TODO: Load students, teachers, and courses as before.
                # ...
                self.students = [StudentUser(s["id"], s["name"]) for s in data.get("students", [])]
                for student, raw in zip(self.students, data.get("students", [])):
                    student.enrolled_course_ids = raw.get("enrolled_course_ids", [])

                self.teachers = [TeacherUser(t["id"], t["name"], t["speciality"])
                                 for t in data.get("teachers", [])]

                self.courses = [Course(c["id"], c["name"], c["instrument"], c["teacher_id"])
                                for c in data.get("courses", [])]
                for course, raw in zip(self.courses, data.get("courses", [])):
                    course.enrolled_student_ids = raw.get("enrolled_student_ids", [])
                    course.lessons = raw.get("lessons", [])

                # TODO: Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't exist.
                self.attendance_log = data.get("attendance", [])
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")

    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            # TODO: Add the attendance_log to the dictionary to be saved.
            # Since it's already a list of dicts, no conversion is needed.
            "attendance": self.attendance_log,
            # ... (next_id counters) ...
        }
        # TODO: Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def find_student_by_id(self, student_id):
        return next((s for s in self.students if s.id == student_id), None)

    def find_course_by_id(self, course_id):
        return next((c for c in self.courses if c.id == course_id), None)

    def get_lessons_by_day(self, day):
        lessons = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson["day"].lower() == day.lower():
                    lessons.append({"course": course, "lesson": lesson})
        return lessons

    def check_in(self, student_id, course_id):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False

        timestamp = datetime.datetime.now().isoformat()
        record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        self.attendance_log.append(record)
        self._save_data()
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    def get_daily_lessons(self, day):
        """Get all lessons scheduled for a specific day."""
        daily_lessons = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson.get('day', '').lower() == day.lower():
                    # Get teacher name
                    teacher = self.find_teacher_by_id(course.teacher_id)
                    teacher_name = teacher.name if teacher else "Unknown"

                    # Get enrolled student names
                    student_names = []
                    for student_id in course.enrolled_student_ids:
                        student = self.find_student_by_id(student_id)
                        if student:
                            student_names.append(student.name)

                    daily_lessons.append({
                        'course_name': course.name,
                        'instrument': course.instrument,
                        'teacher': teacher_name,
                        'time': lesson.get('time', ''),
                        'students': student_names
                    })
        return daily_lessons

    def switch_course(self, student_id, from_course_id, to_course_id):
        """Switch a student from one course to another."""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student or not from_course or not to_course:
            print("Error: Invalid student or course ID.")
            return False

        if from_course_id not in student.enrolled_course_ids:
            print("Error: Student is not enrolled in the source course.")
            return False

        if to_course_id in student.enrolled_course_ids:
            print("Error: Student is already enrolled in the target course.")
            return False

        # Remove from old course
        student.enrolled_course_ids.remove(from_course_id)
        from_course.enrolled_student_ids.remove(student_id)

        # Add to new course
        student.enrolled_course_ids.append(to_course_id)
        to_course.enrolled_student_ids.append(student_id)

        self._save_data()
        print(f"Success: Student {student.name} switched from {from_course.name} to {to_course.name}.")
        return True

    def find_teacher_by_id(self, teacher_id):
        """Find a teacher by their ID."""
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None