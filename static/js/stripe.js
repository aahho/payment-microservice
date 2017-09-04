$(document).ready(function() {
	var stripe = Stripe('pk_test_uaY9HcET4hVPR7mT8JZCR2HP');
	var elements = stripe.elements();
	var style = {
	  base: {
	    // Add your base input styles here. For example:
	    fontSize: '16px',
	    lineHeight: '24px'
	  }
	};

	// Create an instance of the card Element
	var card = elements.create('card', {style: style});

	// Add an instance of the card Element into the `card-element` <div>
	card.mount('#card-element');
	card.addEventListener('change', function(event) {
	  var displayError = document.getElementById('card-errors');
	  if (event.error) {
	    displayError.textContent = event.error.message;
	  } else {
	    displayError.textContent = '';
	  }
	});
	var form = document.getElementById('payment-form');
	form.addEventListener('submit', function(event) {
	  event.preventDefault();

	  stripe.createToken(card).then(function(result) {
	    if (result.error) {
	      var errorElement = document.getElementById('card-errors');
	      errorElement.textContent = result.error.message;
	    } else {
	      stripeTokenHandler(result.token);
	    }
	  });
	});
	function stripeTokenHandler(token) {
		var form = document.getElementById('payment-form');
		var hiddenInput = document.createElement('input');
		hiddenInput.setAttribute('type', 'hidden');
		hiddenInput.setAttribute('name', 'stripeToken');
		hiddenInput.setAttribute('value', token.id);
		form.appendChild(hiddenInput);

		form.submit();
	}

	$('.payment-btn').click(function(){
		var td = $(this).closest('td');
		var value = $(td).find('input[type=hidden]').val();
		console.log(value);
		if (value) {
			var form = document.getElementById('saved-card');
			form.submit();
		}
		return false;
	});
});