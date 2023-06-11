function updateItem(id, quantity) {
    var quantityElement = $('#quantity-' + id);
    var priceElement = $('#price-' + id);
    var totalElement = $('#total-' + id);
    var decrementButton = $('#decrement-' + id);

    quantityElement.text(quantity);

    if (quantity > 1) {
        decrementButton.show();
    } else {
        decrementButton.hide();
    }

    var priceValue = priceElement.text().replace(/[^0-9.-]+/g,"");
    var price = parseFloat(priceValue);

    var total = (quantity * price).toFixed(2);

    totalElement.text('$' + total);
}

function calculateTotalOrderPrice() {
  var totalElements = $('td[id^="total-"]');
  var sum = 0;

  totalElements.each(function() {
    var totalValue = $(this).text().replace(/[^0-9.-]+/g,"");
    var total = parseFloat(totalValue);
    sum += total;
  });

  var totalPriceElement = $('#total-order-price');
  totalPriceElement.text('Total order price: $' + sum.toFixed(2));
}

function incrementItem(id, url) {
    $.ajax({
        url: url,
        method: 'GET',
        success: function(response) {
            updateItem(id, response.quantity);
            calculateTotalOrderPrice();
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

function decrementItem(id, url) {
    $.ajax({
        url: url,
        method: 'GET',
        success: function(response) {
            updateItem(id, response.quantity);
            calculateTotalOrderPrice();
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}