$(document).ready(function () {
    $('#id_handle').parent().siblings('p[class=help]').text(
        'The handle must be written in the format "[language_code]_menu_live", e.g. "en_menu_live", for the menu to ' +
        'be live on the website. You can use other handles, e.g. "en_oldmenu", to store other draft menus without ' +
        'them getting displayed.'
    ).css({'color': 'red'});

    $('#tab-content:contains("Download PO file and input translations offline")')
        .find('>:first-child')
        .prepend('<p style="margin-left: 50px; color: red; font-weight: bold;">' +
            'Use the "STOP TRANSLATION" option if you want to translate additional fields ' +
            'such as: survey/poll/quiz answers, index page description, recommended content, ' +
            'search engine friendly title, search description, lead image, icon.' +
            '</p>')
});


