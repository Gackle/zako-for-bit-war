var semantic = $('.ui .container');
semantic.menu = {};

// ready event
semantic.menu.ready = function() {

  // selector cache
  var
    $dropdownItem = $('.main.container .menu .dropdown .item'),
    $popupItem    = $('.main.container .popup.example .browse.item'),
    $menuItem     = $('.main.container .menu a.item, .menu .link.item').not($dropdownItem),
    $dropdown     = $('.main.container .menu .ui.dropdown'),

    $defineItem   = $menuItem.filter('#define'),
    $exampleItem  = $menuItem.filter('#example'),
    $tokenTipItem = $('.main.container .menu .ui.dropdown#token').find('div.item'),
    // alias
    handler = {

      activate: function() {
        if(!$(this).hasClass('dropdown browse')) {
          $(this)
            .addClass('active')
            .closest('.ui.menu')
            .find('.item')
              .not($(this))
              .removeClass('active')
          ;
        }
      },

      toggle: function() {
        // 隐藏当前面板
        $('.ui.grid .ui.segment.content').hide();
        $('#' + this.id + "-content").show();
      },

      loadTokenData: function() {
        // 隐藏当前面板
        $('.ui.grid .ui.segment.content').hide();
        var $content = $('#token-content');
        $($content.find('h2')[0]).text($(this).text());
        $($content.find('h3')[0]).next().text(token_dict[$(this).text()]["title"]);
        $($content.find('h3')[1]).next().text(token_dict[$(this).text()]["usage"]);
        $($content.find('h3')[2]).next().text(token_dict[$(this).text()]["description"]);
        $content.show();
      }

    }
  ;

    

  $dropdown
    .dropdown({
      on: 'hover'
    })
  ;

  $('.main.container .ui.search')
    .search({
      type: 'category',
      apiSettings: {
        action: 'categorySearch'
      }
    })
  ;

  $('.school.example .browse.item')
    .popup({
      popup     : '.admission.popup',
      hoverable : true,
      position  : 'bottom left',
      delay     : {
        show: 300,
        hide: 800
      }
    })
  ;

  $popupItem
    .popup({
      inline   : true,
      hoverable: true,
      popup    : '.fluid.popup',
      position : 'bottom left',
      delay: {
        show: 300,
        hide: 800
      }
    })
  ;

  $menuItem
    .on('click', handler.activate)
  ;

  $defineItem
    .on('click', handler.toggle);

  $exampleItem
    .on('click', handler.toggle);

  $tokenTipItem
    .on('click', handler.loadTokenData);
};


// attach ready event
$(document)
  .ready(semantic.menu.ready)
;