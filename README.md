# django-react-template

## How to start a project with this template

1. Clone this repo

    ```bash
    git clone git@github.com:GearShift-SL/django-react-template.git my-new-project
    ```

    ```bash
    cd my-new-project
    ```

2. Rename the `origin` to `upstream`

    ```bash
    git remote rename origin upstream
    ```

3. Add the new origin

    ```bash
    git remote add origin git@github.com:you/my-new-project.git
    ```

    ```bash
    git push -u origin main
    ```

## How to bring template updates later

1. Get the template changes
    ```bash
    git fetch upstream
    ```

2. Merge them
    ```bash
    git merge upstream/main
    ```