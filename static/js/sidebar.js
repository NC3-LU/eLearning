$(document).ready(function () {
    let sidebarState = 'expanded';

    $('#sidebarToggle').click(function () {
        $('#sidebar .d-none').toggleClass('d-sm-inline');
        $('#sidebar .d-inline').toggleClass('d-sm-none');
        $('#logo_small, #open_sidebar, #language_selector_minimized').toggleClass('d-sm-none');
        if (sidebarState === 'expanded') {
            $('#sidebar').addClass('minimized');
            sidebarState = 'minimized';
        } else {
            $('#sidebar').removeClass('minimized');
            sidebarState = 'expanded';
        }
    });
});
