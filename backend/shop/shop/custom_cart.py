from cart.cart import Cart


class CustomCart(Cart):

    def add(self, product, quantity=1, action=None):
        """
        Add a product to the cart or update its quantity.
        """
        id = product.id
        newItem = True
        if str(product.id) not in self.cart.keys():

            self.cart[product.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'title': product.title,
                'quantity': 1,
                'price': str(product.price),
            }
        else:
            newItem = True

            for key, value in self.cart.items():
                if key == str(product.id):
                    value['quantity'] = value['quantity'] + 1
                    newItem = False
                    self.save()
                    break
            if newItem == True:
                self.cart[product.id] = {
                    'userid': self.request,
                    'product_id': product.id,
                    'title': product.title,
                    'quantity': 1,
                    'price': str(product.price),
                }

        self.save()
