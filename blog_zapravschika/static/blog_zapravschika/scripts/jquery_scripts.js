<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>


$(".ssilka_articles").click(() => {
    $("#summernote").load("{% url 'detailed_article' post.slug %}");
});
