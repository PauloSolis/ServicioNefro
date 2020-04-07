var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
    // This function will display the specified tab of the form...
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    //... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").hidden = true;
        document.getElementById("guardar").hidden = false;
    } else {
        document.getElementById("nextBtn").hidden = false;
        document.getElementById("guardar").hidden = true;
    }
    //... and run a function that will display the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form... :
    if (currentTab >= x.length) {
        //...the form gets submitted:
        document.getElementById("regForm").submit();
        return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var i, valid = true;
    // A loop that checks every input field in the current tab:

    for (i = 1; i < 11; i++) {
        p1 = document.getElementById("id_p" + i + "_0");
        p2 = document.getElementById("id_p" + i + "_1");
        p3 = document.getElementById("id_p" + i + "_2");
        p4 = document.getElementById("id_p" + i + "_3");
        p5 = document.getElementById("id_p" + i + "_4");

        if (p1.checked || p2.checked || p3.checked || p4.checked || p5.checked) {
            document.getElementById("p" + i).removeAttribute("style")
        }else{
            document.getElementById("p" + i).style.color = "red"
            valid = false;
        }
    }

    if (currentTab == 1){
        p11 = document.getElementById("id_p11");
        p12 = document.getElementById("id_p12");
        p13 = document.getElementById("id_p13");

        if (p11.value == ""){
            document.getElementById("invalido11").hidden= false;
            valid = false;
        }else{
            document.getElementById("invalido11").hidden= true;
        }
        if (p12.value == ""){
            document.getElementById("invalido12").hidden= false;
            valid = false;
        }else{
            document.getElementById("invalido12").hidden= true;
        }
        if (p13.value == ""){
            document.getElementById("invalido13").hidden= false;
            valid = false;
        }else{
            document.getElementById("invalido13").hidden= true;
        }
    }

    if(currentTab == 2){
        p14 = document.getElementById("id_p14_0");
        p14_1 = document.getElementById("id_p14_1");
        p14_2 = document.getElementById("id_p14_2");

        if (p14.checked || p14_1.checked || p14_2.checked ) {

        }else{

            valid = false;
        }
    }


    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    else{
        alert("Es necesario llenar todo los campos");
    }
    return valid;

}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active-step", "");
    }
    //... and adds the "active" class to the current step:
    x[n].className += " active-step";
}
