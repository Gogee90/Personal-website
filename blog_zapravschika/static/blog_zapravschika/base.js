function changeId(id, div) {
    let url_name = $(id).attr('href');
    history.pushState(null, document.title, url_name);
    let urlPath = window.location.pathname;
    $("#summernote").load(`${url_name} ${div}`, function () {
        $(".em_text").css("display", "none").fadeIn("fast");
        $(".content_section_01").css("display", "none").fadeIn("slow");
        let title = $("h3.em_text").text();
        switch (urlPath) {
            case "/articles/":
                document.title = "Последние статьи";
                break;
            case "/news/":
                document.title = "Новости сайта";
                break;
            case "/":
                document.title = "Ремонт, заправка, восстановление картриджей";
                break;
            case "/faq/":
                document.title = "Часто задаваемые вопросы";
                break;
            case "/coordinates":
                document.title = "Как нас найти";
                break;
            default:
                document.title = title;
        }

        $(".disqus").append(function () {
            var disqus_config = function () {
                this.page.url = window.location.href;  // Replace PAGE_URL with your page's canonical URL variable
                this.page.title = title;
            };

            (function() { // DON'T EDIT BELOW THIS LINE
                var d = document, s = d.createElement('script');
                s.src = 'https://refill56-ru.disqus.com/embed.js';
                s.setAttribute('data-timestamp', +new Date());
                (d.head || d.body).appendChild(s);
            })();
        });
    });
}

function getPassword() {
    let password = document.getElementById("id_password").value;
    let password2 = document.getElementById("id_password2").value;
    let props = {"display": "none", "color": "red", "text-align": "center"};
    if (password !== password2 || password < password2) {
        $(".registration").show(function() {
            $(this).append("<p>Пароли не совпадают!</p>").css(props).fadeIn("slow");
        });
    } else if ($("#id_email").val() == '' || $("#id_first_name").val() == '' || $("#id_last_name").val() == '') {
        $(".registration").show(function() {
            $(this).append("<p>Одно из полей не заполнено!</p>").css(props).fadeIn("slow");
        });
    } else {
        let formData = $(".registration").serializeArray();
        $.post({
            url: "registration/",
            data: formData,
            success: $.modal.close()
        });
    };
};

$('a.open-modal').click(function(event) {
  $(this).modal({
    fadeDuration: 250
  });
  return false;
});

window.onpopstate = function (e) {
    e.preventDefault();
    this.location.reload();
}

$(document).ready(function() {
    $(".main_page").css("display", "none").fadeIn(300);
    $(".em_text").css("display", "none").fadeIn("fast");
    $(".content_section_01").css("display", "none").fadeIn("slow");
});

/*$("option").on("click", function(e) {
    let optionVal = $(this).val();
    e.preventDefault();
    $("#id_recipient").append(optionVal);
});*/

$("#id_recipient_list").change(function() {
    var str = "";
    $("select option:selected").each(function() {
        str += $(this).text() + ", ";
    });
    $("#id_recipient[name='recipient']").val(str);
}).trigger("change");