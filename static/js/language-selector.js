$(document).ready(function () {
    $('#language_selector_expanded, #language_selector_minimized').change(function () {
        $(this).closest('form').submit();
    });
});
