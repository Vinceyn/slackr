# Principles we decided to follow

As a flexible agile software engineering team, we decided to follow as much as possible some principles. We find these principles paramount to have a code extensible, reusable, maintainable, understandable and testable. We tried to achieved it through abstraction, and remove the most of the hard code part.
However, we didn't want to fall into a coding that is too abstract, which can lead to less readability and overcomplex functions/structures. 

We tried to follow these principles during this iteration refactoring:
* Don't repeat yourself: If some portions of the code were repeated in our code, we decided to factorize them into functions who would have a self-explanotory name
* Keep it stupid, simple: We tried to remove the overcomplex code. If we couldn't, we decided to split it up into helper functions, or with a readable indentation
* You aren't gonna need it: We removed the unused imports, and the helper functions that were not used but still put on the code in the case we would need them. 

We also did small improvents in various parts of the code, by reading it again, and cross-checking each other code to have differents feedbacks.
Even though our test were already pretty solid, we decided to add test playing on the invariant properties of our classes
We used pytest coverage to ensure that all of our code was tested, and we improved our test thanks to it.
We used pylint to have feedback on our code style and we change our code according to its review.

# Changes in the code

## Search
* Creation of a helper function to check the arguments
* Removed unused variables
* Created a test using invariant property

## Channel
* Creation of helper functions to check the arguments
* Creation of helper functions to factorize the code 
* Simplification of functions (channel_messages..)
* Removed comments to make the code more readable
* Added Consistency, by removing the tests about u_id_exists, the existence of u_id was already checked in auth
* Increased readibility by removing useless variable, or adding some variables if the code was too "one-lined"
* Removed unused functions
* Created a test using invariant property of channel_id

