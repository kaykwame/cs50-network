document.addEventListener('DOMContentLoaded', function () {

  // Add event listeners to the edit buttons on each of the current user's posts.
  var editbuttons = document.getElementsByClassName('editpost');
  for (i = 0; i < editbuttons.length; i++) {
      editbuttons[i].addEventListener("click", editpost);
    }
});

function editpost() {

  // Select elements with class name 'newpostform'
  let editForm = document.querySelectorAll('.newpostform')

  // clone form
  let newForm = editForm[0].cloneNode(true)
    const element = event.target;
    const parent = element.parentElement;

    // If element clicked is an edit button, get contents of post, replace post with newpostform and prefill it with contents of post.
    if (element.className === 'btn btn-primary editpost'){
      childrxn = parent.children;
      content = childrxn[3].innerHTML;
      parent.replaceWith(newForm);
      document.getElementsByName('Post_content')[1].innerText = content

      document.getElementsByClassName('btn btn-primary submitbutton')[1].className = "btn btn-primary submitbutton1";

      // Get id of parent element of edit button.
      var pre_id = parent.id;

      // Split id into 2 strings at designated character which is 't' in this case.
      var res = pre_id.split("t");

      // Second string is the id of the post
      var id = res[1]

      // Add an event listener to an element (button) with class name 'submitbutton1'.
      document.querySelectorAll('.submitbutton1')[0].addEventListener('click', () => save_edit(`${id}`, parent, newForm));
    }
  }


function save_edit(id, parent, newForm){
  // Prevent default action of form
  event.preventDefault();

  // Get edited content
  var newcontent = document.getElementsByName('Post_content')[1].value;

    // Send PUT request to update contents of post with new/edited content.
      fetch(`/post/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        Post_content: `${newcontent}`
    })
})
// Replace old content with new content in element.
.then(parent.children[3].innerHTML = newcontent)
// Replace form (textarea) with new/updated element (new content).
.then(newForm.replaceWith(parent))
}


function likepost(){
    var element = event.target;
    var id = element.parentElement.id;
    var href = '/like/'
    event.preventDefault();

    // Send ajax request with post id
    $.ajax({
      url: href,
      data: {
        id: id,
      },
      // After a successful operation, reload the element to update number of likes.
      success: function () {
        $("#kwame" + id).load(` #${id}`);
      },
    });
  }
