from main import get_x1, get_x2, get_discriminant
import unittest


class TestDiscriminantMethods(unittest.TestCase):
    def test_normal(self):
        a = 1
        b = -70
        c = 600

        d = get_discriminant(a, b, c)
        self.assertEqual(d, 2500)

        x1 = get_x1(a, b, d)
        self.assertEqual(x1, 60)

        x2 = get_x2(a, b, d)
        self.assertEqual(x2, 10)

    def test_discriminant_zero(self):
        a = 1
        b = 12
        c = 36

        d = get_discriminant(a, b, c)
        self.assertEqual(d, 0)

        x1 = get_x1(a, b, d)
        x2 = get_x2(a, b, d)
        self.assertEqual(x2, "Нет решения")

    def test_discriminant_less_then_zero(self):
        a = 3
        b = -5
        c = 3

        d = get_discriminant(a, b, c)
        self.assertLess(d, 0)

        x1 = get_x1(a, b, d)
        x2 = get_x2(a, b, d)
        self.assertEqual(x1, "Нет решения")
        self.assertEqual(x1, x2)


if __name__ == "__tests__":
    unittest.main()