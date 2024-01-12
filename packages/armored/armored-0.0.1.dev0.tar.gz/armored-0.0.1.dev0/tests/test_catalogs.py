import unittest

import armored.catalogs as catalogs


class TestColumn(unittest.TestCase):
    def test_varchar_column(self):
        varchar_col = catalogs.BaseColumn.model_validate(
            {
                "name": "foo",
                "dtype": {
                    "type": "varchar",
                    "max_length": 1000,
                },
            }
        )
        self.assertEqual("foo", varchar_col.name)
        print(type(varchar_col.dtype))

    def test_int_column(self):
        int_col = catalogs.BaseColumn.model_validate(
            {"name": "foo", "dtype": {"type": "int"}}
        )
        self.assertEqual("foo", int_col.name)
        self.assertEqual("integer", int_col.dtype.type)
