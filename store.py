import yaml
from item import Item
from shopping_cart import ShoppingCart
from errors import (
    TooManyMatchesError,
    ItemAlreadyExistsError,
    ItemNotExistError
)


class Store:
    """
    A class that shows the collection of items which are
    available for purchase.
    """
    def __init__(self, path):
        """
        Initializes a Store instance by loading items from a YAML file.

        Parameters:
        - path (str): The path to the YAML file containing item information.
        """
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        """
        Converts raw item data to a list of Item objects.

        Parameters:
        - items_raw (list): Raw item data from the YAML file.

        Returns:
        - list: List of Item objects.
        """
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        """
        Retrieves the list of items available in the store.

        Returns:
        - list: List of Item objects.
        """
        return self._items

    def search_by_name(self, item_name: str) -> list:
        """
        Searches for items in the store based on a given name and returns
        a sorted list.

        Parameters:
        - item_name (str): The name of the item to search for.

        Returns:
        - list: Sorted list of matching Item objects.
        """
        # Initialize an empty list to store matching items
        result = []
        for item in self._items:
            # Check if the item's name contains the search term
            # and it's not in the shopping cart
            if item_name in item.name and \
               item not in self._shopping_cart.item_list:
                # Add the matching item to the result list
                result.append(item)
        # Sort the result list based on the number of matching tags and
        # item name
        result.sort(key=lambda x: (-self.number_of_matching_tags(x), x.name))
        return result

    def tags_list(self) -> list:
        """
        Returns a list of all tags from items in the shopping cart.

        Returns:
        - list: List of tags.
        """
        # Initialize an empty list to store tags
        result = []
        # Iterate through each item in the shopping cart
        for item in self._shopping_cart.item_list:
            for tag in item.hashtags:
                result.append(tag)
        return result

    def number_of_matching_tags(self, item: Item) -> int:
        """
        Returns the number of matching tags between the given item and items
        in the shopping cart.

        Parameters:
        - item (Item): The item for which to calculate the matching tags.

        Returns:
        - int: The number of matching tags.
        """
        count = 0
        for tag in item.hashtags:
            count += self.tags_list().count(tag)
        return count

    def search_by_hashtag(self, hashtag: str) -> list:
        """
        Searches for items in the store based on a given
        hashtag and returns a sorted list.

        Parameters:
        - hashtag (str): The hashtag to search for.

        Returns:
        - list: Sorted list of matching Item objects.
        """
        # Initialize an empty list to store matching items
        result = []
        # Iterate through each item in the store
        for item in self._items:
            # Check if the item has the specified hashtag
            # and is not in the shopping cart
            if hashtag in item.hashtags and \
                       item not in self._shopping_cart.item_list:
                    result.append(item)

        # Sort the result list based on the number of matching tags
        # and item name
        result.sort(key=lambda x: (-self.number_of_matching_tags(x), x.name))
        return result

    def add_item(self, item_name: str):
        """
        Adds an item with the given name to the customer’s
        shopping cart.

        Parameters:
        - item_name (str): The name or distinct substring
        of the item to be added.

        Raises:
        - ItemNotExistError: If no such item exists.
        - TooManyMatchesError: If there are multiple items
        matching the given name.
        - ItemAlreadyExistsError: If the given item is already
        in the shopping cart.
        """
        # Initialize an empty list to store matching items
        matching_items = []
        # Iterate through each item in the store
        for item in self._items:
            # Check if the provided name or distinct substring is in the
            # item's name
            if item_name.lower() in item.name.lower():
                matching_items.append(item)
        # Check if no matching item is found
        if len(matching_items) == 0:
            raise ItemNotExistError(
                "No item with the specified name or substring exists."
            )

        # Check if multiple matching items are found
        if len(matching_items) > 1:
            raise TooManyMatchesError(
                "Multiple items match the given name or substring."
            )
        selected_item = matching_items[0]
        # Check if the selected item is already in the shopping cart
        if selected_item in self._shopping_cart.item_list:
            raise ItemAlreadyExistsError(
                "The selected item is already in the shopping cart."
            )
        # Add the selected item to the shopping cart
        self._shopping_cart.add_item(selected_item)

    def remove_item(self, item_name: str):
        """
        Removes an item with the given name from the customer’s shopping cart.

        Parameters:
        - item_name (str): The name or distinct substring of the item
        to be removed.

        Raises:
        - ItemNotExistError: If no such item exists.
        - TooManyMatchesError: If there are multiple
        items matching the given name.
        """
        # Initialize an empty list to store matching items
        matching_items = []
        # Iterate through each item in the shopping cart
        for item in self._shopping_cart.item_list:
            # Check if the provided name or distinct substring is in the
            # item's name
            if item_name.lower() in item.name.lower():
                matching_items.append(item)
        # Check if no matching item is found
        if len(matching_items) == 0:
            raise ItemNotExistError(
                "No item with the specified name or substring exists."
            )
        # Check if multiple matching items are found
        if len(matching_items) > 1:
            raise TooManyMatchesError(
                "Multiple items match the given name or substring."
            )
        selected_item = matching_items[0]
        # Remove the selected item from the shopping cart
        self._shopping_cart.remove_item(selected_item.name)

    def checkout(self) -> int:
        """
        Returns the total price of all items in the customer’s shopping cart.

        Returns:
        - int: Total price of items in the shopping cart.
        """
        return self._shopping_cart.get_subtotal()
