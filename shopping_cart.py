from item import Item
import errors


class ShoppingCart:
    """
    Represents the current items in a shopping cart.
    """
    def __init__(self) -> None:
        """Initializes a new shopping cart with an empty list of items."""
        self.item_list = []

    def add_item(self, item: Item):
        """
        Insert the object into the shopping cart.
        If it is already in the cart, raises ItemAlreadyExistsError.
        """
        # Check if the price is legal (not negative)
        if item.price < 0:
            raise errors.ItemCanNotHaveNegativePrice

        if item in self.item_list:
            raise errors.ItemAlreadyExistsError
        else:
            self.item_list.append(item)

    def items_names_list(self):
        """Helper function for remove_item.
        Construct a list of names of the items in the shopping cart.
        """
        names_list = []
        for item in self.item_list:
            names_list.append(item.name)
        return names_list

    def remove_item(self, item_name: str):
        """Remove the item from the shopping cart by name.
        Raises ItemNotExistError if the item is not in the cart.
        """
        # Raise an error if the item is not in the names list of
        # the shopping cart
        if item_name not in self.items_names_list():
            raise errors.ItemNotExistError
        else:  # Remove the item
            for item in self.item_list:
                if item_name == item.name:
                    self.item_list.remove(item)
                    break

    def get_subtotal(self) -> int:
        """Calculate and return the subtotal of the shopping cart."""
        total_price = 0

        # Summing up the price of each item
        for item in self.item_list:
            total_price += item.price

        return total_price
