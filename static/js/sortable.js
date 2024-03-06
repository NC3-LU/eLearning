$(function () {
    $(".sortable").sortable({
        connectWith: ".sortable",
        cursor: "move",
        handle: ".handle",
    }).disableSelection();
});
