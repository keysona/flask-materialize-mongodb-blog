/**
 * Created by key on 16-5-1.
 */
$( document ).ready(function(){
    $('.button-collapse').sideNav();

    var markdown_body = $(".markdown-body")
    // design markdown image
    markdownImage();
    markdownHeadersNav();
    scrollHandler();

    $('.scrollspy').scrollSpy();

    $(".post-title").mouseover(function(){
      $(this).addClass("z-depth-2");
    });

    $(".post-title").mouseout(function(){
      $(this).removeClass("z-depth-2");
    });

    $('.collapsible').collapsible({
      accordion : false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
    });
    $(".toc-wrapper").width($(".info").width());
    $(".toc-wrapper").pushpin({ top: $(".toc-wrapper").offset().top });
});

function markdownImage()
{
    var imgs = $('.markdown-body img').addClass('responsive-img materialboxed').css("opacity","0");
    $('.materialboxed').materialbox();
    var i;
    var options = [];
    for(i = 0; i < imgs.length ; i++){
        var id = "img-" + i;
        $(imgs[i]).attr("id",id);
        id = "#" + id;
        options.push({
            selector: id,
            offset: 10,
            callback: function(id) {
                return function () {
                    Materialize.fadeInImage(id);
                }
            }(id)
        });
    }
    Materialize.scrollFire(options);
}

function markdownHeadersNav() {
    var headers = $(".markdown-body").find("h1,h2,h3,h4,h5,h6");
    var headersNav = $(".section .table-of-contents");
    var i;
    for(i = 0; i < headers.length; i++){
        var header = $(headers[i]);
        var title = header.text();

        var div = $("<div></div>").attr("id",title).addClass("section scrollspy")
        header.after(div);
        var tmp = header.next().next();
        div.append($(headers[i]));
        while(!tmp.is("h1,h2,h3,h4,h5,h6")){
          var current = tmp;
          tmp = tmp.next()
          div.append(current);;
          if(tmp.length == 0){
            console.log("hello");
            break;
          }
        }
        var aTag = $("<li></li>")
        aTag.append($("<a></a>").attr("href","#"+title).text(title));
        headersNav.append(aTag);
    }
}

function scrollHandler(){
    var didScroll;
    var lastScrollTop = 0;
    var delta = 5;
    var navbarHeight = $('#navbar').outerHeight();
    $(window).scroll(function(event){
        didScroll = true;

        // scroll to top
        if($(this).scrollTop() > 100){
          $("#rocket").fadeIn();
        }else{
          $("#rocket").fadeOut();
        }
    });

    $("#rocket").click(function(){
      $('html,body').animate({scrollTop:0},1000);
    });


    // Hide Header on on scroll down
    setInterval(function() {
        if (didScroll) {
            hasScrolled();
            didScroll = false;
        }
    }, 250);

    function hasScrolled() {
        var st = $(this).scrollTop();
        // alert(st);
        // Make sure they scroll more than delta
        if(Math.abs(lastScrollTop - st) <= delta)
            return;

        // If they scrolled down and are past the navbar, add class .nav-up.
        // This is necessary so you never see what is "behind" the navbar.
        if (st > lastScrollTop && st > navbarHeight){
            // Scroll Down
            $('#navbar').clearQueue().animate({
                top: "-" + navbarHeight + "px"
            },250);
        } else {
            // Scroll Up
            $('#navbar').clearQueue().animate({
                top:0 + "px"
            },250);;
        }
        lastScrollTop = st;
      }
}
