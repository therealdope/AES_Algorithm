(function() {
    var customDelay = 800;
    var fadeDuration = 300;
    var box = document.getElementById('box');

    window.addEventListener('load', function() {
        setTimeout(function() {
            var loader = document.querySelector('.loader');
            if (loader) {
                // Set a transition for opacity so it fades out smoothly
                loader.style.transition = 'opacity ' + fadeDuration + 'ms ease';
                loader.style.opacity = '0';
                // Remove the loader from the DOM after the fade-out completes
                setTimeout(function() {
                    if (loader.parentNode) {
                        loader.parentNode.removeChild(loader);
                    }
                    if (box && box.parentNode) {
                        box.parentNode.removeChild(box);
                    }
                }, fadeDuration);
            }
        }, customDelay);
    });
})();