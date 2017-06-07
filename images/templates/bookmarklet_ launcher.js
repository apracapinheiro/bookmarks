/**
 * Created by 81135998191 on 07/06/2017.
 */

(function () {
    if (window.myBookmarklet !== undefined) {
        myBookmarklet();
    }
    else {
        document.body.appendChild(document.createElement('script')).src = 'http://127.0.0.1:8200/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 99999999999999999999);
    }
})();