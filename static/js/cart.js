/* var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
} */

$(document).ready(function(){
	/* $.ajax(
	{
		url: '/updateItem/',
		type: "POST",
		data: "courseid="+''+"&action="+'',
		dataType: "text",
		headers: {'X-CSRFToken': csrftoken},
		success:function(response)
		{
			$('#cart-total').html(response);
			console.log(response)
		}
	}); */
	if (user == "AnonymousUser")
	{
		$('#login-opt').text('Login');
		$('#login-opt').attr("href","/login");
	}
	else
	{
		$('#login-opt').text('Logout');
		$('#login-opt').attr("href","/logout");
	}
	$(".update-cart").click(function(){
	  var courseid = $(this).attr("id");
	  var action = $(this).attr("data-action");
	  //alert(user);
	  if (user == "AnonymousUser")
	  {
		console.log("User not logged in...");
		addCookieItem(courseid,action)
	  }
	  else
	  {
		var data = "courseid="+courseid+"&action="+action
		//alert(data)
		$.ajax(
		{
			url: '/updateItem/',
			type: "POST",
			data: data,
			dataType: "text",
			headers: {'X-CSRFToken': csrftoken},
			success:function(response)
			{
				//$('#cart-total').html(response);
				console.log(response)
				location.reload()
			}
		});
	  }
	});



	function addCookieItem(productId, action){
		console.log('User is not authenticated')
	
		if (action == 'add'){
			if (cart[productId] == undefined){
			cart[productId] = {'quantity':1}
	
			}else{
				cart[productId]['quantity'] += 1
			}
		}
	
		if (action == 'remove'){
			cart[productId]['quantity'] -= 1
	
			if (cart[productId]['quantity'] <= 0){
				console.log('Item should be deleted')
				delete cart[productId];
			}
		}
		console.log('CART:', cart)
		document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
		
		location.reload()
	}
	/* $("form").on('submit',function(e){
		e.preventDefault();
		$('#form-button').addClass("hidden");
		$("#payment-info").removeClass("hidden");
	});

	if(user != "AnonymousUser")
	{
		$('#user-info').addClass("hidden");
		$('#form-wrapper').addClass("hidden");;
		$("#payment-info").removeClass("hidden");
	} */
	/* =======addedd----------- */
/* 	var total = '{{order.get_cart_total|floatformat:2}}'

	if(user != "AnonymousUser")
	{
		$('#user-info').addClass("hidden");
		$('#form-wrapper').addClass("hidden");;
		$("#payment-info").removeClass("hidden");
	}
	$("form").on('submit',function(e){
		e.preventDefault();
		$('#form-button').addClass("hidden");
		$("#payment-info").removeClass("hidden");
		
	});

	$("#make-payment").on('click',function(){
		if(user == "AnonymousUser")
		{
			var name = '';
			var email = '';
		}
		else
		{
			name = $('#name').val();
			email = $('#email').val();
		}
		var data2 = "name="+name+"&email="+email+"&total="+total;
		alert(data2);
		$.ajax({
			url: '/processOrder/',
			type: "POST",
			data: data2,
			dataType: "text",
			headers: {'X-CSRFToken': csrftoken},
			success:function(response)
			{
				//$('#cart-total').html(response);
				console.log(response)
			}
		});
	}); */
  });