import argparse

from conf.db import SessionLocal
from models.models import Student, Group, Teacher, Subject, Grade


session = SessionLocal()


# 🔗 Мапінг моделей
MODELS = {
    "Student": Student,
    "Group": Group,
    "Teacher": Teacher,
    "Subject": Subject,
    "Grade": Grade,
}


# 🔧 CREATE
def create(model, args):
    obj = model()

    if hasattr(obj, "name") and args.name:
        obj.name = args.name

    if isinstance(obj, Student) and args.group_id:
        obj.group_id = args.group_id

    if isinstance(obj, Subject) and args.teacher_id:
        obj.teacher_id = args.teacher_id

    if isinstance(obj, Grade):
        obj.student_id = args.student_id
        obj.subject_id = args.subject_id
        obj.grade = args.grade

    session.add(obj)
    session.commit()
    print(f"✅ Created {model.__name__}: {obj.id}")


# 📋 LIST
def list_all(model):
    results = session.query(model).all()
    for item in results:
        print(item)


# 🔄 UPDATE
def update(model, args):
    obj = session.query(model).filter(model.id == args.id).first()

    if not obj:
        print("❌ Not found")
        return

    if hasattr(obj, "name") and args.name:
        obj.name = args.name

    if isinstance(obj, Student) and args.group_id:
        obj.group_id = args.group_id

    if isinstance(obj, Subject) and args.teacher_id:
        obj.teacher_id = args.teacher_id

    if isinstance(obj, Grade):
        if args.grade:
            obj.grade = args.grade

    session.commit()
    print("✅ Updated")


# ❌ REMOVE
def remove(model, args):
    obj = session.query(model).filter(model.id == args.id).first()

    if not obj:
        print("❌ Not found")
        return

    session.delete(obj)
    session.commit()
    print("🗑 Deleted")


# 🚀 CLI
def main():
    parser = argparse.ArgumentParser()


    parser = argparse.ArgumentParser(
        description="📚 CLI for managing students database",
    )

    parser.add_argument(
        "-a", "--action",
        required=True,
        choices=["create", "list", "update", "remove"],
        help="Action to perform"
    )

    parser.add_argument(
        "-m", "--model",
        required=True,
        choices=["Student", "Group", "Teacher", "Subject", "Grade"],
        help="Database model"
    )

    parser.add_argument("-n", "--name")
    parser.add_argument("--id", type=int)
    parser.add_argument("--group_id", type=int)
    parser.add_argument("--teacher_id", type=int)
    parser.add_argument("--student_id", type=int)
    parser.add_argument("--subject_id", type=int)
    parser.add_argument("--grade", type=float)

    args = parser.parse_args()

    model = MODELS.get(args.model)

    if not model:
        print("❌ Unknown model")
        return

    if args.action == "create":
        create(model, args)

    elif args.action == "list":
        list_all(model)

    elif args.action == "update":
        update(model, args)

    elif args.action == "remove":
        remove(model, args)

    else:
        print("❌ Unknown action")


if __name__ == "__main__":
    main()
