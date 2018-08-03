
// keep track of the ""

// a dictionary of span ids as keys, and values are a list of annotation objects
var annotations = {}
var original_document = ""
var annotation_additions = {}

function range(end=1, start=0) {
    return (new Array(end - start)).fill(undefined).map((_, i) => i + start);
}

function restartAnnotations(){
    annotations = {}
}

function windowReload(){
    restartAnnotations()
    docbox = document.getElementById('doc-content')
    doc = docbox.textContent
    insertDoc(doc)
    docbox.addEventListener('mouseup', showMenu)
    autocomplete(document.getElementById("myInput"), []);

}

function next(){
  $.get(
    "/next",
    function(result){
      var doc = result['doc']
      var title = result['title']
      var annotations = result['annotations']
      setDataToScreen(doc, title, annotations)
    }
  )
  clearLabels()
}

function prev(){
  $.get(
    "/prev",
    function(result){
      var doc = result['doc']
      var title = result['title']
      var annotations = result['annotations']
      setDataToScreen(doc, title, annotations)
    }
  )
  clearLabels()  
}

spanset = {}
labels = {}
referenceSpans = {}
selectedRange = null
referenceSpanID = null

function deleteLabel(referenceID){
  label = labels[referenceSpanID]
  label.remove()
  delete labels[referenceSpanID]
}

function unhighlight(referenceSpanID){
  function inner() {
    relatedspans = spanset[referenceSpanID]
    span = document.getElementById(referenceSpanID)
    console.log("You clicked span " + referenceSpanID)
    console.log("Current color is " + span.style.backgroundColor)
    console.log("Related spans include: " + relatedspans)
    for (var i = 0; i < relatedspans.length; ++i){
        sid = relatedspans[i]
        s = document.getElementById(sid)
        s.style = null
        s.onclick = null
        delete spanset[sid]
    }
  }
  return inner
}



function highlightSpan(span, relatedspans, referenceSpanID){
    ids = relatedspans.map(s => s.id)
    span.style.backgroundColor = "#f18973";
    spanset[span.id] = ids
    referenceSpans[span.id] = referenceSpanID
    span.onclick = unhighlight(referenceSpanID)
    return span
}

Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
}
NodeList.prototype.remove = HTMLCollection.prototype.remove = function() {
    for(var i = this.length - 1; i >= 0; i--) {
        if(this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}

function getCurrentLabelValues(){
    results = []
    Object.keys(labels).forEach(function(referenceSpanID) {
        labelName = labels[referenceSpanID].textContent
        results.push(labelName)
    });
    return results
}

function createLabelPrompt(coords){

    labelNames = getCurrentLabelValues()
    InputForm = document.getElementById('myInput')
    SubmitButton = document.getElementById('myInputSubmit')
    ResetButton = document.getElementById('myInputReset')
    InputContainer = document.getElementById('inputContainer')

    showMenu()

    autocomplete(InputForm, labelNames);
    //autocomplete(InputForm, ['hamburger']);
}

function hideMenu(){

    InputForm = document.getElementById('myInput')
    SubmitButton = document.getElementById('myInputSubmit')
    ResetButton = document.getElementById('myInputReset')
    InputContainer = document.getElementById('inputContainer')

    ResetButton.style.visibility = 'hidden'
    SubmitButton.style.visibility = 'hidden'
    InputContainer.style.visibility = 'hidden'
    InputForm.style.visibility= 'hidden'
}




function showMenu(){

    selection = document.getSelection()
    range = selection.getRangeAt(0)
    coords = range.getBoundingClientRect()
    contents = range.extractContents()
    spans = Array.from(contents.children)

    if (spans.length > 1) {

        referenceSpanID = spans[0].id
        range = highlightSelected(range, coords, spans, referenceSpanID)
        InputForm = document.getElementById('myInput')
        SubmitButton = document.getElementById('myInputSubmit')
        ResetButton = document.getElementById('myInputReset')
        InputContainer = document.getElementById('inputContainer')

        ResetButton.style.visibility = 'visible'
        SubmitButton.style.visibility = 'visible'
        InputContainer.style.visibility = 'visible'
        InputForm.style.visibility= 'visible'

        ResetButton.style.left = coords.left + window.pageXOffset+"px";
        ResetButton.style.top = coords.bottom  + window.pageYOffset+"px";
        ResetButton.onclick = generateCancel(referenceSpanID)

        InputContainer.style.left = coords.left + window.pageXOffset+"px";
        InputContainer.style.top = coords.bottom  + window.pageYOffset+"px";

        InputForm.style.left = coords.left + window.pageXOffset+"px";
        InputForm.style.top = coords.bottom  + window.pageYOffset+"px";

        SubmitButton.style.left = coords.left + window.pageXOffset+"px";
        SubmitButton.style.top = coords.bottom  + window.pageYOffset+"px";
        SubmitButton.onclick = generateSubmit(referenceSpanID, coords)

        selectedRange = range
        console.log("Words selected at " + coords.left + " " + coords.bottom)
        console.log("Submit button location: " + SubmitButton.style.left)

        //showBoxAt(coords, referenceSpanID)
    } else {
        fragment = document.createDocumentFragment();
        fragment.append(contents)
        range.insertNode(fragment)
    }
}

function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}

function generateSubmit(referenceSpanID, coords){
    function inner(){
        console.log("Calling Submit with referenceID: " + referenceSpanID)
        InputForm = document.getElementById('myInput')
        label = InputForm.value
        console.log("Attempting to submit " + label)
        //InputForm.value = ""
        hideMenu()
        message = document.createElement('div');

        height = document.getElementById(referenceSpanID).offsetHeight
        message.style.cssText = "position:absolute; color: red";
        message.style.left = coords.left + window.pageXOffset+"px";
        message.style.top = coords.top + .75 * height + window.pageYOffset+"px";
        message.innerHTML = label;
        message.id = "label_" + referenceSpanID
        document.body.append(message);
        labels[referenceSpanID] = message

        inputVals = Array.from(Object.values(labels))
        labelVals = inputVals.filter(onlyUnique).map(label => label.textContent)
        autocomplete(InputForm, labelVals)

    }

    return inner
}

function repositionLabelBySpanId(spanid){
  console.log("Repositioning " + spanid)
  s = document.getElementById(spanid)
  left = s.offsetLeft
  top = s.offsetTop //- s.offsetHeight
  label = labels[spanid]
   //1.1 * height
  label.style.left = left + window.pageXOffset+"px";
  label.style.top = top +  .75 * s.offsetHeight + window.pageYOffset+"px";
}

function repositionLabels(){
    spansWithLabel = Object.keys(labels).map(repositionLabelBySpanId)
}

function generateCancel(referenceSpanID){
    function inner(){
        //InputForm = document.getElementById('myInput')
        //InputForm.textContent = ""
        hideMenu()
        console.log("Going to call unhighlight with ref id " + referenceSpanID)
        unhighlight(referenceSpanID)
    }

    return inner
}


function highlightSelected(range, coords, spans, referenceSpanID){
    referenceSpanID = spans[0].id
    // extracting contents creates ghost elements, lets delete them.
    fid = spans[0].id
    lid = spans.slice(-1)[0].id
    console.log(lid)
    document.getElementById(fid).remove();
    document.getElementById(lid).remove();

    hspans = []
    fragment = document.createDocumentFragment();

    for (var i = 0; i < spans.length; ++i){
        hspan = highlightSpan(spans[i], spans, referenceSpanID)
        fragment.append(hspan)
    }
    range.insertNode(fragment)
    //showBoxAt(coords, referenceSpanID)
    return range
}


function clearLabels(){
  Object.entries(labels).map(tuple =>{
    ref_id = tuple[0]
    label = tuple[1]
    label.remove()
    delete labels[ref_id]
  })
}



function setDataToScreen(doc, title, annotations){
    console.log("Setting data to screen")
    insertDoc(doc)
    insertTitle(title)

}

function insertTitle(title){
    containerInsert(title, "doc-title")
}

function zip(){

  let lengths = Array.from(arguments).map(i => i.length)
  let shortest = Math.min(...lengths)

  let result = Array()

  for (var i = 0; i < shortest; ++i){
        let elem = Array()
        for (var j = 0; j < arguments.length; ++j){
            elem.push(arguments[j][i])
        }
        result.push(elem)
  }

  return result
}


function insertDoc(doc){

    function range(end=1, start=0) {
        return (new Array(end - start)).fill(undefined).map((_, i) => i + start);
    }

    function toSpan(char, id){
        let span = document.createElement("span");
        span.id = id
        span.innerText = char

        return span
    }

    docContainer = document.getElementById('doc-content')
    docContainer.innerHTML = ""
    id_iter = range(doc.length)
    iterable = zip(doc, id_iter)
    iterable.map(
        tuple => docContainer.appendChild(toSpan(tuple[0], "text_"+tuple[1]))
     )

}

var tokenize = function(s) {
    discardEmpty = true
    pattern = new RegExp(/(\w+|[а-я0-9_]+|\.|\!|\'|\"")/i);
    results = s.split(pattern);
    return results
}


function bundleToJson(){
  results = {}
  docContainer = document.getElementById('doc-content')
  spans = Array.from(docContainer.children)

  spans.map(span => {
    entry = {'text': span.textContent, 'entity': null, 'label_id': null}
    results[span.id] = entry
  })

  Object.entries(labels).map(tuple => {
    referenceID = tuple[0]
    label = tuple[1]
    related = Array.from(spanset[referenceID])
    related.map(spanid => {
      results[spanid]['entity'] = label.textContent
      results[spanid]['label_id'] = label.id
    })
  })
  return JSON.stringify(Object.values(results))
}

function submitDocument(){
  payload = {"document": bundleToJson()}
  $.post(
      '/submit',
      payload,
      function(response){
        console.log(response)
      }
   )
}

function containerInsert(content, container_id){
  var container = document.getElementById(container_id)
  container.textContent = content
}

window.onload = windowReload
window.onresize = repositionLabels

// NEW STUFF BELOW
function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}
