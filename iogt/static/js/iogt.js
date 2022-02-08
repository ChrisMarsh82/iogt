function validateFileUpload(fileInput, file_size_threshold) {
    if (!fileInput.files || !fileInput.files[0])
        return true;
    else {
        var file = fileInput.files[0];
        if (file.size >= file_size_threshold)
            return confirm('The file you have uploaded exceeds ' + Math.round(file_size_threshold / 1024 / 1024) + 'mb. ' +
                'This will prohibit access to the file in a low bandwidth setting, may restrict feature phone access, or ' +
                'violate your mobile network operator agreements. To reduce file size, try resizing and compressing your ' +
                'file. Do you want to continue?');
    }

    return true;
}

function validateFreeBasicsFileUpload(fileInput, file_size_threshold) {
    if (!fileInput.files || !fileInput.files[0])
        return true;
    else {
        var file = fileInput.files[0];
        if (file.size >= file_size_threshold)
            alert(`File size exceeds facebook free basics limit (${file_size_threshold / 1024}KB).`);
    }

    return true;
}

$(document).ready(() => {
    const searchFormHolder = $('.search-form-holder');
    const commentForm = $('.comments__form');
    const commentLikeHolders = $('.like-holder');
    const commentReplyLinks = $('.reply-link');
    const chatbotBtnContainers = $('.chatbot-button-container');
    const offlineAppBtns = $('.block-offline_app_button');
    const questionnaireSubmitBtns = $('.survey-page__btn');
    const progressHolder = $('.progress-holder');
    const changeDigitalPinBtn = $('.change-digital-pin');
    const loginCreateAccountBtns = $('.login-create-account-btn');
    const logoutBtn = $('.logout-btn');

    const disableForOfflineAccess = () => {
        searchFormHolder.hide();
        commentForm.hide();
        commentLikeHolders.attr('style', 'display: none !important');
        commentReplyLinks.hide();
        chatbotBtnContainers.hide();
        offlineAppBtns.hide();
        questionnaireSubmitBtns.hide();
        progressHolder.hide();
        changeDigitalPinBtn.hide();
        loginCreateAccountBtns.hide();
        logoutBtn.hide();
    };

    const enableForOnlineAccess = () => {
        searchFormHolder.show();
        commentForm.show();
        commentLikeHolders.attr('style', 'display: inline-block !important');
        commentReplyLinks.show();
        chatbotBtnContainers.show();
        offlineAppBtns.show();
        questionnaireSubmitBtns.show();
        progressHolder.show();
        changeDigitalPinBtn.show();
        loginCreateAccountBtns.show();
        logoutBtn.show();
    };

    $(window).on('offline', () => disableForOfflineAccess());
    $(window).on('online', () => enableForOnlineAccess());

    if (!window.navigator.onLine) {
        disableForOfflineAccess();
    }
});
