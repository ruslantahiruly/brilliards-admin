$(function() {

  $('.city-switcher').click(function () {
    $('.city-selector').addClass('is-visible');
  });

  $('.city-selector-close').click(function () {
    $('.city-selector').removeClass('is-visible');
  });

  $('.city-selector').on('click', '.city-selector-item', function () {
    if ($(this).attr('data-city')) {
      var city = $(this).attr('data-city')
      $.ajax({
        type: 'GET',
        url: '/',
        data: {city: city},
        success: function (data) {
          location.href = '/';
        },
        error: function () {},
      });
    }
  });

  $('.tabs-panel').on('click', '.tabs-item:not(.active)', function () {
    $(this)
      .addClass('active').siblings().removeClass('active')
      .closest('.tabs').find('.tabs-page').removeClass('active').eq($(this).index()).addClass('active');
  });

  $('.tabs').on('click', '.tab-next', function () {
    $(this)
      .closest('.tabs-page').removeClass('active').next('.tabs-page').addClass('active')
      .closest('.tabs').find('.tabs-item.active').removeClass('active').next('.tabs-item').addClass('active');
  });

  $('select').styler();
  $('input[type=checkbox]').styler();
  $('input[type=file]').styler();

  $('.phone').inputmask({"mask": "+7 (999) 999-99-99"});
  $('.working-hours-input').inputmask({"mask": "99:99"});

  if ($('.t-white .owl-carousel.owl-calendar .item').length > 5) {
    $('.t-white .owl-carousel.owl-calendar').owlCarousel({
      loop:false,
      items: 10,
      margin: 20,
      // dots: true,
      // nav: true,
    });
  }

  $('.owl-carousel.content-section-photos').owlCarousel({
    loop:true,
    items: 1,
  });

  // $('.t-white .owl-carousel.owl-calendar').owlCarousel({
  //   loop:false,
  //   items: 10,
  //   margin: 20,
  //   dots: false,
  // });

  $('#dialog-create').dialog({
    autoOpen: false,
  });

  $('#dialog-update').dialog({
    autoOpen: false,
  });

  $('#datepicker').datepicker({
    dateFormat: "yy-mm-dd",
    showOn: "both",
    buttonImage: "/static/clubs/img/icons/icon-calendar.svg",
    buttonImageOnly: true,
    buttonText: "Выберите дату",
    defaultDate: new Date(),
    minDate: +1,
    maxDate: +7,
    onSelect: function (dateText, inst) {
      var section = $(this).closest('.content-section');
      section.addClass('running');
      var col = $(this).closest('.col-12').next('.col-12');
      var date = $(this).datepicker('getDate');
      var dayOfTheWeek = weekday[date.getUTCDay()];
      $.ajax({
        type: 'GET',
        data: {day_of_the_week: dayOfTheWeek},
        success: function (data) {
          col.replaceWith(data);
          section.removeClass('running');
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('#datepicker').datepicker('refresh');

  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  var weekday=new Array(7);
  weekday[0]="MO";
  weekday[1]="TU";
  weekday[2]="WE";
  weekday[3]="TH";
  weekday[4]="FR";
  weekday[5]="SA";
  weekday[6]="SU";

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    complete: function () {
      $('select').styler({
        // selectVisibleOptions: 5,
      });
      $('input[type=checkbox]').styler();
      $('input[type=file]').styler();
      $('.phone').inputmask({"mask": "+7(999) 999-99-99"});
      $('.working-hours-input').inputmask({"mask": "99:99"});
      $('.price-hours-input').inputmask({"mask": "99:99"});
      $('#hall-accordion').accordion({
        header: "h3",
        collapsible: true,
        active: false,
        heightStyle: "content",
        beforeActivate: function(event, ui ) {
          var header = $(event.originalEvent.target).is('.ui-accordion-header');
          return header;
        },
      });
      $('.game-accordion').accordion({
        header: "h4",
        collapsible: true,
        active: false,
        heightStyle: "content",
        beforeActivate: function(event, ui ) {
          var header = $(event.originalEvent.target).is('.ui-accordion-header');
          return header;
        },
      });
      $('.table-accordion').accordion({
        header: "h5",
        collapsible: true,
        active: false,
        heightStyle: "content",
        beforeActivate: function(event, ui ) {
          var header = $(event.originalEvent.target).is('.ui-accordion-header');
          return header;
        },
      });
      $('.price-accordion').accordion({
        header: "h3",
        collapsible: true,
        active: false,
        heightStyle: "content",
        beforeActivate: function(event, ui ) {
          var header = $(event.originalEvent.target).is('.ui-accordion-header');
          return header;
        },
      });
      $('#datepicker').datepicker({
        dateFormat: "yy-mm-dd",
        showOn: "both",
        buttonImage: "/static/clubs/img/icons/icon-calendar.svg",
        buttonImageOnly: true,
        buttonText: "Выберите дату",
        defaultDate: new Date(),
        minDate: 0,
        maxDate: +6,
        onSelect: function (dateText, inst) {
          var section = $(this).closest('.content-section');
          section.addClass('running');
          var col = $(this).closest('.col-12').next('.col-12');
          var date = $(this).datepicker('getDate');
          var dayOfTheWeek = weekday[date.getUTCDay()];
          $.ajax({
            type: 'GET',
            data: {day_of_the_week: dayOfTheWeek},
            success: function (data) {
              col.replaceWith(data);
              section.removeClass('running');
            },
            error: function () {
              console.log('error');
            },
          });
        }
      });
      $('.t-white .owl-carousel.photo-slider').owlCarousel({
        loop: false,
        items: 3,
        margin: 20,
      });
    }
  });

  // CLUB BASIC
  $('.club-create-form').on('click', '.submit', function (e) {
    e.preventDefault();
    $(this).attr('disabled', true);
    $(this).addClass('running');
    $.ajax({
      type: 'POST',
      data: $('.club-create-form').serialize(),
      success: function (data) {
        $('.club-create-form').remove();
        $('.final-screen').removeClass('is-hidden');
      },
      error: function (data) {
        // console.log(data);
      },
    });
  });

  $('.content-section').on('click', '.edit-button', function (e) {
    var club = $(this).data('id');
    var row = $(this).closest('.row');
    var nextRow = row.next('.row');
    var container = $(this).closest('.container-s');
    row.remove();
    nextRow.removeClass('is-hidden');
    $.ajax({
      type: 'GET',
      url: '/partner/club/'+club+'/',
      success: function (data) {
        container.append(data);
      },
      error: function () {},
    });
  });

  $('.container-s').on('click', '.club-update-form .submit', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var club = $(this).data('id');
    $.ajax({
      type: 'POST',
      url: '/partner/club/'+club+'/',
      data: $('.club-update-form').serialize(),
      success: function (data) {
        $('.club-update-form .confirm-msg').removeClass('is-hidden');
        disabled.attr('disabled', false);
        running.removeClass('running');
      },
      error: function () {
      },
    });
  });

  $('.container-s').on('click', '.tab-basic', function (e) {
    var club = $(this).data('id');
    var row = $(this).closest('.row');
    var nextRow = row.next('.row');
    $.ajax({
      type: 'GET',
      url: '/partner/club/'+club+'/',
      success: function (data) {
        nextRow.replaceWith(data);
      },
      error: function () {
      },
    });
  });

  // WORKING TIME
  $('.container-s').on('click', '.tab-working-time', function (e) {
    var club = $(this).data('id');
    var row = $(this).closest('.row');
    var nextRow = row.next('.row');
    $.ajax({
      type: 'GET',
      url: '/partner/club/'+club+'/working-time/',
      success: function (data) {
        nextRow.replaceWith(data);
      },
      error: function () {
      },
    });
  });

  $('.container-s').on('click', '.working-time .schedule-th', function (e) {
    if ( $('.working-time-form').length ) {
      $('.working-time-form').remove();
      var club = $(this).data('id');
      var day = $(this).data('day');
      var schedule = $(this).closest('.schedule');
      if ( $(this).find('.is-hidden').length ) {
        var curDay = $(this).find('.is-hidden').text();
        $.ajax({
          type: 'GET',
          url: '/partner/club/working-time/'+curDay+'/update/',
          success: function (data) {
            schedule.after(data);
          },
          error: function () {
          },
        });
      } else {
        $.ajax({
          type: 'GET',
          url: '/partner/club/'+club+'/working-time/'+day+'/create/',
          success: function (data) {
            schedule.after(data);
          },
          error: function () {
          },
        });
      }
    } else {
      var club = $(this).data('id');
      var day = $(this).data('day');
      var schedule = $(this).closest('.schedule');
      if ( $(this).find('.is-hidden').length ) {
        var curDay = $(this).find('.is-hidden').text();
        $.ajax({
          type: 'GET',
          url: '/partner/club/working-time/'+curDay+'/update/',
          success: function (data) {
            schedule.after(data);
          },
          error: function () {
          },
        });
      } else {
        $.ajax({
          type: 'GET',
          url: '/partner/club/'+club+'/working-time/'+day+'/create/',
          success: function (data) {
            schedule.after(data);
          },
          error: function () {
          },
        });
      }
    }
  });

  $('.container-s').on('click', '.working-time-form .submit', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    if ( $(this).data('workingtime') ) {
      var curDay = $(this).data('workingtime');
      $.ajax({
        type: 'POST',
        url: '/partner/club/working-time/'+curDay+'/update/',
        data: $('.working-time-form').serialize(),
        success: function (data) {
          // $('.working-time-form .confirm-msg').removeClass('is-hidden');
          $('.tab-working-time').trigger('click');
        },
        error: function () {
        },
      });
    } else {
      var club = $(this).data('id');
      var day = $(this).data('day');
      $.ajax({
        type: 'POST',
        url: '/partner/club/'+club+'/working-time/'+day+'/create/',
        data: $('.working-time-form').serialize(),
        success: function (data) {
          // $('.working-time-form .confirm-msg').removeClass('is-hidden');
          $('.tab-working-time').trigger('click');
        },
        error: function () {
        },
      });
    }
  });

  // HALL
  $('.container-s').on('click', '.tab-equipment', function (e) {
    var club = $(this).data('id');
    var row = $(this).closest('.row');
    var nextRow = row.next('.row');
    $.ajax({
      type: 'GET',
      url: '/partner/club/'+club+'/hall/',
      success: function (data) {
        nextRow.replaceWith(data);
      },
      error: function () {
      },
    });
  });

  $('.container-s').on('click', '.hall .add-hall', function (e) {
    var row = $(this).closest('.row');
    var club = $(this).data('id');
    $.ajax({
      type: 'GET',
      url: '/partner/club/'+club+'/hall/create/',
      success: function (data) {
        row.replaceWith(data);
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.hall .hall-submit', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var club = $(this).data('id');
    var borderBlock = $(this).closest('.border-block');
    $.ajax({
      type: 'POST',
      url: '/partner/club/'+club+'/hall/create/',
      data: $('.hall-form').serialize(),
      success: function (data) {
        // borderBlock.replaceWith(data);
        $('.tab-equipment').trigger('click');
        setTimeout(function() {
          $('.container-s .hall-view:last .ui-accordion-header').trigger('click');
        }, 300);
      },
      error: function () {
        console.log('error');
      },
    });
  });

  // $('.container-s').on('click', '.hall-view', function (e) {
  //   var hall = $(this).data('id');
  //   var view = $(this);
  //   $.ajax({
  //     type: 'GET',
  //     url: '/partner/club/hall/'+hall+'/update/',
  //     success: function (data) {
  //       view.replaceWith(data);
  //     },
  //     error: function () {
  //     },
  //   });
  // });

  $('.container-s').on('click', '.hall-update-btn', function (e) {
    if ( $(this).data('id') ) {
      var disabled = $(this).attr('disabled', true);
      var running = $(this).addClass('running');
      var hall = $(this).data('id');
      var row = $(this).closest('.hall-update-wrapper');
      $.ajax({
        type: 'GET',
        url: '/partner/club/hall/'+hall+'/update/',
        success: function (data) {
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.hall-update', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var hall = $(this).data('id');
    $.ajax({
      type: 'POST',
      url: '/partner/club/hall/'+hall+'/update/',
      data: $('.hall-update-form').serialize(),
      success: function (data) {
        // console.log(data);
        $('.tab-equipment').trigger('click');
        // $('.hall-update-form .confirm-msg').removeClass('is-hidden');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.hall-delete-button', function (e) {
    if ( $(this).data('id') ) {
      var disabled = $(this).attr('disabled', true);
      var running = $(this).addClass('running');
      var hall = $(this).data('id');
      var row = $(this).closest('.hall-update-wrapper');
      $.ajax({
        type: 'GET',
        url: '/partner/club/hall/'+hall+'/delete/',
        success: function (data) {
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.hall-delete', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var hall = $(this).data('id');
    var borderBlock = $(this).closest('.border-block');
    $.ajax({
      type: 'POST',
      url: '/partner/club/hall/'+hall+'/delete/',
      success: function (data) {
        // console.log('heolo');
        // borderBlock.remove();
        $('.tab-equipment').trigger('click');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.hall-delete-cancel', function (e) {
    $('.tab-equipment').trigger('click');
  });

  $('.container-s').on('click', '.add-game', function (e) {
    if ( $(this).data('id') ) {
      var hall = $(this).data('id');
      var row = $(this).closest('.row');
      $.ajax({
        type: 'GET',
        url: '/partner/club/hall/'+hall+'/game/create/',
        // data: {hall: hall},
        success: function (data) {
          // console.log(data);
          // $('.add-game-kind').before(data);
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.game-submit', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var hall = $(this).data('id');
    // var game = $(this).closest('.game-kind-form');
    var borderBlock = $(this).closest('.border-block');
    $.ajax({
      type: 'POST',
      url: '/partner/club/hall/'+hall+'/game/create/',
      data: $('.game-form').serialize(),
      success: function (data) {
        // borderBlock.replaceWith(data);
        $('.tab-equipment').trigger('click');
        // setTimeout(function() {
        //   $('.container-s .hall-view:last .ui-accordion-header').trigger('click');
        // }, 300);
        // $('#hall-accordion').accordion('refresh');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.game-update-btn', function (e) {
    if ( $(this).data('id') ) {
      var disabled = $(this).attr('disabled', true);
      var running = $(this).addClass('running');
      var game = $(this).data('id');
      var row = $(this).closest('.game-update-wrapper');
      $.ajax({
        type: 'GET',
        url: '/partner/club/hall/game/'+game+'/update/',
        success: function (data) {
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.game-update', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var game = $(this).data('id');
    $.ajax({
      type: 'POST',
      url: '/partner/club/hall/game/'+game+'/update/',
      data: $('.game-update-form').serialize(),
      success: function (data) {
        // console.log(data);
        $('.tab-equipment').trigger('click');
        // $('.hall-update-form .confirm-msg').removeClass('is-hidden');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.game-delete-button', function (e) {
    if ( $(this).data('id') ) {
      var disabled = $(this).attr('disabled', true);
      var running = $(this).addClass('running');
      var game = $(this).data('id');
      var row = $(this).closest('.game-update-wrapper');
      $.ajax({
        type: 'GET',
        url: '/partner/club/hall/game/'+game+'/delete/',
        success: function (data) {
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.game-delete', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var game = $(this).data('id');
    var borderBlock = $(this).closest('.border-block');
    $.ajax({
      type: 'POST',
      url: '/partner/club/hall/game/'+game+'/delete/',
      success: function (data) {
        // console.log('heolo');
        // borderBlock.remove();
        $('.tab-equipment').trigger('click');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.game-delete-cancel', function (e) {
    $('.tab-equipment').trigger('click');
  });

  $('.container-s').on('click', '.add-table', function (e) {
    if ( $(this).data('id') ) {
      var game = $(this).data('id');
      var row = $(this).closest('.row');
      $.ajax({
        type: 'GET',
        url: '/partner/club/hall/game/'+game+'/table/create/',
        success: function (data) {
          // console.log(data);
          // $('.add-table').before(data);
          // $('.add-table').closest('.row').closest('.col-24').before(data);
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.table-submit', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var game = $(this).data('id');
    var borderBlock = $(this).closest('.border-block');
    $.ajax({
      type: 'POST',
      url: '/partner/club/hall/game/'+game+'/table/create/',
      data: $('.table-form').serialize(),
      success: function (data) {
        // borderBlock.replaceWith(data);
        $('.tab-equipment').trigger('click');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.table-update-btn', function (e) {
    if ( $(this).data('id') ) {
      var disabled = $(this).attr('disabled', true);
      var running = $(this).addClass('running');
      var table = $(this).data('id');
      var row = $(this).closest('.table-update-wrapper');
      $.ajax({
        type: 'GET',
        url: '/partner/club/hall/game/table/'+table+'/update/',
        success: function (data) {
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.table-update', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var table = $(this).data('id');
    $.ajax({
      type: 'POST',
      url: '/partner/club/hall/game/table/'+table+'/update/',
      data: $('.table-update-form').serialize(),
      success: function (data) {
        // console.log(data);
        $('.tab-equipment').trigger('click');
        // $('.hall-update-form .confirm-msg').removeClass('is-hidden');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.table-delete-button', function (e) {
    if ( $(this).data('id') ) {
      var disabled = $(this).attr('disabled', true);
      var running = $(this).addClass('running');
      var table = $(this).data('id');
      var row = $(this).closest('.table-update-wrapper');
      $.ajax({
        type: 'GET',
        url: '/partner/club/hall/game/table/'+table+'/delete/',
        success: function (data) {
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.table-delete', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var table = $(this).data('id');
    var borderBlock = $(this).closest('.border-block');
    $.ajax({
      type: 'POST',
      url: '/partner/club/hall/game/table/'+table+'/delete/',
      success: function (data) {
        // console.log('heolo');
        // borderBlock.remove();
        $('.tab-equipment').trigger('click');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.table-delete-cancel', function (e) {
    $('.tab-equipment').trigger('click');
  });

  // PRICES
  $('.container-s').on('click', '.tab-prices', function (e) {
    var club = $(this).data('id');
    var row = $(this).closest('.row');
    var nextRow = row.next('.row');
    $.ajax({
      type: 'GET',
      url: '/partner/club/'+club+'/price/',
      success: function (data) {
        nextRow.replaceWith(data);
      },
      error: function () {
      },
    });
  });

  $('.container-s').on('click', '.price .add-price', function (e) {
    var row = $(this).closest('.row');
    var club = $(this).data('id');
    $.ajax({
      type: 'GET',
      url: '/partner/club/'+club+'/price/create/',
      success: function (data) {
        // row.before(data);
        row.replaceWith(data);
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.price-submit', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var club = $(this).data('id');
    var borderBlock = $(this).closest('.border-block');
    $.ajax({
      type: 'POST',
      url: '/partner/club/'+club+'/price/create/',
      data: $('.price-form').serialize(),
      success: function (data) {
        // borderBlock.replaceWith(data);
        $('.tab-prices').trigger('click');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.price-update-btn', function (e) {
    if ( $(this).data('id') ) {
      var disabled = $(this).attr('disabled', true);
      var running = $(this).addClass('running');
      var price = $(this).data('id');
      var row = $(this).closest('.price-update-wrapper');
      $.ajax({
        type: 'GET',
        url: '/partner/club/price/'+price+'/update/',
        success: function (data) {
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.price-update', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var price = $(this).data('id');
    $.ajax({
      type: 'POST',
      url: '/partner/club/price/'+price+'/update/',
      data: $('.price-update-form').serialize(),
      success: function (data) {
        // console.log(data);
        $('.tab-prices').trigger('click');
        // $('.hall-update-form .confirm-msg').removeClass('is-hidden');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.price-delete-button', function (e) {
    if ( $(this).data('id') ) {
      var disabled = $(this).attr('disabled', true);
      var running = $(this).addClass('running');
      var price = $(this).data('id');
      var row = $(this).closest('.price-update-wrapper');
      $.ajax({
        type: 'GET',
        url: '/partner/club/price/'+price+'/delete/',
        success: function (data) {
          row.replaceWith(data);
        },
        error: function () {
          console.log('error');
        },
      });
    }
  });

  $('.container-s').on('click', '.price-delete', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var price = $(this).data('id');
    var borderBlock = $(this).closest('.border-block');
    $.ajax({
      type: 'POST',
      url: '/partner/club/price/'+price+'/delete/',
      success: function (data) {
        // console.log('heolo');
        // borderBlock.remove();
        $('.tab-prices').trigger('click');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.price-delete-cancel', function (e) {
    $('.tab-prices').trigger('click');
  });

  $('.container-s').on('click', '.tab-photos', function (e) {
    var club = $(this).data('id');
    var row = $(this).closest('.row');
    var nextRow = row.next('.row');
    $.ajax({
      type: 'GET',
      url: '/partner/club/'+club+'/photo/',
      success: function (data) {
        nextRow.replaceWith(data);
      },
      error: function () {
      },
    });
  });

  $('.container-s').on('click', '.add-photo', function (e) {
    var row = $(this).closest('.row');
    var club = $(this).data('id');
    $.ajax({
      type: 'GET',
      url: '/partner/club/'+club+'/photo/create/',
      success: function (data) {
        row.replaceWith(data);
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.photo-submit', function (e) {
    e.preventDefault();
    var disabled = $(this).attr('disabled', true);
    var running = $(this).addClass('running');
    var formData = new FormData($('.photo-form')[0]);
    var club = $(this).data('id');
    var borderBlock = $(this).closest('.border-block');
    $.ajax({
      type: 'POST',
      url: '/partner/club/'+club+'/photo/create/',
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        // borderBlock.replaceWith(data);
        $('.tab-photos').trigger('click');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  // BOOKING
  var rowHalls;
  var rowGames;
  var rowDateTime;
  $('.content-section').on('click', '.hall-choice-button', function (e) {
    if ( $(this).data('id') ) {
      var hall = $(this).data('id');
      rowHalls = $(this).closest('.row');
      var section = $(this).closest('.content-section');
      section.addClass('running');
      $.ajax({
        type: 'GET',
        data: {hall: hall},
        success: function (data) {
          // console.log(row);
          rowHalls.detach();
          section.removeClass('running');
          section.append(data);

          // row.appendTo(sec);
        },
        error: function () {
          // console.log('error');
        },
      });
    }
  });

  $('.content-section').on('click', '.game-choice-button', function (e) {
    if ( $(this).data('id') ) {
      var game = $(this).data('id');
      rowGames = $(this).closest('.row');
      var section = $(this).closest('.content-section');
      section.addClass('running');
      $.ajax({
        type: 'GET',
        data: {game: game},
        success: function (data) {
          // console.log(row);
          rowGames.detach();
          section.removeClass('running');
          section.append(data);
        },
        error: function () {
          // console.log('error');
        },
      });
    }
  });

  if ( $('.content-section .time').hasClass('is-active') ) {

  } else {

  }
  $('.content-section').on('click', '.time', function (e) {
    if ( $('.content-section .time').hasClass('is-active') ) {
      if ( $(this).prev().hasClass('is-active') || $(this).next().hasClass('is-active') ) {
        $(this).toggleClass('is-active');
      } else {
        $(this).removeClass('is-active');
      }
    } else {
      // if ( ( $(this).prevAll('.time').is(':contains("00:00")') || $(this).is(':contains("00:00")') ) && ( $(this).prevAll('.time').is(':contains("00:00")').prev('.time') || $(this).is(':contains("00:00")').prev('.time') ) ) {
      if ( ( $(this).prevAll('.time').is(':contains("00:00")') || $(this).is(':contains("00:00")') ) ) {
        $(this).toggleClass('js-next');
      }

      $(this).toggleClass('is-active');
      $(this).nextAll("*:lt(3)").toggleClass('is-active');
    }
  });

  $('#dialog-create').on('click', '.time', function (e) {
    if ( $('#dialog-create .time').hasClass('is-active') ) {
      if ( $(this).prev().hasClass('is-active') || $(this).next().hasClass('is-active') ) {
        $(this).toggleClass('is-active');
      }
    } else {
      // if ( ( $(this).prevAll('.time').is(':contains("00:00")') || $(this).is(':contains("00:00")') ) && ( $(this).prevAll('.time').is(':contains("00:00")').prev('.time') || $(this).is(':contains("00:00")').prev('.time') ) ) {
      if ( ( $(this).prevAll('.time').is(':contains("00:00")') || $(this).is(':contains("00:00")') ) ) {
        $(this).toggleClass('js-next');
      }

      $(this).toggleClass('is-active');
      $(this).nextAll("*:lt(3)").toggleClass('is-active');
    }
  });

  // $('#dialog-create').on('click', '.time', function (e) {
  //   $(this).toggleClass('is-active');
  //   $(this).nextAll("*:lt(3)").toggleClass('is-active');
  // });

  $('.content-section').on('click', '.datetime-button', function (e) {
    var date = $(this).closest('.row').find('#datepicker').val();
    rowDateTime = $(this).closest('.row');
    var nextDay = 0
    if ( $(this).closest('.row').find('.timepicker').find('.time.is-active:first').hasClass('js-next') ) {
      var startTime = $(this).closest('.row').find('.timepicker').find('.time.is-active:first').text();
      nextDay = 1
    } else {
      var startTime = $(this).closest('.row').find('.timepicker').find('.time.is-active:first').text();
      nextDay = 0
    }
    var endTime = $(this).closest('.row').find('.timepicker').find('.time.is-active:last').next().text();
    var game = $(this).closest('.row').find('.game').text();
    var day = $(this).closest('.row').find('.day-of-the-week').text();
    var section = $(this).closest('.content-section');
    section.addClass('running');
    $.ajax({
      type: 'GET',
      data: {
        booking_date: date,
        next_day: nextDay,
        start_time: startTime,
        end_time: endTime,
        selected_game: game,
        week_day: day,
      },
      success: function (data) {
        rowDateTime.detach();
        // row.replaceWith(data);
        section.removeClass('running');
        section.append(data);
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.content-section').on('click', '.table-choice-button', function (e) {
    var table = $(this).data('id');
    var date = $(this).closest('.row').find('.start-date').text();
    var nextDay = $(this).closest('.row').find('.next-day').text();
    var startTime = $(this).closest('.row').find('.start-time').text();
    var endTime = $(this).closest('.row').find('.end-time').text();
    var day = $(this).closest('.row').find('.day-of-the-week').text();
    var section = $(this).closest('.content-section');
    section.addClass('running');
    row = $(this).closest('.row');
    $.ajax({
      type: 'GET',
      data: {
        booking_date: date,
        next_day: nextDay,
        start_time: startTime,
        end_time: endTime,
        selected_table: table,
        week_day: day,
      },
      success: function (data) {
        row.detach();
        // row.replaceWith(data);
        section.append(data);
        section.removeClass('running');
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.content-section').on('click', '.back-button-halls', function (e) {
    var section = $(this).closest('.content-section');
    $(this).closest('.row').remove();
    rowHalls.appendTo(section);
  });

  $('.content-section').on('click', '.back-button-games', function (e) {
    var section = $(this).closest('.content-section');
    $(this).closest('.row').remove();
    rowGames.appendTo(section);
  });

  $('.content-section').on('click', '.back-button-datetime', function (e) {
    var section = $(this).closest('.content-section');
    $(this).closest('.row').remove();
    rowDateTime.appendTo(section);
  });

  $('.content-section').on('click', '.booking-submit', function (e) {
    e.preventDefault();
    var dates = $(this).closest('.content-section').find('.booking-dates-wrapper');
    var form = $(this).closest('.booking-form');
    var section = $(this).closest('.content-section');
    section.addClass('running');
    $.ajax({
      type: 'POST',
      data: $('.booking-form').serialize(),
      success: function (data) {
        form.remove();
        dates.remove();
        section.removeClass('running');
        $('.final-screen-order').text(data.codeNumber);
        $('.final-screen').removeClass('is-hidden');
      },
      error: function () {
        // console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.extranet-hall', function (e) {
    var hall = $(this).data('id');
    var row = $(this).closest('.row');
    $.ajax({
      type: 'GET',
      data: {hall: hall},
      success: function (data) {
        row.after(data);
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('.container-s').on('click', '.extranet-game', function (e) {
    var game = $(this).data('id');
    var row = $(this).closest('.row');
    $.ajax({
      type: 'GET',
      data: {game: game},
      success: function (data) {
        row.after(data);
      },
      error: function () {
        console.log('error');
      },
    });
  });

  // BOOKING EXTRANET
  $('#dialog-create').on('click', '.extranet-datetime-button', function (e) {
    // var game = 1;
    // var nextDay = 0;
    // if ( $(this).closest('.row').find('.timepicker').find('.time.is-active:first').hasClass('js-next') ) {
    //   var startTime = $(this).closest('.row').find('.timepicker').find('.time.is-active:first').text();
    //   nextDay = 1;
    // } else {
    //   var startTime = $(this).closest('.row').find('.timepicker').find('.time.is-active:first').text();
    //   nextDay = 0;
    // }
    var startTime = $(this).closest('.timepicker-wrapper').find('.timepicker').find('.time.is-active:first').text();
    var endTime = $(this).closest('.timepicker-wrapper').find('.timepicker').find('.time.is-active:last').next().text();
    var table = $(this).closest('.timepicker-wrapper').find('.extranet-booking-table').text();
    var club = $(this).closest('.timepicker-wrapper').find('.extranet-booking-club').text();
    var date = $(this).closest('.timepicker-wrapper').find('.extranet-booking-day').text();
    var day = $(this).closest('.timepicker-wrapper').find('.day-of-the-week').text();
    var wrapper = $(this).closest('.timepicker-wrapper');
    var dialog = $(this).closest('#dialog-create');
    $.ajax({
      type: 'GET',
      url: '/partner/'+club+'/booking/',
      data: {
        booking_date: date,
        week_day: day,
        selected_table: table,
        club: club,
        start_time: startTime,
        end_time: endTime,
      },
      success: function (data) {
        // wrapper.addClass('is-hidden');
        // $('#dialog-create .dialog-form').removeClass('is-hidden');
        // row.after(data);
        wrapper.detach();
        // row.replaceWith(data);
        dialog.append(data);
      },
      error: function () {
        console.log('error');
      },
    });
  });

  $('#dialog-create').on('click', '.extranet-booking-submit', function (e) {
    var cost = $(this).closest('.content-section').find('.cost');
    var club = $(this).closest('.booking-form').find('.extranet-booking-club').text();
    // console.log(club);
    e.preventDefault();
    var form = $(this).closest('.booking-form');
    $.ajax({
      type: 'POST',
      url: '/partner/'+club+'/booking/',
      data: $('.booking-form').serialize(),
      success: function (data) {
        $('#dialog-create').dialog('close');
        location.reload();
        // console.log(data);
        // form.remove();
        // $('.final-screen-order').text(data.codeNumber);
        // $('.final-screen').removeClass('is-hidden');
        // cost.addClass('is-hidden');
      },
      error: function () {
        // console.log('error');
      },
    });
  });

  $('#dialog-update').on('click', '.extranet-booking-submit', function (e) {
    var booking = $(this).closest('.booking-form').find('.extranet-booking-id').text();
    // console.log(club);
    e.preventDefault();
    var form = $(this).closest('.booking-form');
    $.ajax({
      type: 'POST',
      url: '/partner/booking/'+booking+'/',
      data: $('.booking-form').serialize(),
      success: function (data) {
        $('#dialog-update').dialog('close');
        location.reload();
      },
      error: function () {
        // console.log('error');
      },
    });
  });

  // $('.container-s').on('click', '.extranet-table', function (e) {
  //   var table = $(this).data('id');
  //   var row = $(this).closest('.row');
  //   $.ajax({
  //     type: 'GET',
  //     data: {table: table},
  //     success: function (data) {
  //       row.after(data);
  //     },
  //     error: function () {
  //       console.log('error');
  //     },
  //   });
  // });

});
