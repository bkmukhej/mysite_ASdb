from .models import *


class Category():

    def __str__(self):
        return self.category_id

    def __init__(self, category_obj):
        if category_obj == "root":
            self.category_name = 'root'
            self.category_id = 0
            #self.parent_id = category_obj.parent_id
            self.category_type = 1
            self.seo_name = 'root'
            self.children = set([])
            self.children_id = set([])
            self.products = set([])
            self.master_category = int()
            self.product_facing_categories = set([])
            self.category_level = 'root'
        else:    
            self.category_name = category_obj.category_name
            self.category_id = category_obj.category_id
            #self.parent_id = category_obj.parent_id
            self.category_type = category_obj.category_type
            self.seo_name = category_obj.seo_name
            self.children = set([])
            self.children_id = set([])
            self.products = set([])
            self.master_category = int()
            self.product_facing_categories = set([])

            if category_obj.category_level == 1:
                self.category_level = 'master'
            elif category_obj.category_level == 2:
                self.category_level = 'default'
            elif category_obj.category_level == 3:
                self.category_level = 'sub'
            
        
    def find_children(self, category_list):
        if self.category_level == 'sub':
            raise ValueError("Category doesn't have any children categories.")
            return
        for obj in category_list:
            if obj.parent_id == self.category_id:
                self.children.add(Category(obj))
                self.children_id.add(obj.category_id)
        return

    def get_grand_children(self, category_list):
        if self.category_level is not('master'):
            raise ValueError("Category is not a master category.")
            return

        if not(self.children):
            self.find_children(category_list)

        grand_children = set([])
        for obj in set(category_list) - self.children:
            if (obj.parent_id in self.children_id):
                grand_children.add(obj.category_id)
        return grand_children

    def find_product_facing_categories(self, category_list):
        if self.category_level == 'master':
            self.product_facing_categories.update(self.get_grand_children(category_list))
        elif self.category_level == 'default':
            self.find_children(category_list)
            self.product_facing_categories.update(self.children_id)
        elif self.category_level == 'sub':
            self.product_facing_categories.add(self.category_id)

        return

    
    def assign_products(self, product_list):
        for prod in product_list:
            if prod['category_id'] in self.product_facing_categories:
                self.products.add(prod['product_id'])
        return