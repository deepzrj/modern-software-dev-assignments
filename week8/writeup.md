# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Submission Details

Name: Deepthy
SUNet ID: Not applicable
Citations: **Bolt documentation: https://support.bolt.new/building/intro-bolt**

This assignment took me about **4** hours to do. 


## App Concept 
```
Task Board is a small CRUD application for tracking personal development tasks. Users can create tasks with a title, description, status, and priority; view the full task list; edit existing tasks; delete tasks; and receive validation feedback when required fields are missing. Each version keeps the same user-facing feature set while using a different technology stack and persistence approach.
```


## Version #1 Description
```
APP DETAILS:
===============
Folder name: bolt-task-board
AI app generation platform: Bolt.new
Tech Stack: React + Vite
Persistence: Browser localStorage
Frameworks/Libraries Used: React, React DOM, Vite
(Optional but recommended) Screenshots of core flows: Not included

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: The main issue was keeping persistence simple enough for a generated single-page app. I used localStorage so the app can run without a backend or external database.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): The most useful prompt details were the exact data model, required CRUD flows, and validation rules. Keeping the prompt focused on one primary resource avoided unnecessary features.

c. Approximate time-to-first-run and time-to-feature metrics: About 10 minutes to first run and 35 minutes to complete CRUD, persistence, styling, and README notes.
```

## Version #2 Description
```
APP DETAILS:
===============
Folder name: flask-task-board
AI app generation platform: None
Tech Stack: Python Flask + Jinja templates
Persistence: Local JSON file, tasks.json
Frameworks/Libraries Used: Flask, Jinja
(Optional but recommended) Screenshots of core flows: Not included

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: The main issue was preserving form values after validation errors. I passed submitted form data back into the template so the user does not lose input when a title is missing.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): This version was manual, but the same implementation prompt worked well: one resource, required title validation, simple persistence, and server-rendered CRUD routes.

c. Approximate time-to-first-run and time-to-feature metrics: About 15 minutes to first run and 45 minutes to complete routes, templates, JSON persistence, styling, and README notes.
```

## Version #3 Description
```
APP DETAILS:
===============
Folder name: node-task-board
AI app generation platform: None
Tech Stack: Node.js HTTP server + Vanilla JavaScript frontend
Persistence: Local JSON file, tasks.json
Frameworks/Libraries Used: Node.js built-in http, fs, path, crypto modules
(Optional but recommended) Screenshots of core flows: Not included

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: The main issue was avoiding extra dependencies while still providing a complete API. I used Node's built-in HTTP module and kept the API surface to GET, POST, PUT, and DELETE task routes.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): The strongest guidance was specifying the JSON API contract and matching frontend flows. Explicit validation and persistence requirements kept the implementation scoped.

c. Approximate time-to-first-run and time-to-feature metrics: About 10 minutes to first run and 40 minutes to complete the API, frontend integration, persistence, styling, and README notes.
```

## Personal Learnings & Takeaways

Week 8 gave me experience working with the same application across different stacks—React, Flask, and Node. This helped me see how similar concepts like CRUD operations are implemented in different environments.

I learned that while the tools and syntax change, the core logic remains the same. It also highlighted trade-offs between simplicity and flexibility, such as using localStorage versus backend persistence.

Overall, this week helped me understand how transferable development concepts are across different technologies.

## Personal Learnings & Takeaways

Week 8 involved implementing the same application across multiple stacks: React, Flask, and Node.

I observed that core concepts remain consistent:
- CRUD operations (Create, Read, Update, Delete)
- Data validation
- State management

However, implementation differs:
- React uses **client-side state and localStorage**
- Flask uses **server-rendered templates and backend logic**
- Node uses **API-driven architecture with HTTP endpoints**

This demonstrated the concept of **abstraction**, where the same functionality is expressed through different technologies.

The key takeaway was that understanding fundamental concepts is more important than mastering any single framework.
