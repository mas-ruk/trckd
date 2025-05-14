document.addEventListener('DOMContentLoaded', function() {
    let csvData = null; // Variable to store CSV content
    const fileInp = document.getElementById('filename');
    const csvPaste = document.getElementById('csvPaste');

    // disable / enable other input method
    function toggleInputs(fileActive) {
        fileInp.disabled = !fileActive;
        csvPaste.disabled = fileActive;
        if (fileActive) {
            csvPaste.value = '';
        } else {
            fileInp.value = '';
        }
    }

    // grab csv from csv file
    fileInp.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            toggleInputs(true);
            const reader = new FileReader();
            reader.onload = function(e) {
                csvData = e.target.result;

            }
            reader.readAsText(file);
        }
    });

    // Paste input handler
    csvPaste.addEventListener('input', function() {
        if (this.value) {
            toggleInputs(false);
            csvData = this.value;
        }
    });

    // grab csv text from pastebin
    function formatCSVText() {
        document.getElementById('submitCsv').addEventListener('click', () => {
            let csvText = document.getElementById('csvPaste');
            csvData = csvText.value; // Store pasted CSV in the same variable
        });
    }

    // placeholder until we get add to collection working
    document.getElementById('submitCsv').addEventListener('click', () => {
         if (csvData) {
             // Process csvData and send to database
         }
    });
});