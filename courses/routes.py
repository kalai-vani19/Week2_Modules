from flask import Blueprint, request, jsonify
from courses import db
from courses.models import Course, Student, Enrollment

courses_bp = Blueprint("courses", __name__, url_prefix="/api/courses")


def make_response_json(data, status_code=200):
    return jsonify({
        "status": "success",
        "data": data
    }), status_code


# GET ALL COURSES
@courses_bp.route("/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return make_response_json([c.to_dict() for c in courses])


# CREATE COURSE
@courses_bp.route("/", methods=["POST"])
def create_course():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No input data"}), 400

    required = ["name", "code", "credits"]
    for field in required:
        if field not in data:
            return jsonify({"status": "error", "message": f"{field} is required"}), 400

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"]
    )

    db.session.add(course)
    db.session.commit()

    return make_response_json(course.to_dict(), 201)


# GET COURSE BY ID
@courses_bp.route("/<int:id>/", methods=["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)
    return make_response_json(course.to_dict())


# UPDATE COURSE
@courses_bp.route("/<int:id>/", methods=["PUT"])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        course.name = data["name"]
    if "code" in data:
        course.code = data["code"]
    if "credits" in data:
        course.credits = data["credits"]

    db.session.commit()
    return make_response_json(course.to_dict())


# DELETE COURSE
@courses_bp.route("/<int:id>/", methods=["DELETE"])
def delete_course(id):
    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return make_response_json({"message": "Course deleted"})


# JOIN: Students in a Course
@courses_bp.route("/<int:id>/students/", methods=["GET"])
def get_course_students(id):
    enrollments = Enrollment.query.filter_by(course_id=id).all()

    students = []
    for e in enrollments:
        students.append(e.student.to_dict())

    return make_response_json(students)