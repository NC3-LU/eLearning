$(document).ready(function () {
    let sidebarState = 'expanded';

    $('#sidebarToggle').click(function () {
        $('#sidebar .d-none').toggleClass('d-sm-inline');
        $('#logo_small, #open_sidebar').toggleClass('d-sm-none');
        if (sidebarState === 'expanded') {
            $('#sidebar').addClass('minimized');
            sidebarState = 'minimized';
        } else {
            $('#sidebar').removeClass('minimized');
            sidebarState = 'expanded';
        }
    });
});
