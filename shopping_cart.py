from item import Item
import errors


class ShoppingCart:
    
    #Initializes a new shopping cart with an empty list of items.
    def __init__(self) -> None:
        self.itemList = []
        
    #Insert the object into the shopping cart, if it is in the cart already, raises ItemAlreadyExistsError   
    def add_item(self, item: Item):
        
        #Check if the price is legal (not negative)
        if item.price < 0:
            raise errors.ItemCanNotHaveNegativePrice
        
        if item in self.itemList:
            raise errors.ItemAlreadyExistsError
        else: 
            self.itemList.append(item)
            
    #Helper function for the remove_item. Constract a list of names of the items that are in the shopping cart
    def items_names_list (self):
        names_list=[]
        
        for item in self.itemList:
            names_list.append(item.name)        
        
        return names_list
        
    def remove_item(self, item_name: str):
        #Raise an error if the item is not in the names list of the shopping cart
        if item_name not in self.items_names_list():
            raise errors.ItemNotExistError
        
        #Removing the item if it was found in the shopping list
        else:
            for item in self.itemList:
                if item_name == item.name:
                    self.itemList.remove(item)
                    break
                    

    def get_subtotal(self) -> int:
        totalPrice = 0
        
        #Summing up the price of each item
        for item in self.itemList:
            totalPrice+=item.price
        
        return totalPrice
    