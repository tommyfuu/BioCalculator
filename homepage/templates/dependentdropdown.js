var $cat = $("#category1"),
    $subcat = $(".subcat");

var optgroups = {};

$subcat.each(function(i,v){
  var $e = $(v);
  var _id = $e.attr("id");
  optgroups[_id] = {};
  $e.find("optgroup").each(function(){
    var _r = $(this).data("rel");
    $(this).find("option").addClass("is-dyn");
    optgroups[_id][_r] = $(this).html();
  });
});
$subcat.find("optgroup").remove();

var _lastRel;
$cat.on("change",function(){
    var _rel = $(this).val();
    if(_lastRel === _rel) return true;
    _lastRel = _rel;
    $subcat.find("option").attr("style","");
    $subcat.val("");
    $subcat.find(".is-dyn").remove();
    if(!_rel) return $subcat.prop("disabled",true);
    $subcat.each(function(){
      var $el = $(this);
      var _id = $el.attr("id");
      $el.append(optgroups[_id][_rel]);
    });
    $subcat.prop("disabled",false);
});