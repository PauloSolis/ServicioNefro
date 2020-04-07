
$( document ).ready(function() {
  $(".sidebar-hide").removeClass("hidden");
  $(".sidebar-hide").toggle();
});

$("#sideopener").click(toggle);

    let sidebar = false;
    function toggle() {
      if (sidebar){
        closeNav();
        $(".sidebar-hide").fadeToggle(50);
      }else{
        openNav();
        $(".sidebar-hide").delay(400).fadeToggle(90);
      }
      sidebar = !sidebar;
    }


    function openNav() {
      document.getElementById("mySidenav").style.width = "200px";
      document.getElementById("main").style.marginLeft = "200px";
      document.getElementById("sideopener").innerHTML = "<i class='fas fa fa-times icon-size'></i>";
      document.getElementById("sideopener").style.paddingLeft = "85%";
      items = document.getElementsByClassName("sidebar-list");
      for(i=0; i<items.length; i++) {
        items[i].style.marginLeft = "10%";
      }
    }
    function closeNav() {
      document.getElementById("mySidenav").style.width = "40px";
      document.getElementById("main").style.marginLeft = "40px";
      document.getElementById("sideopener").innerHTML = "<i class='fas fa-angle-double-right icon-size'></i>";
      document.getElementById("sideopener").style.paddingLeft = "11px";
      items = document.getElementsByClassName("sidebar-list");
      for(i=0; i<items.length; i++) {
        items[i].style.marginLeft = "1px";
      }
    }
