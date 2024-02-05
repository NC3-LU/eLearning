$(document).ready(function () {
    const languageSelector = $('#language_selector');

    languageSelector.focus(() => {
        languageSelector.find('option').each(function () {
            $(this).text($(this).data('fullname'));
        });
    });

    languageSelector.change(() => {
        const selectedOption = languageSelector.find('option:selected');
        selectedOption.text(selectedOption.val());
        languageSelector.closest('form').submit();
    });

    languageSelector.blur(() => {
        languageSelector.find('option').each(function () {
            $(this).text($(this).val());
        });
    });

    languageSelector.focusout(() => {
        const selectedOption = languageSelector.find('option:selected');
        selectedOption.text(selectedOption.val());
    });
});