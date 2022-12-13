
function redirectSuccess() {// Inform the user that their entry has been saved.

  // Select everything but the layout from the template.
  const mainBodyDiv = document.getElementById("MainBody");

  // Clear %block content% data from the page.
  mainBodyDiv.innerHTML = "";

  // Create the 'success' view.
  mainBodyDiv.appendChild( document
                           .createElement("h2")
                           .setAttribute("id", "SuccessBanner")
			   .innerHTML = "Success!!";            );
  // PAGE BREAK
  mainBodyDiv.appendChild( document.createElement("br"); );

  // Create the 'home' button.
  mainBodyDiv.appendChild( document
                           .createElement("button")
                           .setAttribute("id", "homeButton")
                           .setAttribyte("onclick", "https://guyyatsu.me")
		           .innerHTML = "home"; );
  // PAGE BREAK
  mainBodyDiv.appendChild( document.createElement("br"); );
}


function createSaveButton() {
  // Define a button that allows a way out of the editing loop.
  // --When clicked, this button executes a function that:
  //    -Clears the templating provided by this page.
  //    -Re-Writes the page MainBody with confirmation of acceptance.
  //    -Redirects the visitor back to the top of the domain.

  // Select the section of the page dedicated to our shenanigans.
  const submissionButtonDiv = document.getElementById("SubmissionButtons")

  // Add a 'save' button that returns the redirectSuccess function onClick.
  submissionButtonDiv.appendChild( document
		                   .createElement("button")
                                   .setAttribute("id", "saveButton")
                                   .setAttribute("onclick", "redirectSuccess()")
                                   .innerHTML = "save";                          );
}


function createSubmitButton() {
  // Define a button that allows for re-submission of form data.
  // --Sets itself up to loop indefinitely until the visitor decides
  // they're satisfied with their input.

  // Select the section of the page dedicated to our shenanigans.
  const submissionButtonDiv = document.getElementById("SubmissionButtons")

  // Create a button to update information before saving.
  submissionButtonDiv.appendChild( document
		                   .createElement("button")
                                   .setAttribute("id", "submitButton")
                                   .setAttribute("type", "submit")
                                   .setAttribute("onclick", "UpdateForm()")
                                   .innerHTML = "submit";                   );
}


function UpdateForm() {

  // Let the user know the page is responding.
  document.getElementById("UpdateConfirmation")
	  .innerHTML = "Your submission has been saved; but you may still edit it.";

  // CLEAR the 'SubmisionButtons' div and re-create them.
  document.getElementById("SubmissionButtons")
          .innerHTML = "";

  createSaveButton();
  createSubmitButton();
  redirectSuccess();
}
