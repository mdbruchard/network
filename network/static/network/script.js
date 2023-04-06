document.addEventListener('DOMContentLoaded', function() {

  // Hide the edit div by default
editHidden()
})

// Function to hide the edit div
 function editHidden() {

   // Storing the div in a variable
   let div = document.querySelectorAll('.post-edit');

   // For all div with "post-edit" class
   for (let i = 0; i < div.length; i++) {

     // Display none
     div[i].style.display = 'none';
   }
 }

// Editing the post
function editShow(id) {

  // Display the right contents when the edit button is press
  document.querySelector(`#post-edit-${id}`).style.display = 'block';
  document.querySelector(`#p${id}`).style.display = 'none';

  // Get the form e when submit it...
  document.querySelector(`#edit-form-${id}`).onsubmit = () => {

    // Fetch the post with that ID
    fetch(`/edit/${id}`, {
      method: 'POST',
      body: JSON.stringify({
        post: document.querySelector(`#edit${id}`).value
      })
    })
    .then(response => response.json())
    .then(response => {


      console.log(response)

      document.querySelector(`#post-edit-${id}`).style.display = 'none';
      document.querySelector(`#p${id}`).style.display = 'block';
      document.querySelector(`#post-text-${id}`).innerHTML =
      document.querySelector(`#edit${id}`).value;
    })
return false;

}
}

function like(id) {


    fetch(`/likes/${id}`)
    .then(response => response.json())
    .then(post => {

      console.log(post.like);

      document.querySelector(`#num-likes-${id}`).innerHTML = post.like.length;



    })


}
