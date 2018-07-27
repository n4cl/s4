$(function() {

  var esURL = sssConfig.esServerName + "es/_search";
  var sssURL = "s3search.cgi";

  $("input[type='reset']")
    .after("<span id='total'>0</span>件")
    .after("&nbsp;")
    .after("<input type='button' id='esearch' value='拡張検索'>")
    .after("&nbsp;")
    .after("表示件数:&nbsp;<input type='number' id='maxRows' min='1' max='100' value='50' style='width:3rem'>")
    .after("&nbsp;");

  $("#esearch").click(function() {
    var resultPos = $("form[name='formtop']").next("table");
    resultPos.children("form[name='_form']").remove();
  
    var keyword = $("input[name='memo']").val();
    var esData = {
            "query":{
              "bool":{
                "must":[
                  {
                    "query_string":{
                      "default_field":"text",
                      "query":keyword,
                    }
                  },
                ],
              }
            },
            "from":0,
            "size":$("#maxRows").val(),
            };
    $.ajax({
      url: esURL,
      type: "post",
      contentType: "application/json",
      data: JSON.stringify(esData),
    }).done(function(data) {
      var sssData = {
        cmd: "searchnippodetail",
        nid: [],
      };

      $("#total").text(data.hits.total);

      $.each(data.hits.hits, function(i, nippo) {
        sssData.nid.push(nippo._id);
      });

      $.get(sssURL, $.param(sssData, true), function(data) {
        $("form", data).each(function() {
          resultPos.append(this);  
        });
      });
    });
  });
});
