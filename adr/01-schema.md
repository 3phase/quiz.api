# Decision for the application schema

## Background

The application needs continuous collaboration between multiple data entities which need to be associated with the user.
The entities then need to be re-used by other users.

## Decision

As the application is going to be requiring interactions between multiple entities working in parallel, we are going to
use a db (tbd).
An initial, very high-level draft of the database schema would look like this:

| **Quiz**                  |
|---------------------------|
| questions  --> Question[] |
| created_by --> User       |
| managed_by --> User[]     |       // tbd

| **Question**            |
|-------------------------|
| text -> str             |
| quiz -> Quiz            |
| options -> QuizOption[] |
| prev -> Question        |         // tbd
| next -> Question        |         // tbd

| **QuestionOption**   |
|----------------------|
| text -> str          |
| correct -> bool      |
| question -> Question |

| **Invitation**    |
|-------------------|
| quiz -> Quiz      |
| from_user -> User |
| to_user -> User   |

| **User**   |
|------------|
| uid -> str |

| **QuestionOption**   |
|----------------------|
| text -> str          |
| correct -> bool      |
| question -> Question |

| **Answer**                          |
|-------------------------------------|
| question -> Question                |
| questionOptions -> QuestionOption[] |
| user -> User                        |

| **Score**        |
|------------------|
| user -> User     |
| quiz -> Quiz     |
| points -> number |











