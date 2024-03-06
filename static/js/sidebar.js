$(document).ready(function () {
    let windowsWidth = $(window).width();
    let sidebarState = 'expanded';

    $('#sidebarToggle').click(function () {
        $('#sidebar .d-none').toggleClass('d-sm-inline');
        $('#sidebar .d-inline').toggleClass('d-sm-none');
        $('#logo_small, #open_sidebar').toggleClass('d-sm-none');
        if (sidebarState === 'expanded') {
            $.get( 'sidebar_state/' + '?state=minimized', function() {
            })
            $('#sidebar').addClass('minimized');
            sidebarState = 'minimized';
        } else {
            $.get( 'sidebar_state/' + '?state=expanded', function() {
            })
            $('#sidebar').removeClass('minimized');
            sidebarState = 'expanded';
        }
    });

    $(window).on('resize', function(){
        var win = $(this);
        if (win.width() <= 992 && sidebarState === 'expanded') {
            $('#sidebarToggle').trigger( "click" );
        }else if (win.width() > 992 && sidebarState === 'minimized'){
            $('#sidebarToggle').trigger( "click" );
        }
    });

    if (windowsWidth <= 992 && sidebarState === 'expanded'){
        $('#sidebarToggle').trigger( "click" );
    }
});
