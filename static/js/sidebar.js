function toggleSidebar() {
    $('#sidebar .d-none').toggleClass('d-sm-inline');
    $('#sidebar .d-inline').toggleClass('d-sm-none');
    $('#sidebar').addClass('minimized');
    $('#logo_small, #open_sidebar').toggleClass('d-sm-none');
    $('#logo_small').removeClass('d-sm-none');
    $('#logo_large').addClass('d-none');
    $('#start-button').addClass('d-none');

    console.log('sidebar toggled');
}

$(document).ready(function () {
    let windowsWidth = $(window).width();
    let sidebarState = JSON.parse(document.getElementById('sidebarState').textContent);
    console.log(sidebarState);

    if (sidebarState === 'minimized') {
        toggleSidebar();
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $('#sidebarToggle').on("click", function () {
    
        $('#sidebar .d-none').toggleClass('d-sm-inline');
        $('#sidebar .d-inline').toggleClass('d-sm-none');
        if (sidebarState === 'expanded') {
            $.ajax({
                type: "POST",
                url: 'sidebar_state/?state=minimized',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (data) {
                    $('#sidebar').addClass('minimized');
                    $('#logo_small').removeClass('d-sm-none');
                    $('#logo_large').addClass('d-none');
                    $('#start-button').addClass('d-none');
                    sidebarState = 'minimized';
                    console.log('after ajax:', sidebarState);
                },
                error: function (data) {
                    console.log(data);
                }
            });
            
        } else {
            $.ajax({
                type: "POST",
                url: 'sidebar_state/?state=expanded',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (data) {
                    $('#sidebar').removeClass('minimized');
                    $('#logo_small').addClass('d-sm-none');
                    $('#logo_large').removeClass('d-none');
                    $('#start-button').removeClass('d-none');
                    sidebarState = 'expanded';
                    console.log('after ajax:', sidebarState);                    
                },
                error: function (data) {
                    console.log(data);
                }
            });
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
