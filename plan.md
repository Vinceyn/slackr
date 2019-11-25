# Plan for Iteration 2
Iteration 2 will involve implementing many of the functions in the interface given to us in the spec. Since we already have a spec and tests to match, we should be able to develop everything in parallel, with each of us implementing functions for one component.

However, it would appear that the auth module is heavily depended on by all the other modules, so we will likely work on implementing the `auth_*` functions, before splitting up and completing the rest of the functions in parallel.

## Timeline and Division of Tasks
The specifications for Iteration 2 will be released in week 4, and we will have until week 7 to work on the iteration. We will likely only be able to begin on the second iteration after the Week 4 lab, effectively giving us three and a half weeks for this iteration.

The following diagram shows our timeline for the iteration:
![Timeline](https://gitlab.cse.unsw.edu.au/COMP1531/19T3/W17A-We_Push_to_Master/raw/master/docs/Timeline.png "Our Iteration 2 expected timeline")

Each person was assigned the same module that they completed the tests for, which we determine will likely be more efficient. We also determined that the `channel` module will take the most work, so both Avin and Vincent were assigned to that. `user` will likely take the least amount of work, so after Eddie completes that module he will assist with either `channel` or `messages`, whichever is more in need of help.

Our assumptions on the amount of work required for each module was based on the complexity of writing tests for the modules in Iteration 1.

In the final week, we will spend the first half implementing any miscellaneous functionality, such as `search`, `standup_*` and `admin_userpermission_change`. This is also the stage where we will begin to test how well our modules integrate with each other, and fix any miscellaneous issues there. (Ideally, we will begin this stage before week 7, but this is the worst case scenario.)

In the last half of the week, we will extensively test the iteration, both using the tests from Iteration 1 and through user-side testing. We will take this time to address any miscellaneous bugs or functionality issues with the iteration.

## Use of software tools to assist the team
In iteration 1, we have used 3 software tools to coordinate ourselves:

* Gitlab
* Trello
* Group chat

We'll use the same tools for iteration 2. We hadn't got any coordination problems in iteration 1 thanks to these software, so we'll keep them. The Trello, which was not really useful during iteration 1 due to a lot of changes in our work repartition, will surely be helpful in iteration 2 as each member will work independently in his part. 