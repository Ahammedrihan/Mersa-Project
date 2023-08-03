$(document).ready(function (){
    $('#payWithRazorpay').click(function (e){
        e.preventDefault();

    var first_name = $("[name='first_name']").val();
    var last_name = $("[name='last_name']").val();
    var email = $("[name='email']").val();
    var phone = $("[name='phone']").val();
    var address_line1 = $("[name='address_line1']").val();
    var address_line2 = $("[name='address_line2']").val();
    var country = $("[name='country']").val();
    var state = $("[name='state']").val();
    var city = $("[name='city']").val();
    var postcode = $("[name='postcode']").val();

    if (first_name == ""||last_name == ""||email == ""||phone == ""||address_line1 == ""||address_line2 == ""||country == ""||state == ""||city == ""||postcode == "")

    {
        swal("Alert!"," All Fields Are Mandatory !","error");

        return false;
    }
    else
    {
        $.ajax({
            method: "GET",
            url: "proceed-to-pay/",
            success: function(response){
                if (response.JsonResponse){
                    console.log(response,"dagdhdhdhdddgdgdrgdg")
                }
                

            }
        });


        // var options = {
        //     "key": "YOUR_KEY_ID", // Enter the Key ID generated from the Dashboard
        //     "amount": "50000", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
        //     "currency": "INR",
        //     "name": "Acme Corp", //your business name
        //     "description": "Test Transaction",
        //     "image": "https://example.com/your_logo",
        //     "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
        //     "handler": function (response){
        //         alert(response.razorpay_payment_id);
        //         alert(response.razorpay_order_id);
        //         alert(response.razorpay_signature)
        //     },
        //     "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
        //         "name": "Gaurav Kumar", //your customer's name
        //         "email": "gaurav.kumar@example.com", 
        //         "contact": "9000090000"  //Provide the customer's phone number for better conversion rates 
        //     },
        //     "notes": {
        //         "address": "Razorpay Corporate Office"
        //     },
        //     "theme": {
        //         "color": "#3399cc"
        //     }
        // };
        // var rzp1 = new Razorpay(options);
        
        // rzp1.open();

    }




    });

});