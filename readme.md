# Django User Search API Project

This project is a Django-based web application that includes a Search API for querying users by name or email. It supports pagination and provides an interface for managing friend requests between users.



## Project Structure
- **myproject/**: Root directory for the Django project.
  - **myproject/settings.py**: Django settings for the project.
  - **myproject/urls.py**: URL routing configuration.
  - **users/**: Django app for user management.
    - **users/models.py**: User model definitions.
    - **users/views.py**: API views for user management.
    - **users/serializers.py**: Serializers for user data.
  - **friendrequests/**: Django app for handling friend requests.
    - **friendrequests/models.py**: Friend request model definitions.
    - **friendrequests/views.py**: API views for friend requests.
  - **Dockerfile**: Docker configuration file for building the application image.
  - **docker-compose.yml**: Docker Compose file for setting up services.

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) installed on your system.
- [Docker Compose](https://docs.docker.com/compose/) installed on your system.

### Setting Up the Project

1. **Clone the Repository**
   ```sh
   git clone https://github.com/code-with-dhruv/Accuknox_dhruv
   cd myproject
   
