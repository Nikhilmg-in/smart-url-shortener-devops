Role Name
=========

Installs the Python runtime dependencies for the Smart URL Shortener and starts it.

Role Variables
--------------

- `app_dir`  - install path (default: `~/smart-url-shortener`)
- `app_port` - port uvicorn listens on (default: `8081`)
- `app_env`  - value of the `APP_ENV` variable

Example Playbook
----------------

    - hosts: local
      roles:
        - urlshortener
