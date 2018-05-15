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

function offerAnnotation(text){
  var container = document.getElementById('annotate-button')

  if (text.length > 0){
    container.style.visibility = 'visible'
    var annotate_content = document.getElementById('annotate_content')
    annotate_content.value = text
  } else{
    container.style.visibility = 'hidden'
  }
}
document.onmouseup = function() {
  var text = getSelectionText()
  offerAnnotation(text)
};
