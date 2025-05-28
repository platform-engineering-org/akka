# Flask Application: GitLab Runner Management

This Flask application provides a simple web interface to manage GitLab runners. Users can view existing runners and submit requests to provision new runners attached to a specified GitLab group.

## 🚀 Application Routes

### `/` — View Existing Runners

- **Method**: `GET`
- **Description**: Displays a list of existing GitLab runners.
- **Usage**: Navigate to the root URL in a browser to view the list of runners.

---

### `/request-runner` — Request a New GitLab Runner

- **Methods**: `GET`, `POST`
- **Description**: Serves a web form for requesting a new GitLab runner. Upon submission, the application captures the request details and initiates provisioning logic (e.g., logs the request, stores it, or triggers automation).

#### 🔧 Required Fields

| Field                | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| Environment Name     | The target environment for the runner (e.g., `dev`, `prod`)                |
| GitLab Project Group | The GitLab group **to which the runner should be attached**                |
| Tags                | Comma-separated list of tags used to match the runner to appropriate jobs   |

#### Example Usage

1. Navigate to `/request-runner` in your browser.
2. Fill out the form with the required details.
3. Submit the form to request provisioning of a new GitLab runner attached to the specified group.
