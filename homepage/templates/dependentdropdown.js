// // $(function(){
    
// //   var $cat = $("#cat"),
// //       $subcat = $("#subcat");
  
// //   $cat.on("change",function(){
// //       var _rel = $(this).val();
// //       $subcat.find("option").attr("style","");
// //       $subcat.val("");
// //       if(!_rel) return $subcat.prop("disabled",true);
// //       $subcat.find("[rel="+_rel+"]").show();
// //       $subcat.prop("disabled",false);
// //   });
  
// // });
// // // var $cat = $("#category1"),
// // //     $subcat = $(".subcat");

// // // var optgroups = {};

// // // $subcat.each(function(i,v){
// // //   var $e = $(v);
// // //   var _id = $e.attr("id");
// // //   optgroups[_id] = {};
// // //   $e.find("optgroup").each(function(){
// // //     var _r = $(this).data("rel");
// // //     $(this).find("option").addClass("is-dyn");
// // //     optgroups[_id][_r] = $(this).html();
// // //   });
// // // });
// // // $subcat.find("optgroup").remove();

// // // var _lastRel;
// // // $cat.on("change",function(){
// // //     var _rel = $(this).val();
// // //     if(_lastRel === _rel) return true;
// // //     _lastRel = _rel;
// // //     $subcat.find("option").attr("style","");
// // //     $subcat.val("");
// // //     $subcat.find(".is-dyn").remove();
// // //     if(!_rel) return $subcat.prop("disabled",true);
// // //     $subcat.each(function(){
// // //       var $el = $(this);
// // //       var _id = $el.attr("id");
// // //       $el.append(optgroups[_id][_rel]);
// // //     });
// // //     $subcat.prop("disabled",false);
// // // });

// <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
// function dynamicdropdown(listindex)
// {
//     switch (listindex)
//     {
//     case "mass" :
//         document.getElementById("status").options[0]=new Option("Select status","");
//         document.getElementById("status").options[1]=new Option("g","g");
//         document.getElementById("status").options[2]=new Option("pg","pg");
//         document.getElementById("status").options[3]=new Option("ng","ng");
//         document.getElementById("status").options[4]=new Option("μg","μg");
//         document.getElementById("status").options[5]=new Option("mg","mg");
//         document.getElementById("status").options[6]=new Option("cg","cg");
//         // document.getElementById("status").options[2]=new Option("pg","pg");
//         // document.getElementById("status").options[2]=new Option("pg","pg");
//         // document.getElementById("status").options[2]=new Option("pg","pg");
//         // document.getElementById("status").options[2]=new Option("pg","pg");
//         // document.getElementById("status").options[2]=new Option("pg","pg");
//         break;
//     case "moles" :
//         document.getElementById("status").options[0]=new Option("Select status","");
//         document.getElementById("status").options[1]=new Option("Hello","open");
//         document.getElementById("status").options[2]=new Option("Hi","delivered");
//         document.getElementById("status").options[3]=new Option("Hey","shipped");
//         break;
//     case "volume" :
//         document.getElementById("status").options[0]=new Option("Select status","");
//         document.getElementById("status").options[1]=new Option("Hello","open");
//         document.getElementById("status").options[2]=new Option("Hi","delivered");
//         document.getElementById("status").options[3]=new Option("Hey","shipped");
//         break;
//     case "molarity" :
//         document.getElementById("status").options[0]=new Option("Select status","");
//         document.getElementById("status").options[1]=new Option("Hello","open");
//         document.getElementById("status").options[2]=new Option("Hi","delivered");
//         document.getElementById("status").options[3]=new Option("Hey","shipped");
//         break;
//     case "density" :
//         document.getElementById("status").options[0]=new Option("Select status","");
//         document.getElementById("status").options[1]=new Option("Hello","open");
//         document.getElementById("status").options[2]=new Option("Hi","delivered");
//         document.getElementById("status").options[3]=new Option("Hey","shipped");
//         break;
//     }
//     return true;
// }