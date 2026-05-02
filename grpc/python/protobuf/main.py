from __future__ import annotations

import json

import address_pb2
import person_pb2


def print_section(title: str) -> None:
    print(f"\n=== {title} ===")


def build_person_keyword_style() -> person_pb2.Person:
    person = person_pb2.Person(
        first_name="Alice",
        age=25,
        courses=["Math", "Computer Science"],
        course_grades={"Math": 95, "Computer Science": 98},
        phone_type=person_pb2.PHONE_TYPE_MOBILE,
        email="alice@example.com",
    )

    address = address_pb2.Address(
        street="123 Main St",
        city="Addis Ababa",
        zip_code="1000",
    )
    person.address.CopyFrom(address)

    # Wrapper fields are messages, so we set their inner value.
    person.weight_kg.value = 65
    return person


def build_person_step_by_step() -> person_pb2.Person:
    person = person_pb2.Person(first_name="Alice", age=25)
    person.courses.extend(["Math", "Computer Science"])
    person.course_grades.update({"Math": 95, "Computer Science": 98})
    person.phone_type = person_pb2.PHONE_TYPE_MOBILE
    person.email = "alice@example.com"
    person.address.CopyFrom(
        address_pb2.Address(
            street="123 Main St",
            city="Addis Ababa",
            zip_code="1000",
        )
    )
    person.weight_kg.value = 65
    return person


def show_defaults_and_presence() -> None:
    empty_person = person_pb2.Person()

    print_section("Proto3 Defaults And Presence")
    print(f"default first_name: {empty_person.first_name!r}")
    print(f"default age: {empty_person.age}")
    print(f"has address? {empty_person.HasField('address')}")
    print(f"has weight_kg? {empty_person.HasField('weight_kg')}")
    print(f"which identifier? {empty_person.WhichOneof('identifier')}")


def show_oneof_behavior(person: person_pb2.Person) -> None:
    print_section("Oneof Behavior")
    print(f"identifier before username: {person.WhichOneof('identifier')}")
    print(f"email before username: {person.email!r}")

    person.username = "alice_dev"

    print(f"identifier after username: {person.WhichOneof('identifier')}")
    print(f"email after username: {person.email!r}")
    print(f"username after username: {person.username!r}")


def show_serialization(person: person_pb2.Person) -> None:
    print_section("Binary Serialization")
    binary_data = person.SerializeToString()

    with open("person.bin", "wb") as output_file:
        output_file.write(binary_data)

    json_equivalent = {
        "first_name": person.first_name,
        "age": person.age,
        "address": {
            "street": person.address.street,
            "city": person.address.city,
            "zip_code": person.address.zip_code,
        },
        "courses": list(person.courses),
        "course_grades": dict(person.course_grades),
        "phone_type": person_pb2.PhoneType.Name(person.phone_type),
        person.WhichOneof("identifier"): getattr(person, person.WhichOneof("identifier")),
        "weight_kg": person.weight_kg.value,
    }
    json_data = json.dumps(json_equivalent).encode("utf-8")

    print(f"protobuf size: {len(binary_data)} bytes")
    print(f"json size: {len(json_data)} bytes")
    print(f"first 20 protobuf bytes: {binary_data[:20].hex(' ')}")

    person_from_file = person_pb2.Person()
    with open("person.bin", "rb") as input_file:
        person_from_file.ParseFromString(input_file.read())

    print(f"deserialized first_name: {person_from_file.first_name}")
    print(f"round trip equal? {person == person_from_file}")


def main() -> None:
    person1 = build_person_keyword_style()
    person2 = build_person_step_by_step()

    print_section("Builder Style And Equality")
    print(f"person1 == person2? {person1 == person2}")
    print(f"has address? {person1.HasField('address')}")
    print(f"has email? {person1.HasField('email')}")
    print(f"has username? {person1.HasField('username')}")
    print(f"has weight_kg? {person1.HasField('weight_kg')}")

    show_defaults_and_presence()
    show_oneof_behavior(person1)
    show_serialization(person1)


if __name__ == "__main__":
    main()
