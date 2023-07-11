$(document).ready(function() {
var perPage = 8;
var page = 1;
    function loadProducts() {
      var startIndex = (page - 1) * perPage;
      var endIndex = startIndex + perPage;
      $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem&limit=${perPage}&offset=${startIndex}`, function(data) { //BUG FIXED NEW
        var product_item = data.items;
        if (product_item.length > 0) {
          totalPages = Math.ceil(data.meta.total_count / perPage); //BUG FIXED NEW
          console.log('=>'+totalPages);
          for (var i = 0; i < product_item.length; i++) {
            if (i >= product_item.length) {
              break;
            }
            var productPage = product_item[i];
            var productPageId = productPage.id;
            var productPageSlug = productPage.meta.slug;
            var productPostsAPIURL = `/UNIQUEAPI174/pages/${productPageId}`;
            $.getJSON(productPostsAPIURL, function(productsData) {
              var product = productsData;
              if (product.PRODUCT_OFFER.length > 0) {
                var postHTML = `
                  <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                    <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                    <div class="card-body">
                      <h3 class="card-title h4">
                        <a href="" class="black-color">${product.title}</a>
                      </h3>
                      <span class="text-decoration-line-through icon2">${separateDigitsWithComma(product.price)}</span>
                      <span class="red-color">${separateDigitsWithComma(product.PRODUCT_OFFER[0].value)}<span>تومان</span></span>
                      <hr />
                      <div id="TOOLS" class="tolspro">
                      <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                        <span class="price"></span></a>
                        <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                        <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                      </div>
                    </div>
                  </div>
                `;
                $('#PRODUCT').append(postHTML);
              } else {
                var postHTML = `
                  <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                    <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                    <div class="card-body">
                      <h3 class="card-title h4">
                        <a href="" class="black-color">${product.title}</a>
                      </h3>
                      <span class="red-color">${separateDigitsWithComma(product.price)}<span>تومان</span></span>
                      <hr />
                      <div id="TOOLS" class="tolspro">
                      <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}', '${productPageSlug}', '${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                      <span class="price"></span>
                        <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                        <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                        </div>
                    </div>
                  </div>
                `;
                $('#PRODUCT').append(postHTML);
              }//
  
            });
          }
          if (page >= totalPages) {
            $('#load-more').hide();
          } else {
            $('#load-more').show();
          }
  
          page++;
        }
      });
    }
    $('#load-more').click(function() {
        loadProducts();
      });
    loadProducts();
  });
// Start filters :
var pageD = 1;
function defaultProduct() {
  var perPage = 8;
  var startIndex = (page - 1) * perPage;
  var endIndex = startIndex + perPage;

  $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem&order=first_published_at&limit=${perPage}&offset=${startIndex}`, function(data) {
    var product_item = data.items;
    if (product_item.length > 0) {
      totalPages = Math.ceil(data.meta.total_count / perPage);
      $('#PRODUCT').html("");

      for (var i = 0; i < product_item.length; i++) {
        if (i >= product_item.length) {
          break;
        }
        var productPage = product_item[i];
        var productPageId = productPage.id;
        var productPageSlug = productPage.meta.slug;
        var productPostsAPIURL = `/UNIQUEAPI174/pages/${productPageId}`;
        $.getJSON(productPostsAPIURL, function(productsData) {
          var product = productsData;
          if (product.PRODUCT_OFFER.length > 0) {
            var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>
                  <span class="text-decoration-line-through icon2">${separateDigitsWithComma(product.price)}</span>
                  <span class="red-color">${separateDigitsWithComma(product.PRODUCT_OFFER[0].value)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                    <span class="price"></span>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          } else {
            var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>
                  <span class="red-color">${separateDigitsWithComma(product.price)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}', '${productPageSlug}', '${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                  <span class="price"></span>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          }

        });
      }
      if (pageD >= totalPages) {
        $('#load-more').hide();
      } else {
        $('#load-more').show();
      }

      pageD++;
    }
  });
}
var pageO = 1;
function oldProduct() {
  var perPage = 8;
  var startIndex = (pageO - 1) * perPage;
  var endIndex = startIndex + perPage;

  $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem&order=-first_published_at&limit=${perPage}&offset=${startIndex}`, function(data) {
    var product_item = data.items;
    if (product_item.length > 0) {
      totalPages = Math.ceil(data.meta.total_count / perPage);
      $('#PRODUCT').html("");

      for (var i = 0; i < product_item.length; i++) {
        if (i >= product_item.length) {
          break;
        }
        var productPage = product_item[i];
        var productPageId = productPage.id;
        var productPageSlug = productPage.meta.slug;
        var productPostsAPIURL = `/UNIQUEAPI174/pages/${productPageId}`;
        $.getJSON(productPostsAPIURL, function(productsData) {
          var product = productsData;
          if (product.PRODUCT_OFFER.length > 0) {
            var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>{
                  <span class="text-decoration-line-through icon2">${separateDigitsWithComma(product.price)}</span>
                  <span class="red-color">${separateDigitsWithComma(product.PRODUCT_OFFER[0].value)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                    <span class="price"></span>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          } else {
            var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>
                  <span class="red-color">${separateDigitsWithComma(product.price)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}', '${productPageSlug}', '${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                  <span class="price"></span>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          }
        });
      }
      if (pageO >= totalPages) {
        $('#load-more').hide();
      } else {
        $('#load-more').show();
      }

      pageO++;
    }
  });
}
var pageL = 1;
function lowPrice() {
  var perPage = 8;
  var startIndex = (pageL - 1) * perPage;
  var endIndex = startIndex + perPage;
  $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem&order=price&limit=${perPage}&offset=${startIndex}`, function(data) {
    var product_item = data.items;
    if (product_item.length > 0) {
      totalPages = Math.ceil(data.meta.total_count / perPage);
      $('#PRODUCT').html("");
      for (var i = 0; i < product_item.length; i++) {
        if (i >= product_item.length) {
          break;
        }
        var productPage = product_item[i];
        var productPageId = productPage.id;
        var productPageSlug = productPage.meta.slug;
        var productPostsAPIURL = `/UNIQUEAPI174/pages/${productPageId}`;
        $.getJSON(productPostsAPIURL, function(productsData) {
          var product = productsData;
          if (product.PRODUCT_OFFER.length > 0) {
            var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>
                  <span class="text-decoration-line-through icon2">${separateDigitsWithComma(product.price)}</span>
                  <span class="red-color">${separateDigitsWithComma(product.PRODUCT_OFFER[0].value)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                    <span class="price"></span>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          } else {
            var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>
                  <span class="red-color">${separateDigitsWithComma(product.price)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}', '${productPageSlug}', '${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                  <span class="price"></span>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          }

        });
      }
      if (pageL >= totalPages) {
        $('#load-more').hide();
      } else {
        $('#load-more').show();
      }

      pageL++;
    }
  });
}
var pageH = 1;
function highPrice() {
  var perPage = 8;
  var startIndex = (pageH - 1) * perPage;
  var endIndex = startIndex + perPage;
  $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem&order=-price&limit=${perPage}&offset=${startIndex}`, function(data) {
    var product_item = data.items;
    if (product_item.length > 0) {
      totalPages = Math.ceil(data.meta.total_count / perPage);
      $('#PRODUCT').html("");
      for (var i = 0; i < product_item.length; i++) {
        if (i >= product_item.length) {
          break;
        }
        var productPage = product_item[i];
        var productPageId = productPage.id;
        var productPageSlug = productPage.meta.slug;
        var productPostsAPIURL = `/UNIQUEAPI174/pages/${productPageId}`;
        $.getJSON(productPostsAPIURL, function(productsData) {
          var product = productsData;
          if (product.PRODUCT_OFFER.length > 0) {
            var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>
                  <span class="text-decoration-line-through icon2">${separateDigitsWithComma(product.price)}</span>
                  <span class="red-color">${separateDigitsWithComma(product.PRODUCT_OFFER[0].value)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                    <span class="price"></span>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          } else {
            var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>
                  <span class="red-color">${separateDigitsWithComma(product.price)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}', '${productPageSlug}', '${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                  <span class="price"></span>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          }

        });
      }
      if (pageH >= totalPages) {
        $('#load-more').hide();
      } else {
        $('#load-more').show();
      }

      pageH++;
    }
  });
}
function priceSearch() {
  var minPrice = document.getElementById("min-price").value;
  var maxPrice = document.getElementById("max-price").value;
  if(minPrice && maxPrice){
    $.ajax({
      url : '/priceSearch',
      type : 'POST',
      data : {
        'minPrice' : minPrice,
        'maxPrice' : maxPrice,
      },
      success : function(response){
        if (response.success === false){
          Swal.fire({
            icon: 'error',
            title: response.status,
            showConfirmButton: true,
            timer: 2500,
          });
        }else{
          $('#PRODUCT').html("");
          for (let i = 0; i < response.data_list.length; i++) {
            $.getJSON(`/UNIQUEAPI174/pages/${response.data_list[i].status}`,function(productData){
              let product = productData;
              if(product.PRODUCT_OFFER.length >0){
              var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>
                  <span class="text-decoration-line-through icon2">${separateDigitsWithComma(product.price)}</span>
                  <span class="red-color">${separateDigitsWithComma(product.PRODUCT_OFFER[0].value)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}','${product.meta.html_url}','${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                    <span class="price"></span></a>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${product.meta.html_url}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                  </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          } else {
            var postHTML = `
              <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                <div class="card-body">
                  <h3 class="card-title h4">
                    <a href="" class="black-color">${product.title}</a>
                  </h3>
                  <span class="red-color">${separateDigitsWithComma(product.price)}<span>تومان</span></span>
                  <hr />
                  <div id="TOOLS" class="tolspro">
                  <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}', '${product.meta.html_url}', '${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                  <span class="price"></span>
                    <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                    <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${product.meta.html_url}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                </div>
              </div>
            `;
            $('#PRODUCT').append(postHTML);
          }
            })//end JSON request
          };// end for
        };
      }
    });// end ajax request
  }else{
    Swal.fire({
      icon: "error",
      title: "ابتدا یک مقدار وارد کنید",
      showConfirmButton: false,
      timer: 2500,
    });
  }// end if
}
function add_favourite(product_id, product_slug, product_title, product_image, product_quantity, product_color, product_add_cart_date){
  // Data to be sent with the POST request
  let token = $('input[name=csrfmiddlewaretoken]').val();
  let data = {
    'product_id': product_id,
    'product_slug':product_slug,
    'product_title': product_title,
    'product_image': product_image,
    'quantity':product_quantity,
    'selected_color_text':product_color,
    'add_cart_date':product_add_cart_date,
    csrfmiddlewaretoken: token,
  };
  // Send request to server
  $.ajax({
    url: '/cart/favourite/add',
    type: 'POST',
    data: data,
    success: function(response) {
      if (response.success === false) {
        Swal.fire({
          icon: "error",
          title: response.status,
          showConfirmButton: false,
          timer: 3000,
        });
      } else {
        Swal.fire({
          icon: "success",
          title: response.status,
          showConfirmButton: false,
          timer: 2000,
        });
      }
    },
    error: function(xhr, status, error) {
      console.log(status);
      Swal.fire({
        icon: "error",
        title: status,
        showConfirmButton: false,
        timer: 3000,
      });
    }
  });
}
// add comparison
function add_comparison(product_id, product_slug, product_title, product_image, product_quantity, product_color, product_color_quantity, product_add_cart_date){
  let token = $('input[name=csrfmiddlewaretoken]').val();
  // Data to be sent with the POST request
  let data = {
    'product_id':product_id,
    'product_slug':product_slug,
    'product_title': product_title,
    'product_image': product_image,
    'quantity':product_quantity,
    'selected_color_text':product_color,
    'product_color_quantity':product_color_quantity,
    'add_cart_date':product_add_cart_date,
    csrfmiddlewaretoken: token,
  };
  // Send request to server
  $.ajax({
    url: '/cart/comparison/add',
    type: 'POST',
    data: data,
    success: function(response) {
      if (response.success === false) {
        Swal.fire({
          icon: "error",
          title: response.status,
          showConfirmButton: false,
          timer: 3000,
        });
      } else {
        Swal.fire({
          icon: "success",
          title: response.status,
          showConfirmButton: false,
          timer: 2000,
        });
      }
    },
    error: function(xhr, status, error) {
      console.log(status);
      Swal.fire({
        icon: "error",
        title: status,
        showConfirmButton: false,
        timer: 3000,
      });
    }
  });
}


document.getElementById("defaultFilter").addEventListener("click", function(event) {
  event.preventDefault();
  defaultProduct();
});
document.getElementById("lowPriceFilter").addEventListener("click", function(event) {
  event.preventDefault();
  lowPrice();
});
document.getElementById("highPriceFilter").addEventListener("click", function(event) {
  event.preventDefault();
  highPrice();
});
document.getElementById("newFilter").addEventListener("click", function(event) {
  event.preventDefault();
  defaultProduct();
});
$('#oldFilter').click(function() {
  oldProduct();
});
// فیلتر - چک باکس
var inventoryCheckbox = document.getElementById("inventory");
var specialDiscountCheckbox = document.getElementById("specialdiscount");
// Offer CheckBox ! =>CHANGE<=
var pageQ = 1;
var pageQE = 1;
inventoryCheckbox.addEventListener("change", function() {
  var perPage = 8;
  var startIndex = (pageQ - 1) * perPage;
  var endIndex = startIndex + perPage;
  if (inventoryCheckbox.checked) {
    $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem&limit=${perPage}&offset=${startIndex}`, function(data) {
      var product_item = data.items;
      if (product_item.length > 0) {
        totalPages = Math.ceil(data.meta.total_count / perPage);
        $('#PRODUCT').html("");
        for (var i = 0; i < product_item.length; i++) {
          if (i >= product_item.length) {
            break;
          }
          var productPage = product_item[i];
          var productPageId = productPage.id;
          var productPageSlug = productPage.meta.slug;
          var productPostsAPIURL = `/UNIQUEAPI174/pages/${productPageId}`;
          $.getJSON(productPostsAPIURL, function(productsData) {
            var product = productsData;
              var postHTML = `
                <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                  <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                  <div class="card-body">
                    <h3 class="card-title h4">
                      <a href="" class="black-color">${product.title}</a>
                    </h3>
                    <span class="text-decoration-line-through icon2">${separateDigitsWithComma(product.price)}</span>
                    <span class="red-color">${separateDigitsWithComma(product.PRODUCT_OFFER[0].value)}<span>تومان</span></span>
                    <hr />
                    <div id="TOOLS" class="tolspro">
                    <span class="bi bi-heart" onclick="add_favourite('${product.id}', '${productPageSlug}', '${product.product_title}','${product.image.url}','FV','SV','174')"></span>
                      <span class="price"></span>
                      <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                      <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','174')"></span>
                    </div>
                  </div>
                </div>
              `;
              $('#PRODUCT').append(postHTML);
            });
        }
        if (pageQ >= totalPages) {
          $('#load-more').hide();
        } else {
          $('#load-more').show();
        }
        pageQ++;
      }
    });
  } else {
    var perPage = 8;
    var startIndex = (page - 1) * perPage;
    var endIndex = startIndex + perPage;
    $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem&limit=${perPage}&offset=${startIndex}`, function(data) {
      var product_item = data.items;
      if (product_item.length > 0) {
        totalPages = Math.ceil(data.meta.total_count / perPage);
        $('#PRODUCT').html("");
        for (var i = 0; i < product_item.length; i++) {
          if (i >= product_item.length) {
            break;
          }
          var productPage = product_item[i];
          var productPageId = productPage.id;
          var productPageSlug = productPage.meta.slug;
          var productPostsAPIURL = `/UNIQUEAPI174/pages/${productPageId}`;
          $.getJSON(productPostsAPIURL, function(productsData) {
            var product = productsData;
              var postHTML = `
                <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                  <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                  <div class="card-body">
                    <h3 class="card-title h4">
                      <a href="" class="black-color">${product.title}</a>
                    </h3>
                    <span class="red-color">${separateDigitsWithComma(product.price)}<span>تومان</span></span>
                    <hr />
                    <div id="TOOLS" class="tolspro">
                    <span class="bi bi-heart" onclick="add_favourite('${product.id}', '${productPageSlug}', '${product.product_title}','${product.image.url}','FV','SV','174')"></span>
                      <span class="price"></span>
                      <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                      <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','174')"></span>
                    </div>
                  </div>
                </div>
              `;
              $('#PRODUCT').append(postHTML);
          });
        }
        if (pageQE >= totalPages) {
          $('#load-more').hide();
        } else {
          $('#load-more').show();
        }
  
        pageQE++;
      }
    });
  }
});

var pageXZ = 1;
specialDiscountCheckbox.addEventListener("change", function() {
  var perPage = 8;
  var startIndex = (pageXZ - 1) * perPage;
  var endIndex = startIndex + perPage;
  if (specialDiscountCheckbox.checked) {
    $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem&is_available=true&limit=${perPage}&offset=${startIndex}`, function(data) {
      var product_item = data.items;
      if (product_item.length > 0) {
        totalPages = Math.ceil(data.meta.total_count / perPage);
        $('#PRODUCT').html("");
        for (var i = 0; i < product_item.length; i++) {
          if (i >= product_item.length) {
            break;
          }
          var productPage = product_item[i];
          var productPageId = productPage.id;
          var productPageSlug = productPage.meta.slug;
          var productPostsAPIURL = `/UNIQUEAPI174/pages/${productPageId}`;
          $.getJSON(productPostsAPIURL, function(productsData) {
            var product = productsData;
            if (product.PRODUCT_OFFER.length > 0) {
              var postHTML = `
                <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                  <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                  <div class="card-body">
                    <h3 class="card-title h4">
                      <a href="" class="black-color">${product.title}</a>
                    </h3>
                    <span class="text-decoration-line-through icon2">${separateDigitsWithComma(product.price)}</span>
                    <span class="red-color">${separateDigitsWithComma(product.PRODUCT_OFFER[0].value)}<span>تومان</span></span>
                    <hr />
                    <div id="TOOLS" class="tolspro">
                    <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                      <span class="price"></span></a>
                      <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                      <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                  </div>
                </div>
              `;
              $('#PRODUCT').append(postHTML);
            } else {
              var postHTML = `
                <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                  <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                  <div class="card-body">
                    <h3 class="card-title h4">
                      <a href="" class="black-color">${product.title}</a>
                    </h3>
                    <span class="red-color">${separateDigitsWithComma(product.price)}<span>تومان</span></span>
                    <hr />
                    <div id="TOOLS" class="tolspro">
                    <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}', '${productPageSlug}', '${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                    <span class="price"></span>
                      <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                      <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                      </div>
                  </div>
                </div>
              `;
              $('#PRODUCT').append(postHTML);
            }

          });
        }
        if (pageXZ >= totalPages) {
          $('#load-more').hide();
        } else {
          $('#load-more').show();
        }

        pageXZ++;
      }
    });
  } else {
    $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem&limit=${perPage}&offset=${startIndex}`, function(data) {
      var product_item = data.items;
      if (product_item.length > 0) {
        totalPages = Math.ceil(data.meta.total_count / perPage);
        $('#PRODUCT').html("");
        for (var i = 0; i < product_item.length; i++) {
          if (i >= product_item.length) {
            break;
          }
          var productPage = product_item[i];
          var productPageId = productPage.id;
          var productPageSlug = productPage.meta.slug;
          var productPostsAPIURL = `/UNIQUEAPI174/pages/${productPageId}`;
          $.getJSON(productPostsAPIURL, function(productsData) {
            var product = productsData;
            if (product.PRODUCT_OFFER.length > 0) {
              var postHTML = `
                <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                  <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                  <div class="card-body">
                    <h3 class="card-title h4">
                      <a href="" class="black-color">${product.title}</a>
                    </h3>
                    <span class="text-decoration-line-through icon2">${separateDigitsWithComma(product.price)}</span>
                    <span class="red-color">${separateDigitsWithComma(product.PRODUCT_OFFER[0].value)}<span>تومان</span></span>
                    <hr />
                    <div id="TOOLS" class="tolspro">
                    <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                      <span class="price"></span></a>
                      <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                      <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                    </div>
                  </div>
                </div>
              `;
              $('#PRODUCT').append(postHTML);
            } else {
              var postHTML = `
                <div id="PRODUCT_BODY" class="cardpro" style="width: 18rem">
                  <img src="${product.image.url}" class="card-img-top" alt="${product.image.alt}" />
                  <div class="card-body">
                    <h3 class="card-title h4">
                      <a href="" class="black-color">${product.title}</a>
                    </h3>
                    <span class="red-color">${separateDigitsWithComma(product.price)}<span>تومان</span></span>
                    <hr />
                    <div id="TOOLS" class="tolspro">
                    <span class="bi bi-heart black-color"onclick="add_favourite('${product.id}', '${productPageSlug}', '${product.product_title}','${product.image.url}','FV','SV','0')"></span>
                    <span class="price"></span>
                      <a href="${product.meta.html_url}"><button class="btn btn-danger addtocard" type="submit">مشاهده و خرید</button></a>
                      <span class="bi bi-arrow-left-right" onclick="add_comparison('${product.id}','${productPageSlug}','${product.product_title}','${product.image.url}','FV','SV','1','0')"></span>
                      </div>
                  </div>
                </div>
              `;
              $('#PRODUCT').append(postHTML);
            }

          });
        }
        if (pageXZ >= totalPages) {
          $('#load-more').hide();
        } else {
          $('#load-more').show();
        }

        pageXZ++;
      }else{
        Swal.fire({
          title: "محصولی برای نمایش با این فیلتر وجود ندارد",
          showConfirmButton: false,
          timer: 2000,
        });
      }
    });
  }
});
function loadProductCategory() {
    $.getJSON(`/UNIQUEAPI174/pages/?type=category.CategoryProduct&order=-first_published_at`, function(data) {
      var totalChild = data.meta.total_count;
      var categoryData = data.items;

      for (var i = 0; i < totalChild; i++) {
        if (i >= totalChild) {
          break;
        }
        var pageCategory = categoryData[i];

        var category_to_pages = `<ul class="navliststyle asidecat">
        <li class="bbs1px">
          <a href="/category/products/${pageCategory.id}" class="black-color ahover">${pageCategory.title}</a>
          <span id="${pageCategory.id}"></span>
        </li>
      </ul>`;
        $('#setCat').append(category_to_pages);
      }
    });
  }

loadProductCategory();

function cat_count() {
  $.getJSON(`/UNIQUEAPI174/pages/?type=product.InventoryItem`, function(data) {
    var products = data.items;
    let childs = [];
    let cat_id = new Set();
      for (var c = 0; c < products.length; c++) {
        childs.push(products[c].id);
      }

      let requests = [];
      for (let q = 0; q < childs.length; q++) {
        requests.push(
          $.getJSON(`/UNIQUEAPI174/pages/${childs[q]}`, function(posts) {
            for (let w = 0; w < posts.collection.length; w++){
              cat_id.add(posts.collection[w].id.toString());
            };// end for get collection.id
          })//End getJSON
        );
      }//end for q
      $.when.apply($, requests).then(function() {
        let request_total = Array.from(cat_id);
        for (let x = 0; x < request_total.length; x++) {
          console.log('total => ' + request_total[x]);
          $.ajax({
            url: '/category/product_total',
            type: 'POST',
            data: {
              'request_total': request_total[x],
            },
            success: function(response) {
              if (response.success) {
                console.log('success! ' + response.status);
                document.getElementById(request_total[x]).innerHTML = response.status;
              }
            }
          });
        }
      });
  });
}
cat_count() //Return product category count
// seprate digits with comma function
function separateDigitsWithComma(number) {
  // Convert the number to a string
  var numberString = String(number);

  // Split the string into an array of characters
  var digitsArray = numberString.split('');

  // Reverse the array to process digits from right to left
  digitsArray.reverse();

  // Iterate over the array and insert commas after every third digit
  for (var i = 3; i < digitsArray.length; i += 4) {
    digitsArray.splice(i, 0, ',');
  }

  // Reverse the array again to get the original order
  digitsArray.reverse();

  // Join the array into a string
  var result = digitsArray.join('');

  return result;
}