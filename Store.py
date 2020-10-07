# Author: Quanyue Xie
# Date: 10/7/2020
# Description： this online store simulator contains three parts
# product, customer and store, so that it can record accounts

class Product:
    """A Product object represents a product with an
    ID code, title, description, price and quantity available."""

    def __init__(self, id, title, description, price, quantity_available):
        """class initialize"""
        self._id = id
        self._title = title
        self._description = description
        self._price = price
        self._quantity_available = quantity_available

    def get_product_id(self):
        """Returns product id"""
        return self._id

    def get_title(self):
        """Returns product title"""
        return self._title

    def get_description(self):
        """Returns product description"""
        return self._description

    def get_price(self):
        """Returns product price"""
        return self._price

    def get_quantity_available(self):
        """Returns product quantity available"""
        return self._quantity_available

    def decrease_quantity(self):
        """Decreases the quantity available by one"""
        if self._quantity_available > 0:
            self._quantity_available -= 1
        else:
            print("no enought quantity to decrease")


class Customer:
    """A Customer object represents a customer with a name and account ID.
    Customers must be members of the Store to make a purchase.
    Premium members get free shipping.
    """

    def __init__(self, name, id, premium_member):
        """class initialize
        customer's initial cart is an empty dict
        """
        self._name = name
        self._id = id
        self._premium_member = premium_member
        self._cart = {}

    def get_cart(self):
        """Returns customer cart"""
        return self._cart

    def get_name(self):
        """Returns customer name"""
        return self._name

    def get_customer_id(self):
        """Returns customer id"""
        return self._id

    def is_premium_member(self):
        """ Returns whether the customer is a premium member (True or False)"""
        return self._premium_member

    def add_product_to_cart(self, product_id):
        """Takes a product ID code and adds it to the Customer's cart
        cart is a dictionary object, the key is product_id and the value is product count
        example: cart={'id_apple':2,'id_book':10} means there are 2 apples and 10 books.
        """
        if not product_id in self._cart:
            self._cart[product_id] = 1
        else:
            self._cart[product_id] += 1

    def empty_cart(self):
        """Empties the Customer's cart"""
        self._cart = {}


class InvalidCheckoutError(Exception):
    def __str__(self):
        return "the ID doesn't match a member of the Store"


class Store:
    """A Store object represents a store,
    which has some number of products in its inventory and some number of customers as members.
    """

    def __init__(self):
        """class initialize
        the initial inventory is an empty dict, the dict's key is product_id, the value is a Product object
        the initial customer is an empty dict, the dict's key is customer_id, the value is a Customer object
        """
        self._inventory = {}
        self._membership = {}

    def add_product(self, product):
        """Takes a Product object and adds it to the inventory
        example: inventory={
            '001':Product('001','apple','apple desc ...',9.9,10),
            '002':Product('002','book','book desc ...',11.2,100)}
        """
        product_id = product.get_product_id()

        if product_id not in self._inventory:
            self._inventory[product_id] = product
        else:
            print("this product already exists ...")

    def add_member(self, customer):
        """Takes a Customer object and adds it to the membership
        example: membership={
            '001':Customer('Yinsheng','001',False),
            '002':Customer('kris','002',True)}
        """
        customer_id = customer.get_customer_id()
        if customer not in self._membership:
            self._membership[customer_id] = customer
        else:
            print("customer already exists ...")

    def get_product_from_id(self, product_id):
        """Takes a Product ID and returns the Product with the matching ID.
        If no matching ID is found in the inventory, it returns the special value None
        """
        return self._inventory.get(product_id)

    def get_member_from_id(self, customer_id):
        """ Takes a Customer ID and returns the Customer with the matching ID.
        If no matching ID is found in the membership, it returns the special value None
        """
        return self._membership.get(customer_id)

    def product_search(self, search_string):
        """Takes a search string and returns a sorted (in lexicographic order) list of ID codes
        for every product in the inventory whose title or description contains the search string
        """
        search_result = []

        isearch_string = search_string.lower()

        for k, v in self._inventory.items():
            if isearch_string in v.get_title().lower() or isearch_string in v.get_description().lower():
                search_result.append(k)
        return sorted(search_result)

    def add_product_to_member_cart(self, product_id, customer_id):
        """ Takes a Product ID and a Customer ID (in that order)."""

        current_product = self.get_product_from_id(product_id)
        current_customer = self.get_member_from_id(customer_id)

        if current_product == None:
            return "product ID not found"
        if current_customer == None:
            return "member ID not found"

        if current_product.get_quantity_available() == 0:
            return "product out of stock"
        else:
            current_customer.add_product_to_cart(product_id)
            return "product added to cart"

    def check_out_member(self, customer_id):
        """Takes a Customer ID.
        return the charge for the member's cart.
        """
        current_customer = self.get_member_from_id(customer_id)
        if current_customer == None:
            raise InvalidCheckoutError

        current_customer_cart = current_customer.get_cart()

        cost = 0

        for k, v in current_customer_cart.items():
            current_product = self.get_product_from_id(product_id=k)

            if current_product.get_quantity_available() >= v:
                for i in range(v):
                    current_product.decrease_quantity()
                    cost += current_product.get_price()

            else:
                for i in range(current_product.get_quantity_available()):
                    current_product.decrease_quantity()
                    cost += current_product.get_price()

        current_customer.empty_cart()

        if current_customer.is_premium_member() == True:
            return cost
        else:
            return cost * 1.07


def main():
    p1 = Product("889", "Rodent of unusual size", "when a rodent of the usual size just won't do", 33.45, 8)
    c1 = Customer("Yinsheng", "QWF", False)
    myStore = Store()
    myStore.add_product(p1)
    myStore.add_member(c1)

    # print(myStore.product_search("rodent"))
    add_product_result = myStore.add_product_to_member_cart("889", "QWF")
    # print(add_product_result)
    try:
        result = myStore.check_out_member("QWF")
        print(result)
    except InvalidCheckoutError as err:
        print(err)


if __name__ == "__main__":
    main()
