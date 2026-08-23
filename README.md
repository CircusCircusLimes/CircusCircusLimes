# DishCourse

DishCourse is a social discussion forum built for food lovers — from everyday cooks and foodies to social media chefs and anyone who simply enjoys talking about food.

Users can create posts, share recipes and ideas, participate in conversations through comments and reactions, share media, and communicate directly with other members of the community.

DishCourse was developed by the **CircusCircusLimes** team as part of the **Zip Code Wilmington Data Engineering Program**.

---

## Features

### Posts
- Create and view discussion posts
- Create public or private posts
- Use plain text or Markdown formatting
- Add image and video links to posts
- Browse posts within discussion subforums

### Comments & Reactions
- Comment on discussion posts
- React to posts with Like, Dislike, or Heart
- React to comments with Like, Dislike, or Heart
- View reaction counts
- Change or remove an existing reaction

### Communication
- Send direct messages to other users
- Access conversations with other community members

### User Features
- User registration and authentication
- User profiles
- User settings
- Avatar support

### User Interface
- DishCourse custom branding
- Bootstrap-based interface
- Responsive page layouts
- Navigation for forums, posts, messages, profiles, and settings

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Web application framework |
| Flask-SQLAlchemy | ORM and database integration |
| Flask-Login | User authentication |
| MySQL 8.4 | Relational database |
| PyMySQL | Python MySQL database driver |
| Jinja2 | HTML templating |
| HTML / CSS | Application structure and styling |
| Bootstrap | Responsive UI components |
| JavaScript | Client-side interaction |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Gunicorn | Application server |
| Git / GitHub | Version control and team collaboration |

---

## Application Architecture

The original Flask forum application was refactored into a modular architecture using **Flask Blueprints**.

Major areas of functionality are separated into modules, including:

- Posts
- Comments
- Post Reactions
- Comment Reactions
- Direct Messages
- User Settings
- User Profiles

SQLAlchemy provides the application's ORM layer and connects the Flask application to the MySQL database.

Docker Compose provides a shared development environment consisting of two primary services:

**Web Application**
- Flask application
- Gunicorn application server

**Database**
- MySQL 8.4

This architecture allows each team member to run the same application environment locally.

---

## Database

DishCourse uses **MySQL 8.4** for persistent application storage.

The database includes data for:

- Users
- Subforums
- Posts
- Comments
- Post reactions
- Comment reactions
- Direct messages

Relationships between users, posts, comments, reactions, and messages are managed through SQLAlchemy models.

---

## Getting Started

### Requirements

Before running DishCourse, install:

- Git
- Docker Desktop

---

### 1. Clone the Repository

```bash
git clone https://github.com/CircusCircusLimes/CircusCircusLimes.git
cd CircusCircusLimes
```

---

### 2. Configure Environment Variables

Create a `.env` file in the project root containing the environment variables required by the Docker configuration.

The `.env` file contains local database credentials and configuration information and should **not** be committed to GitHub.

---

### 3. Build and Start DishCourse

From the project root:

```bash
docker compose up -d --build
```

Docker Compose will start both the DishCourse web application and the MySQL database.

---

### 4. Verify the Containers

```bash
docker compose ps
```

The web and database containers should both show as running, with the MySQL container reporting a healthy status.

---

### 5. Open DishCourse

Open a browser and navigate to:

```text
http://localhost:5101
```

---

### Stop DishCourse

```bash
docker compose down
```

---

### Restart the Application

```bash
docker compose restart
```

---

## Development Workflow

The CircusCircusLimes team used a feature-branch development workflow:

```text
Feature Branches
       ↓
      dev
       ↓
     main
```

Features were developed on individual branches and submitted through GitHub pull requests.

Completed features were merged into `dev`, where the integrated application was tested before being promoted to `main`.

GitHub was used for:

- Source control
- Feature branches
- Pull requests
- Code integration
- Team collaboration
- Version management

---

## Testing

The completed application underwent team regression testing after all features were integrated into the `dev` branch.

Testing included:

- User registration and authentication
- Post creation
- Public and private posts
- Plain-text posts
- Markdown-formatted posts
- Image and video links
- Comments
- Post reactions
- Comment reactions
- Direct messaging
- User profiles
- User settings
- Docker application startup
- MySQL database connectivity
- Integrated application functionality

The final integrated build was successfully tested by the team before promotion to `main`.

---

## Project Evolution

DishCourse began as an existing Flask forum application.

The CircusCircusLimes team expanded and modernized the application by:

- Refactoring the application into Flask Blueprints
- Migrating database functionality to MySQL
- Containerizing the application with Docker
- Adding public and private posts
- Adding Markdown and media support
- Adding comments
- Adding post reactions
- Adding comment reactions
- Adding direct messaging
- Expanding user settings and profile functionality
- Creating the DishCourse brand and user interface
- Improving the application's overall structure and user experience

The project provided hands-on experience working with an existing codebase while implementing new features in a collaborative development environment.

---

## Team

**CircusCircusLimes**

- Leigh Durham
- Monah
- Sloane

Developed as part of the **Zip Code Wilmington Data Engineering Program**.

---

## Project Status

**Final Demo Build — Complete**

All planned features have been integrated and regression tested.

DishCourse is ready for final release and demonstration.