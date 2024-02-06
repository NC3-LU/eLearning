$(document).ready(function () {
    function toggleSidebar() {
        $('#sidebar .d-none').toggleClass('d-sm-inline');
        $('#sidebar .d-inline').toggleClass('d-sm-none');
        $('#logo_small, #open_sidebar, #language_selector_minimized').toggleClass('d-sm-none');
    }

    let sidebarState = JSON.parse(document.getElementById('sidebarState').textContent);
    toggleSidebar()
    if (sidebarState === 'expanded') {
        $('#sidebar').removeClass('minimized');
    } else {
        $('#sidebar').addClass('minimized');
    }




    $('#sidebarToggle').click(function () {
        toggleSidebar()
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
});
