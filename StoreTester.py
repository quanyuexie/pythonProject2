import unittest
import Store

class StoreTester(unittest.TestCase):

    def test_product_decrease_quantity_work(self):

        p1 = Store.Product("889", "Rodent of unusual size", "when a rodent of the usual size just won't do", 33.45, 8)
        p1.decrease_quantity()
        self.assertEqual(p1.get_quantity_available(), 7)  # 执行一次decrease_quantity 那么 数量应该减少1

    def test_customer_premium_member_true(self):

        c1 = Store.Customer("Yinsheng", "QWF", True)
        is_premium_member = c1.is_premium_member()
        self.assertTrue(is_premium_member)

    def test_product_in_customer_cart(self):

        c1 = Store.Customer("Yinsheng", "QWF", True)
        c1.add_product_to_cart("prod_001")
        c1.add_product_to_cart("prod_002")
        c1_cart = c1.get_cart()
        self.assertIn("prod_001", c1_cart)
        self.assertNotIn("prod_003", c1_cart)

    def test_product_search_work(self):

        p1 = Store.Product("889", "Rodent of unusual size", "when a rodent of the usual size just won't do", 33.45, 8)
        myStore = Store.Store()
        myStore.add_product(p1)
        search_result = myStore.product_search("Rodent")
        self.assertEqual(search_result, ["889"])

    def test_store_add_member_work(self):

        myStore = Store.Store()
        c1 = Store.Customer("Yinsheng", "QWF", True)
        myStore.add_member(c1)
        self.assertEqual(myStore.get_member_from_id("QWF"), c1)
        self.assertEqual(myStore.get_member_from_id("QWF2"), None)

    def test_check_out_member_work(self):

        p1 = Store.Product("889", "Rodent of unusual size", "when a rodent of the usual size just won't do", 33.45, 2)
        c1 = Store.Customer("Yinsheng", "QWF", True)
        myStore = Store.Store()
        myStore.add_product(p1)
        myStore.add_member(c1)
        myStore.add_product_to_member_cart("889", "QWF")
        myStore.add_product_to_member_cart("889", "QWF")
        myStore.add_product_to_member_cart("889", "QWF")
        cost = myStore.check_out_member("QWF")

        self.assertEqual(cost, 33.45 * 2)
        self.assertAlmostEqual(cost, 67, 0)
        self.assertEqual(p1.get_quantity_available(), 0)
        self.assertEqual(c1.get_cart(), {})


if __name__ == '__main__':

    unittest.main(verbosity=2)
