(function () {
    var dragNDrop = document.querySelector('.form-input-dnd');
    var fileInput = document.querySelector('[name=image]');
    var fileLabelInput = document.querySelector('.input_file_label');

    var addHighlight = function () {
        dragNDrop.classList.add('form-input-dnd--highlight');
    };

    var removeHighlight = function () {
        dragNDrop.classList.remove('form-input-dnd--highlight')
    };

    dragNDrop.addEventListener('dragenter', function (e) {
        addHighlight();
        e.preventDefault();
    });
    dragNDrop.addEventListener('dragover', function (e) {
        addHighlight();
        e.preventDefault();
    });
    dragNDrop.addEventListener('dragleave', function (e) {
        removeHighlight();
        e.preventDefault();
    });
    dragNDrop.addEventListener('drop', function (e) {
        removeHighlight();
        fileInput.files = e.dataTransfer.files;
        if (fileInput.files.length > 0) {
            fileLabelInput.innerHTML = fileInput.files[0].name;
        }
        e.preventDefault();
    });

    fileInput.addEventListener('change', function (e) {
        if (fileInput.files.length > 0) {
            fileLabelInput.innerHTML = fileInput.files[0].name;
        }
    });
})();