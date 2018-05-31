





// keep track of the ""
var current_document = ""

function highlightWords(hash) {
    var offset = 0;
    var original;

    $.each(hash, function(val) {
        original = $(".doc-content").html();
        var length = original.length;
        var before = original.substring(0,val[0]+offset);
        var replace = original.substring(val[0]+offset, val[1]+offset);
        var after = original.substring(val[1]+offset,length);
        var final = before + "<span class='highlight'>" + replace + "</span>" + after;
        offset += 33;
        $(".doc-content").html(final);
    });
}

function getSelectionText() {
    var text = "";
    var activeEl = document.activeElement;
    var activeElTagName = activeEl ? activeEl.tagName.toLowerCase() : null;
    if (
      (activeElTagName == "textarea") || (activeElTagName == "input" &&
      /^(?:text|search|password|tel|url)$/i.test(activeEl.type)) &&
      (typeof activeEl.selectionStart == "number")
    ) {
        text = activeEl.value.slice(activeEl.selectionStart, activeEl.selectionEnd);
    } else if (window.getSelection) {
        text = window.getSelection().toString();
    }

    return text;
}


// function getSelectionOfText() {
//   var sel = window.getSelection()
//   var activeEl = document.activeElement;
//   var text = activeEl.innerHTML
//   var start = sel.anchorOffset
//   var end = sel.extentOffset
//   console.log(start, end)
  //highlightWords([start, end])

  // var parts = [
  //   text.substring(0, start),
  //   "<span class='highlight'>",
  //   text.substring(start, end),
  //   "</span>",
  //   text.substring(end, text.length)
  // ]
  //
  // activeEl.innerHTML = parts.join("")

  // var
  // var start = window.getSelection().extentOffset
  // var end = window.getSelection().anchorOffset
  //
  // sel.anchorNode.textContent.substring(
  //   start,
  //   end
  // )
}

function getSelectedText(){
  var selection = window.getSelection()
  var start = selection.anchorOffset
  var end = selection.extentOffset
  var container = selection.anchorNode.parentNode
  var text = container.textContent.substring(start, end)
  return [text, start, end, container]
}

function offerAnnotation(text){
  var container = document.getElementById('dynamic-select')
  console.log(text)
  if (typeof text != 'undefined' && text.length > 0) {
      container.style.visibility = 'visible'
      var annotate_content = document.getElementById('annotate_content')
      annotate_content.value = text
    } else{
      container.style.visibility = 'hidden'
    }
}
document.onmouseup = function() {
  var arr = getSelectedText()
  var text = arr[0]
  var start = arr[1]
  var end = arr[2]
  var container = arr[3]
  offerAnnotation(text)
};


function submitAnnotation(){
    var selected_text = getSelectedText()
    var data = {'text': selected_text, 'doc': doc}
    $.post(
        '/submit',
        doc,
        function(results){next()}
     )
}

function apply_annotations(annotations){
  annotations.map(a => {
    var text = a[0]
    var x0 = a[1]
    var x1 = a[2]
  })
}

function apply_value(content, container_id){
  var container = document.getElementById(container_id)
  container.textContent = content
}



function apply(title, doc, annotations){
  apply_value(doc, "doc-content")
  apply_value(title, "doc-title")
  apply_annotations(annotations)
}

function next(){
  $.get(
    "/next",
    function(result){
      var doc = result['doc']
      var title = result['title']
      var annotations = result['annotations']
      apply(title, doc, annotations)
    }
  )
}

function annotate(){
  var arr = getSelectedText()
  var text = arr[0]
  var start = arr[1]
  var end = arr[2]
  var container = arr[3]
  apply_annotations([[text, start, stop]])
  // var matched_text = getSelectionText()
  // var doc_container = document.getElementById("article")
  // var pattern = new RegExp(matched_text, "g")
  // var repl = "<span class='highlight'>" + matched_text + "</span>"
  // doc_container.innerHTML = doc_container.innerHTML.replace(pattern, repl)
}

function prev(){
  $.get(
    "/prev",
    function(result){
      var doc = result['doc']
      var title = result['title']
      var annotations = result['annotations']
      apply(title, doc, annotations)
    }
  )
}
