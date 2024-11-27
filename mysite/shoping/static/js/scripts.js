/*!
* Start Bootstrap - Personal v1.0.1 (https://startbootstrap.com/template-overviews/personal)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-personal/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project



$(document).ready(function() {
    // Pritaikyti Select2 abiem elementams
    $('#category').select2({
        placeholder: "-- Pasirinkite --",
        allowClear: true, // Leisti išvalyti pasirinkimą
        width: '100%'    // Užtikrina, kad plotis atitiktų formos elementą
    });

    $('#product').select2({
        placeholder: "-- Pasirinkite --",
        allowClear: true, // Leisti išvalyti pasirinkimą
        width: '100%'    // Užtikrina, kad plotis atitiktų formos elementą
    });
});