# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
API Request Validator
=====================

System:
    A JSON request body validator for a REST API. It validates incoming request
    payloads against a schema that specifies:
      - required fields
      - field types (str, int, float, bool, list, dict)
      - nested object schemas (recursive validation)
      - list element types

    The schema format is a dict where each key maps to a field spec:
        {
            "field_name": {
                "type": str | int | float | bool | list | dict,
                "required": True | False,
                "items_type": <type>,          # only for list fields
                "schema": { ... },             # only for dict (nested object) fields
            }
        }

Expected behavior:
    - A request with all required fields and correct types should validate.
    - Missing required fields produce an error.
    - Wrong types produce an error.
    - Nested objects are validated recursively: a nested object missing a
      required sub-field should produce an error.
    - Lists are validated element-by-element against items_type.

Symptoms:
    Tests are failing because nested object validation appears to be shallow --
    a request that has a nested object present (correct top-level type) but is
    missing required sub-fields inside that object passes validation when it
    should fail.
"""

import unittest


class ValidationError:
    """Represents a single validation error."""

    def __init__(self, field, message):
        self.field = field
        self.message = message

    def __repr__(self):
        return f"ValidationError(field={self.field!r}, message={self.message!r})"


class RequestValidator:
    """Validates a request payload dict against a schema."""

    def __init__(self, schema):
        self.schema = schema

    def validate(self, data, _schema=None, _prefix=""):
        """
        Validate `data` against the schema. Returns a list of ValidationError.
        An empty list means the data is valid.
        """
        schema = _schema if _schema is not None else self.schema
        errors = []

        for field_name, field_spec in schema.items():
            full_field = f"{_prefix}{field_name}" if _prefix else field_name
            required = field_spec.get("required", False)
            expected_type = field_spec.get("type")
            value = data.get(field_name)

            # --- check required ---
            if required and field_name not in data:
                errors.append(ValidationError(full_field, "Field is required"))
                continue

            # --- skip optional absent fields ---
            if field_name not in data:
                continue

            # --- check type ---
            if expected_type and not isinstance(value, expected_type):
                errors.append(
                    ValidationError(
                        full_field,
                        f"Expected type {expected_type.__name__}, "
                        f"got {type(value).__name__}",
                    )
                )
                continue

            # --- nested object ---
            if expected_type is dict and "schema" in field_spec:
                # Validate that the value is a dict (already done above)
                # and that it conforms to the nested schema.
                if isinstance(value, dict):
                    pass  # type is correct, nested object is present

            # --- list element validation ---
            if expected_type is list and "items_type" in field_spec:
                items_type = field_spec["items_type"]
                for i, item in enumerate(value):
                    if not isinstance(item, items_type):
                        errors.append(
                            ValidationError(
                                f"{full_field}[{i}]",
                                f"Expected element type {items_type.__name__}, "
                                f"got {type(item).__name__}",
                            )
                        )

        return errors

    def is_valid(self, data):
        """Convenience method: returns True if no errors."""
        return len(self.validate(data)) == 0


# ---------------------------------------------------------------------------
# Tests -- these should PASS once the bug is fixed
# ---------------------------------------------------------------------------

class TestRequestValidator(unittest.TestCase):

    def _make_user_schema(self):
        """A realistic user-creation schema with a nested address object."""
        return {
            "username": {"type": str, "required": True},
            "email": {"type": str, "required": True},
            "age": {"type": int, "required": False},
            "tags": {"type": list, "required": False, "items_type": str},
            "address": {
                "type": dict,
                "required": True,
                "schema": {
                    "street": {"type": str, "required": True},
                    "city": {"type": str, "required": True},
                    "zip": {"type": str, "required": False},
                },
            },
        }

    def test_valid_request(self):
        """A fully valid request should produce no errors."""
        schema = self._make_user_schema()
        validator = RequestValidator(schema)
        data = {
            "username": "alice",
            "email": "alice@example.com",
            "age": 30,
            "tags": ["admin", "user"],
            "address": {
                "street": "123 Main St",
                "city": "Springfield",
                "zip": "62704",
            },
        }
        errors = validator.validate(data)
        self.assertEqual(errors, [], f"Expected no errors, got: {errors}")

    def test_missing_required_top_level(self):
        """Missing a required top-level field should fail."""
        schema = self._make_user_schema()
        validator = RequestValidator(schema)
        data = {
            "email": "bob@example.com",
            "address": {"street": "1 Elm", "city": "Shelbyville"},
        }
        errors = validator.validate(data)
        field_names = [e.field for e in errors]
        self.assertIn("username", field_names)

    def test_wrong_type(self):
        """Providing the wrong type should fail."""
        schema = self._make_user_schema()
        validator = RequestValidator(schema)
        data = {
            "username": "charlie",
            "email": "charlie@example.com",
            "age": "not-a-number",
            "address": {"street": "2 Oak", "city": "Capital City"},
        }
        errors = validator.validate(data)
        field_names = [e.field for e in errors]
        self.assertIn("age", field_names)

    def test_list_element_type_validation(self):
        """List elements of the wrong type should fail."""
        schema = self._make_user_schema()
        validator = RequestValidator(schema)
        data = {
            "username": "dana",
            "email": "dana@example.com",
            "tags": ["admin", 123, "editor"],
            "address": {"street": "3 Pine", "city": "Ogdenville"},
        }
        errors = validator.validate(data)
        field_names = [e.field for e in errors]
        self.assertIn("tags[1]", field_names)

    def test_nested_object_missing_required_field(self):
        """
        A nested object that is present but missing a required sub-field
        should produce a validation error. This is the key test.
        """
        schema = self._make_user_schema()
        validator = RequestValidator(schema)
        data = {
            "username": "eve",
            "email": "eve@example.com",
            "address": {
                "zip": "90210",
                # 'street' and 'city' are required but missing!
            },
        }
        errors = validator.validate(data)
        field_names = [e.field for e in errors]
        self.assertIn(
            "address.street",
            field_names,
            f"Expected nested required field 'address.street' to fail. "
            f"Got errors: {errors}",
        )
        self.assertIn(
            "address.city",
            field_names,
            f"Expected nested required field 'address.city' to fail. "
            f"Got errors: {errors}",
        )

    def test_optional_field_absent_is_ok(self):
        """Optional fields that are absent should not produce errors."""
        schema = self._make_user_schema()
        validator = RequestValidator(schema)
        data = {
            "username": "frank",
            "email": "frank@example.com",
            "address": {"street": "5 Birch", "city": "North Haverbrook"},
        }
        errors = validator.validate(data)
        self.assertEqual(errors, [], f"Expected no errors, got: {errors}")


if __name__ == "__main__":
    unittest.main()
