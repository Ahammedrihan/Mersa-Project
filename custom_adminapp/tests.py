from django.test import TestCase

# Create your tests here.



{% extends 'layouts/main.html' %}
{% load static %}

{% block style %}
<style>
    .custom-table {
      margin-bottom: 0;
    }
    
    .custom-table thead th {
      padding: 2px 4px;
    }
    
    .custom-table tbody td {
      padding: 2px 4px;
    }
    .custom-table tbody tr td:first-child {
        padding-top: 0;
      }
      
    .custom-table tbody tr td:last-child {
        padding-bottom: 0;}

    .table tbody tr td{
        padding: 6px 30px;
    }
  </style>
{% endblock style %}

{% block body %}
    
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script> <!-- Include jQuery library -->


<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

<div class="container mt-5">
  <div class="row gutters">
      <div class="col-xl-3 col-lg-3 col-md-12 col-sm-12 col-12">
          <!-- User Profile Card -->
          <div class="card h-100">
              <div class="card-body">
                  <div class="account-settings">


                    <div class="text-center">
                        <img src="{% static 'download.png' %}" alt="Profile Photo" class="rounded-circle mt-5 mb-3" style="width: 150px; height: 150px;">
                        <h5 class="card-title">{{request.user.first_name}}</h5>
                        <button type="button" class="btn btn-primary btn-sm mt-2" onclick="document.getElementById('profile-photo-input').click();">
                            Upload Photo
                        </button>
                        <input type="file" id="profile-photo-input" style="display: none;">
                    </div>
                      <!-- View Order Button -->
                      <div class="row p-4">
                          <button type="button"
                                  class="btn btn-primary btn-block btn-lg w-100"
                                  onclick="window.location.href=''">View Order</button>
                                  <button type="button"
                                  class="btn btn-primary btn-block btn-lg w-100 mt-2"
                                  onclick="window.location.href='{% url 'user_profile'%}'">View Profile</button>
                          <button type="button"
                                  class="btn btn-primary btn-block btn-lg w-100"
                                  onclick="window.location.href=''">Back</button>
                      </div>
                  </div>
              </div>
          </div>
      </div>
    
      <div class="col-xl-9 col-lg-9 col-md-12 col-sm-12 col-12">
          <div class="card h-100">
              <div class="card-body">
                  <div class="row gutters">
                             

                    {% if  order %}

                    <div class="col-md-12 align-center">
                      <div class="card">
                          <h3 class="mb-2 text-primary text-center">You Have No Profile Order!..</h3>
                      </div>   
                      </div>
                      {% else %}



                    <div class="col-md-12 align-center">
                        <div class="card">
                            <h3 class="mb-2 text-primary text-center">Profile Orders</h3>
                        </div>   
                        </div>

                 
                      <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12 d-flex flex-wrap px-2 py-2">
                        <div class="table-responsive">
                            <table class="table table-striped table-bordered custom-table ">
                              {% if messages %}
								{% for message in messages %}
                <div class="alert alert-{{ message.tags }}" role="alert">
                  {{ message }}
                </div>
              {% endfor %}
            {% endif %}
                              <thead>
                                <tr>
                                  <th>Order ID</th>
                                  <th>Order Date</th>
                                  <th>Order Total</th>
                                  <th>Status</th>
                                  <th>Action</th>
                                </tr>
                              </thead>
                              <tbody>
                                {% for order in orders %}
                                <tr>

                                  <td> <a href="{% url 'user_profile_order_page_view' order.order_number %}">{{ order.order_number }}</a></td>
                                  <td>{{ order.order_created_date }}</td>
                                  <td>{{ order.order_total_amount}}</td>
                                  <td>{{ order.order_status }}</td>
                                  <td>
                                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModalCenter1" data-order-id="{{order.id}}">
                                      View Order
                                    </button>
                                  </td>
                                </tr>
                                {% endfor %}
                              </tbody>
                            </table>
                          </div>
                          </div>
                     
                  </div>
              </div>
          </div>
      </div>
  </div>
 
 
</div>

<div class="modal fade" id="exampleModalCenter1" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLongTitle">Order Details</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <div class="row">
          <div class="col-md-6">
            <h5 class="modal-subtitle">Order Information</h5>
            <p><strong>Order ID:</strong> <span id="order-id"></span></p>
            <p><strong>Order Number:</strong> <span id="order-number"></span></p>

           
          </div>
          <div class="col-md-6">
            <h5 class="modal-subtitle">User Information</h5>
            <p><strong>First Name:</strong> <span id="user-first-name"></span></p>
            <p><strong>Last Name:</strong> <span id="user-last-name"></span></p>
            <p><strong>Phone:</strong> <span id="user-phone"></span></p>
            <p><strong>Email:</strong> <span id="user-email"></span></p>
           
          </div>
        </div>
        <div class="row mt-4">
          <div class="col-md-6">
            <h5 class="modal-subtitle">Payment Information</h5>
            <p><strong>Payment Mode:</strong> <span id="payment-mode"></span></p>
            <p><strong>Order Total Amount:</strong> <span id="order-total-amount"></span></p>
            <p><strong>Order Status:</strong> <span id="order-status"></span></p>
            <p><strong>Order Created Date:</strong> <span id="order-created-date"></span></p>
            <p><strong>Updated At:</strong> <span id="updated-at"></span></p>
            <p><strong>Payment Mode:</strong> <span id="payment-mode"></span></p>
            <p><strong>Payment ID:</strong> <span id="payment-id"></span></p>
          </div>
          <div class="col-md-6">
            <h5 class="modal-subtitle">Shipping Information</h5>
            <p><strong>Address Line 1:</strong> <span id="address-line1"></span></p>
            <p><strong>Address Line 2:</strong> <span id="address-line2"></span></p>
            <p><strong>Country:</strong> <span id="country"></span></p>
            <p><strong>State:</strong> <span id="state"></span></p>
            <p><strong>City:</strong> <span id="city"></span></p>
            <p><strong>Postcode:</strong> <span id="postcode"></span></p>
          </div>
        </div>
        <div class="row mt-4">
          <div class="col-md-12">
            <h5 class="modal-subtitle">Order Products</h5>
            <table class="table-responsive table-bordered">
              <!-- Table header here -->
              <tr>
                <th>Product ID</th>
                <th>Product Name</th>
                <th>Variant Name</th>
                <th>Quantity</th>
                <th>Amount</th>
                <th>Created At</th>
                <th>Actions</th>
            </tr>
              <tbody>
                
                
                
                {% comment %} {% for product in order_products %} {% endcomment %}
                      
                <tr>
                    <td>{{ order_item.id }}</td>
                    <td>{{ order_item.product.product_name }}</td>
                    <td>{{ order_item.variant.variant_name}}</td>
                    <td>{{ order_item.quantity }}</td>
                    <td>{{ order_item.amount }}</td>
                    <td>{{ order_item.created_at }}</td>
                  
                        <td>
                            {% comment %} {% if order_item.order_status == 'Pending' %}
                                <a href="{% url 'cancel_order' order_item.id %}" class="btn btn-danger">Cancel</a>
                            {% elif order_item.order_status == 'Delivered' %}
                                <a href="{% url 'return_order' order_item.id %}" class="btn btn-warning">Return</a>
                            {% endif %} {% endcomment %}
                        </td>
                      

                </tr>
            
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>











<script>
    $(document).ready(function() {
      $('#exampleModalCenter1').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var orderId = button.data('order-id'); // Extract order ID from the button
        console.log(orderId);
        var modal = $(this);
    
        // Use AJAX or fetch to retrieve the order details based on the orderId
        $.ajax({
          url: '/get_order_details/' + orderId, // Replace with your actual URL
          method: 'GET',
          success: function(response) {
            // Populate the modal with the retrieved order details
            modal.find('#order-id').text(response.order_id); // Use "response", not "reponse"
            console.log(response.order_id);
            modal.find('#order-number').text(response.order_number);
            modal.find('#user-first-name').text(response.user_first_name);
            console.log(response.user_first_name);
            modal.find('#user-last-name').text(response.user_last_name);
            modal.find('#user-phone').text(response.user_phone);
            modal.find('#user-email').text(response.user_email);
            modal.find('#address-line1').text(response.address_line1);
            modal.find('#address-line2').text(response.address_line2);
            modal.find('#country').text(response.country);
            modal.find('#state').text(response.state);
            modal.find('#city').text(response.city);
            modal.find('#postcode').text(response.postcode);
            modal.find('#order-note').text(response.order_note);
            modal.find('#order-total-amount').text(response.order_total_amount);
            modal.find('#order-status').text(response.order_status);
            modal.find('#order-created-date').text(response.order_created_date);
            modal.find('#updated-at').text(response.updated_at);
            modal.find('#payment-mode').text(response.payment_mode);
            modal.find('#payment-id').text(response.payment_id);
          },
          error: function(xhr, status, error) {
            console.log("Error: " + error);
          }
        });
      });
    });
    </script>
    
    {% endif %}
{% endblock body %}

